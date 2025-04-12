import os

from dotenv import load_dotenv
from pika import ConnectionParameters, BlockingConnection

load_dotenv()
RMQ_HOST = os.getenv("RMQ_HOST")
RMQ_PORT = os.getenv("RMQ_PORT")

connection_params = ConnectionParameters(
    host=RMQ_HOST,
    port=RMQ_PORT,
)

def process_message(ch, method, properties, body):
    print(f"Полученное сообщение: {body.decode()}")

    # x = 1 / 0 # Ошибка

    ch.basic_ack(delivery_tag=method.delivery_tag)  # Подтверждение обработки сообщения (хороший вариант)

def main():
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue="messages")

            ch.basic_consume(
                queue="messages",
                on_message_callback=process_message,
                # auto_ack=True, # Автоподтверждение обработки сообщения (плохой вариант)
            )
            print("Ожидание сообщений. Для выхода нажмите CTRL+C")
            ch.start_consuming()

if __name__ == "__main__":
    main()