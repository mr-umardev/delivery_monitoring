pipeline {
  agent any

  stages {

    stage('Verify Docker Installation') {
      steps {
        // Use triple-single quotes to avoid Groovy interpolation of $ characters
        powershell '''
        docker --version
        docker info
        '''
      }
    }

    stage('Setup Workspace') {
      steps {
        // Copy files from a known host path into the Jenkins workspace (optional)
        // If you already check out from Git, you can remove this stage.
        powershell '''
        if (Test-Path "$env:WORKSPACE\\delivery_monitoring") {
          # move files into workspace root (if you previously checked out a subfolder)
          Move-Item "$env:WORKSPACE\\delivery_monitoring\\*" "$env:WORKSPACE" -Force -ErrorAction SilentlyContinue
          Remove-Item "$env:WORKSPACE\\delivery_monitoring" -Recurse -Force -ErrorAction SilentlyContinue
        }
        '''
      }
    }

    stage('Build Delivery Metrics Image') {
      steps {
        powershell '''
        cd "$env:WORKSPACE"
        docker build -t delivery_metrics .
        '''
      }
    }

    stage('Run Delivery Metrics Container') {
      steps {
        powershell '''
        cd "$env:WORKSPACE"
        docker rm -f delivery_metrics 2>$null || true
        docker run -d --name delivery_metrics -p 8000:8000 delivery_metrics
        '''
      }
    }

    stage('Run Prometheus & Grafana') {
      steps {
        powershell '''
        cd "$env:WORKSPACE"
        docker rm -f prometheus 2>$null || true
        docker rm -f grafana 2>$null || true

        docker run -d --name prometheus -p 9090:9090 `
          -v "$env:WORKSPACE\\prometheus.yml":/etc/prometheus/prometheus.yml `
          -v "$env:WORKSPACE\\alert_rules.yml":/etc/prometheus/alert_rules.yml `
          prom/prometheus

        docker run -d --name grafana -p 3000:3000 grafana/grafana
        '''
      }
    }
  }

  post {
    always {
      echo "Pipeline finished. Check container statuses with docker ps."
    }
  }
}
