#!/usr/bin/env python
#python Epydoc docstring for a function http://epydoc.sourceforge.net/manual-epytext.html

__version__ = '$0.1$'.split()[1]
__author__ = 'Varun Maitreya Eranki'
__doc__='''

@author: U{'''+__author__+'''<http://www.github.com/varunmaitreya>}
@version: ''' + __version__ +'''
@copyright: 2018
@license: BCD

@todo: USE A LOOP TO SPLIT EACH STRING INTO CUSTOM SIZE OF STRING PREFERABLY 0.5 GB SO THAT RABBITMQ CAN HANDLE MESSAGES FASTER
@todo: Implement ckanext-dcat

'''

import pika
import re
import crawler

def main():
	'''
	This is the main method where RabbitMQ send and receive queues are implemented
	A CKANURL is received from message queue CKAN and send for crawling.
	A JSONLines file is received from dump function and is send to datajson function for extracting dictionaries
	Dictionary will be made into chunks of data using bytecal function

'''
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='ckan')

    def callback(ch, method, properties, body):
        if re.match('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', body):
            print(" [x] Received %r" % body)
            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', body)
            urlse = str(urls[0])
            print(" [x] Sending url")
            try:
                result = crawler.dump(urlse) 	#CKAN crawler is called
            except Exception:
                print(" [x] Exception caught")
            finally:
                if(result[0] == 0  and result[1] == 0):
                    file = "/data/" + result[2]
                    data = crawler.datajson(file)

                    #TODO:HANDLE URI DATA AND SEND IT IN CHUNKS OF 0.98 GB MAXIMUM PER MESSAGE (USE 0.5 GB FOR SPEED) USING channel.basic_publish
                    #HINT:USE BYTECAL AS IT CAN CALCULATE AND CONCATENATE LENGTH OF STRINGS.

                    channel.basic_publish(exchange='', routing_key='ckan2', body='ckan crawler exited')
                elif(result[0] == 1 and result[1] == 0):
                    channel.basic_publish(exchange='', routing_key='ckan2', body='Error# error processing ckan url')

                connection.close()

    channel.basic_consume(callback,
                          queue='ckan',
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

