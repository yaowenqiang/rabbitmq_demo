import pika
from publisher import connect_machine


def callback(ch, method, properties, body):
    print(f'[X] Received {body}')


if __name__ == '__main__':
    connection, channel = connect_machine()
    channel.queue_declare(queue='sample_test', durable=True)
    channel.basic_consume('sample_test', on_message_callback=callback, auto_ack=True)

    print(f'[X] Waiting for messages, To exit press CTRL-C')
    channel.start_consuming()

