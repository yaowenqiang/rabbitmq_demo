# https://pika.readthedocs.io/en/stable/
import pika, time

message_count = 15
count = 1


def connect_machine():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', 5672, '/', credentials, socket_timeout=300))
    channel = connection.channel()
    return connection, channel


def disconnect_machine(connection):
    connection.close()


if __name__ == '__main__':

    while count <= message_count:
        body_content = f"Message number: {count}"
        count += 1

        connection, channel = connect_machine()
        channel.basic_publish(exchange='', routing_key='sample_test', body=bytes(body_content.encode('utf-8')))
        disconnect_machine(connection)
        print(f'[X] Send {body_content}')

        time.sleep(1)
