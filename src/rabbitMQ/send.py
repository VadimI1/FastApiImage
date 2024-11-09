import os

import pika
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)

load_dotenv(os.path.join(BASE_DIR, '.env'))
def input_rabbitMQ(mess):
    credentials = pika.PlainCredentials(username=os.environ['USERNAME'], password=os.environ['PASSWORD'])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ['HOST'], 5672, '/', credentials))

    channel = connection.channel()

    channel.queue_declare(queue='get')


    channel.basic_publish(exchange='', routing_key='get', body=mess)
    print(f" [x] Sent '{mess}'")
    connection.close()

    return mess

def post_rabbitMQ(mess):
    credentials = pika.PlainCredentials(username=os.environ['USERNAME'], password=os.environ['PASSWORD'])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ['HOST'], 5672, '/', credentials))

    channel = connection.channel()

    channel.queue_declare(queue='post')

    channel.basic_publish(exchange='', routing_key='post',
                          body=f"{mess[0]} {mess[1]}")
    print(f" [x] Sent '{mess}'")
    connection.close()

    return mess

def put_rabbitMQ(mess):
    credentials = pika.PlainCredentials(username=os.environ['USERNAME'], password=os.environ['PASSWORD'])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ['HOST'], 5672, '/', credentials))

    channel = connection.channel()

    channel.queue_declare(queue='put')

    channel.basic_publish(exchange='', routing_key='put',
                          body=mess)
    print(f" [x] Sent '{mess}'")
    connection.close()

    return mess

def del_rabbitMQ(mess):
    credentials = pika.PlainCredentials(username=os.environ['USERNAME'], password=os.environ['PASSWORD'])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ['HOST'], 5672, '/', credentials))

    channel = connection.channel()

    channel.queue_declare(queue='delete')

    channel.basic_publish(exchange='', routing_key='delete',
                          body=mess)
    print(f" [x] Sent '{mess}'")
    connection.close()

    return mess