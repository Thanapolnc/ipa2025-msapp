import pika
import os

def produce(host, body):
    # Get RabbitMQ credentials from environment variables
    rabbitmq_user = os.environ.get("RABBITMQ_USER", "guest")
    rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "guest")
    # Create connection with credentials
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, credentials=credentials)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    channel.queue_declare(queue="router_jobs")
    channel.queue_bind(queue="router_jobs", exchange="jobs", \
    routing_key="check_interfaces")

    channel.basic_publish(exchange="jobs", \
    routing_key="check_interfaces", body=body)

    connection.close()

if __name__ == "__main__":
    produce("localhost", "192.168.1.44")
