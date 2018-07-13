#!/usr/bin/env python
#python Epydoc docstring for a function http://epydoc.sourceforge.net/manual-epytext.html

__version__ = '$0.1$'.split()[1]
__author__ = 'Varun Maitreya Eranki'
__doc__='''

@author: U{'''+__author__+'''<http://www.github.com/varunmaitreya>}
@version: ''' + __version__ +'''
@copyright: 2018
@license: BCD

This is used to send a message stimulation as if java end point has sent a message via ckan queue
NO NEED FOR THIS EXCEPT FOR TESTING WHEN JAVA END POINT IS NOT AVAILABLE

'''

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

#channel.basic_publish(exchange='', routing_key='ckan2', body='hi ckan')
channel.basic_publish(exchange='', routing_key='ckan', body='https://demo.ckan.org')

print(" [x] Sent 'ckancrawler started'")
connection.close()



