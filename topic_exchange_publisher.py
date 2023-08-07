import pika, time
from random import randint
import sys


class publish_engine:
    def __init__(self):
        self._messages = 100
        self._message_interval = 1
        self._connection = None
        self._channel = None
        self._exchange = 'sports.feed.topic'

    def make_connection(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials, socket_timeout=300)
        self._connection = pika.BlockingConnection(parameters)
        print('connected Successfully')
        return self._connection

    def channel(self):
        self._channel = self._connection.channel()
        print('Channel opened...')

    def declare_exchange(self):
        self._channel.exchange_declare(exchange=self._exchange, exchange_type='topic')
        print('Exchange declared...')

    def publish_message(self):
        message_count = 0
        score = 0
        football_score = 0
        hockey_score = 0
        while message_count < self._messages:
            message_count += 1
            score += randint(1,9)
            football_score += randint(0,1)
            hockey_score += randint(0,1)
            message_body = f'Cricket Score | batting Team: Australia | bowling Team : England | Score: {score} | wickets: 2'
            self._channel.basic_publish(exchange=self._exchange, routing_key='scores.cricket',
                                        body=message_body,
                                        properties=pika.BasicProperties(
                                            delivery_mode=2  # make message persistent
                                        ))

            message_body = f'Football Score | Brazil Vs Spain | Brazil : {football_score} | Spain: 0'
            self._channel.basic_publish(exchange=self._exchange, routing_key='scores.football',
                                        body=message_body,
                                        properties=pika.BasicProperties(
                                            delivery_mode=2  # make message persistent
                                        ))

            message_body = f'Hockey Score | India Vs China | India : 0 | China: {hockey_score}'
            self._channel.basic_publish(exchange=self._exchange, routing_key='scores.hockey',
                                        body=message_body,
                                        properties=pika.BasicProperties(
                                            delivery_mode=2  # make message persistent
                                        ))


            print(f'Published scorecard for circket, football and hockey -  {message_count}')
            time.sleep(self._message_interval)

    def close_connection(self):
        self._connection.close()
        print('Closed connection...')

    def run(self):
        self.make_connection()
        self.channel()
        self.declare_exchange()
        self.publish_message()
        self.close_connection()


if __name__ == '__main__':
    engine = publish_engine()
    engine.run()
