from prometheus_client import start_http_server, Summary, Gauge
import random
import time
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# -----------------------
#  Prometheus Metrics
# -----------------------
total_deliveries = Gauge("total_deliveries", "Total number of deliveries")
pending_deliveries = Gauge("pending_deliveries", "Number of pending deliveries")
on_the_way_deliveries = Gauge("on_the_way_deliveries", "Number of deliveries on the way")
average_delivery_time = Summary("average_delivery_time", "Average delivery time in seconds")


# -----------------------
#  Simulation Logic
# -----------------------
def simulate_delivery():
    # 🔥 Force high pending numbers to trigger Prometheus alert
    pending = random.randint(50, 100)

    on_the_way = random.randint(5, 20)
    delivered = random.randint(30, 70)

    # Optional: also push avg delivery time high to trigger second alert
    avg_time = random.uniform(40, 60)

    total = pending + on_the_way + delivered

    # Log values
    logging.info(
        f"Pending={pending}, On-the-way={on_the_way}, Delivered={delivered}, AvgTime={avg_time:.2f}s"
    )

    # Update Prometheus metrics
    total_deliveries.set(total)
    pending_deliveries.set(pending)
    on_the_way_deliveries.set(on_the_way)
    average_delivery_time.observe(avg_time)


# -----------------------
#  Main Entry Point
# -----------------------
if __name__ == "__main__":
    logging.info("Starting Prometheus metrics server on port 8000...")
    start_http_server(8000, addr="0.0.0.0")

    logging.info("Simulating deliveries…")
    while True:
        simulate_delivery()
        time.sleep(1)
