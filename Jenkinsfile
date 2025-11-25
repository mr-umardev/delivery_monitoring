pipeline {
    agent any

    stages {

        stage('Verify Docker Installation') {
            steps {
                powershell '''
                docker --version
                docker info
                '''
            }
        }

        stage('Build Delivery Metrics Image') {
            steps {
                powershell """
                cd "$env:WORKSPACE"
                docker build -t delivery_metrics .
                """
            }
        }

        stage('Run Delivery Metrics Container') {
            steps {
                powershell """
                docker rm -f delivery_metrics 2>$null
                docker run -d `
                    --name delivery_metrics `
                    -p 8000:8000 `
                    delivery_metrics
                """
            }
        }

        stage('Run Prometheus') {
            steps {
                powershell """
                Write-Host 'Stopping old Prometheus container if it exists...'
                docker rm -f prometheus 2>$null

                Write-Host 'Starting Prometheus with correct file mounts...'

                docker run -d `
                    --name prometheus `
                    -p 9090:9090 `
                    -v "$env:WORKSPACE/prometheus.yml:/etc/prometheus/prometheus.yml" `
                    -v "$env:WORKSPACE/alert_rules.yml:/etc/prometheus/alert_rules.yml" `
                    prom/prometheus
                """
            }
        }

        stage('Run Grafana') {
            steps {
                powershell """
                docker rm -f grafana 2>$null
                docker run -d `
                    --name grafana `
                    -p 3000:3000 `
                    grafana/grafana
                """
            }
        }
    }
}
