import pika
import time

class consume_engine:
    def __init__(self):
        self._messages = 100
        self._message_interval = 1
        self._queue_name = None
        self._connection = None
        self._channel = None
        self._exchange = 'sports.feed.exchange'


    def connection(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials, socket_timeout=300)
        self._connection = pika.BlockingConnection(parameters)
        print('connected Successfully')
        return self._connection

    def channel(self):
        self._channel = self._connection.channel()
        print('Channel opened...')

    def declare_exchange(self):
        self._channel.exchange_declare(exchange=self._exchange, exchange_type='direct')
        print('Exchange declared...')

    def declare_queue(self):
        result = self._channel.queue_declare('',exclusive=True)
        self._queue_name = result.method.queue
        print('Queue declared...')
        print('[X] Waiting for messages, To exit press CTRL+C')

    def make_binding(self):
        self._channel.queue_bind(exchange=self._exchange, routing_key='scores.football',
                                 queue=self._queue_name
                                 )
        print(f'Made binding between exchanges {self._exchange} and queue: {self._queue_name}')



    def on_message(self, channel, method, properties, body):
        print(f'[X] Feed Received - {body} \n')
        time.sleep(1)


    def consume_message(self):
        self._channel.basic_consume(self._queue_name, self.on_message, auto_ack=True)
        self._channel.start_consuming()


    def run(self):
        self.connection()
        self.channel()
        self.declare_exchange()
        self.declare_queue()
        self.make_binding()
        self.consume_message()


if __name__ == '__main__':
    engine = consume_engine()
    engine.run()

