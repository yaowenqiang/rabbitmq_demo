import pika
import logging
from pika.frame import *
import  traceback

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

class consume_engine:
    def __init__(self):
        self._channel = None
        self._connection = None
        self.QUEUE = 'orders_g'
        self.EXCHANGE = ''


    def on_open(self, connection):
        print('Reached connection open \n')
        self._channel = self._connection.channel(on_open_callback=self.on_channel_open)


    def on_declare(self, method):
        print('Now in on declare')
        print(method)
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)
        self._consumer_tag = self._channel.basic_consume(self.QUEUE,self.on_message)
        print('Now in after declare')



    def on_consumer_cancelled(self, method_frame):
        print(method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, basic_deliver, properties, body):
        self._channel.basic_ack(basic_deliver.delivery_tag)
        print(basic_deliver)
        print('Delivery tag is: ' + str(basic_deliver.delivery_tag))
        print(properties)
        print('Received content: ' + str(body))


    def on_channel_open(self, channel):
        print('Reached channel open \n')
        # argument_list = {'x-queue-master-locator': 'random'}

        # self._channel.queue_declare(self.QUEUE, durable=True, arguments=argument_list, callback=self.on_declare)
        self._channel.queue_declare(self.QUEUE, durable=True, callback=self.on_declare)
        print('Reached queue declare \n')

    def on_close(self, reply_code, reply_message):
        print(reply_code)
        print(reply_message)
        print('connection is being closed \n')


    def stop_consuming(self):
        print('Keyboard Interrupt received !!! ')
        if self._channel:
            self._channel.basic_cancel(self._consumer_tag, self.on_cancelok)


    def on_cancelok(self, unused_frame):
        self._channel.close()
        self.close_connection()


    def stop(self):
        self._closing = True
        self.stop_consuming()
        self._connection.ioloop.start()


    def close_connection(self):
        self._connection.close()

    def run(self):
        logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT)
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials, socket_timeout=300)
        self._connection = pika.SelectConnection(parameters, on_open_callback=self.on_open)
        self._connection.add_on_close_callback(self.on_close)

        try:
            self._connection.ioloop.start()
        except KeyboardInterrupt:
            self.stop_consuming()


if __name__ == '__main__':
    engine = consume_engine()
    engine.run()


