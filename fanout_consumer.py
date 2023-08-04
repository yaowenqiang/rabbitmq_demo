import pika, time
import logging
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(level=logging.INFO)

class consumer_engine:
    def __init__(self):
        self._messages = 100
        self._message_interval = 1
        self._queue_name = None
        self._connection = None
        self._channel = None
        self._exchange = 'score.feed.exchange'


    def make_connection(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials, socket_timeout=300)
        self._connection = pika.BlockingConnection(parameters)
        LOGGER.error('connected Successfully')
        return self._connection


    def channel(self):
        self._channel = self._connection.channel()
        LOGGER.info('Channel opened...')


    def declare_exchange(self):
        self._channel.exchange_declare(exchange=self._exchange,exchange_type='fanout')
        LOGGER.info('Exchange declared....')


    def declare_queue(self):
        result = self._channel.queue_declare('',exclusive=True)
        LOGGER.info(result)
        self._queue_name = result.method.queue
        LOGGER.info('Queue declared...')
        LOGGER.info(' [*] Waiting for messages. To exit press CTRL+C')


    def make_binding(self):
        LOGGER.info('making binding...')
        self._channel.queue_bind(exchange=self._exchange, queue=self._queue_name)
        LOGGER.info(f'Made binding between exchanges: {self._exchange} and {self._queue_name}')


    def on_message(self, channel, method, properties, body):
        LOGGER.info(f' [X] Feed Received - {body} \n')
        time.sleep(1)


    def consume_message(self):
        self._channel.basic_consume(self._queue_name, self.on_message, auto_ack=True)
        self._channel.start_consuming()

    def close_connection(self):
        self._connection.close()
        LOGGER.info('Closed connection...')



    def run(self):
        self.make_connection()
        self.channel()
        self.declare_exchange()
        self.declare_queue()
        self.make_binding()
        self.consume_message()


if __name__ == '__main__':
    engine = consumer_engine()
    engine.run()
