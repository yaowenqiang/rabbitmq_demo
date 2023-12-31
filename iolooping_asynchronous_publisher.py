import pika
import logging
import  traceback

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

class publish_engine:
    def __init__(self):
        self._number_of_messages = 10
        self._channel = None
        self._connection = None
        self._message_interval = 1
        self._delivered_messages = 0
        self.published_messages = 0

    def on_open(self, connection):
        print('Reached connection open \n')
        self._channel = self._connection.channel(on_open_callback=self.on_channel_open)

    def on_declare(self, channel):
        print('Now is on declare')
        self._channel.confirm_delivery(self.on_delivery_conformation)
        self.schedule_next_message()


        # while self._number_of_messages > 0:
            # print(self._number_of_messages)
            # self._channel.basic_publish(exchange='', routing_key='orders_g',
            #                              body='H' + str(self._number_of_messages),
            #                              properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2)
            #                              )

        #     self._number_of_messages -= 1
        #
        # self._connection.close()

    def on_channel_open(self, channel):
        print('Reached channel open \n')
        # argument_list = {'x-queue-master-locator': 'random'}
        self._channel.queue_declare('orders_g', callback=self.on_declare, durable=True, arguments=None)


    def on_delivery_conformation(self, method_frame):
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        self._delivered_messages += 1
        print('\n'
              '===================================================================================================='
              )
        print(method_frame.method.NAME)
        print(f'An {confirmation_type} has been received')
        print(f'Published {self.published_messages} messages and received delivery conformation for {self._delivered_messages} messages')
        print('\n'
              '===================================================================================================='
              )


    def publish_message(self):
        self._channel.basic_publish(exchange='', routing_key='orders_g', body='H' + str(self._number_of_messages),
                                    properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2)
                                    )

        self._number_of_messages -= 1
        self.published_messages += 1

        if self._number_of_messages >= 0:
            self.schedule_next_message()
        else:
            self._connection.close()


    def schedule_next_message(self):
        #self._connection.add_timeout(self._message_interval, self.published_messages)
        self._connection.ioloop.call_later(self._message_interval, self.publish_message)






    def on_close(self, reply_code, reply_message):
        print(reply_code)
        print(reply_message)


    def run(self):
        logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT)
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials, socket_timeout=300)
        self._connection = pika.SelectConnection(parameters, on_open_callback=self.on_open)
        self._connection.add_on_close_callback(self.on_close)

        try:
            self._connection.ioloop.start()
        except KeyboardInterrupt:
            # logging.error(traceback.format_exc())
            self._connection.close()


if __name__ == '__main__':
    engine = publish_engine()
    engine.run()
