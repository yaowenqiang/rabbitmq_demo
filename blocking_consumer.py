import pika
import time

class consume_engine:
    def __init__(self):
        self._messages = 100
        self._message_interval = 1
        self._queue_name = 'task_queue'
        self._connection = None
        self._channel = None


    def connection(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials, socket_timeout=300)
        self._connection = pika.BlockingConnection(parameters)
        print('connected Successfully')
        return self._connection

    def channel(self):
        self._channel = self._connection.channel()
        print('Channel opened...')


    def declare_queue(self):
        self._channel.queue_declare(queue=self._queue_name, durable=True)
        print('Queue declared...')
        print('[X] Waiting for messages, To exit press CTRL+C')



    def on_message(self, channel, method, properties, body):
        print(f'[X] working on {body}')
        time.sleep(1)
        print('[X] Done')

        self._channel.basic_ack(delivery_tag=method.delivery_tag)


    def consume_message(self):
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(self._queue_name, self.on_message)
        self._channel.start_consuming()


    def run(self):
        self.connection()
        self.channel()
        self.declare_queue()
        self.consume_message()


if __name__ == '__main__':
    engine = consume_engine()
    engine.run()

