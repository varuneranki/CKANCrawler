CKANCrawler
============


A simple crawler that can scrape all CKAN datastores and dump the metadata into JSONLines using CkanAPI
Learn more about CkanAPI at https://github.com/ckan/ckanapi

JSON Lines is a convenient format for storing structured data that may be processed one record at a time.
Learn more about JSONLines at http://jsonlines.org/

JSONL dumps are further transformed into RDF Serilaization using CKAN dcat extention 
Learn more about CKAN dcat extention at https://github.com/ckan/ckanext-dcat#json-dcat-harvester

Installation
==================


Given that you have [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/) installed, execute the following commands:
```bash
mkvirtualenv ckancrawler
cdvirtualenv
mkdir src && cd src
git clone git@github.com:varunmaitreya/CKANCrawler.git && cd ckancrawler
```

This will create Python virtual environment called *ckancrawler* and clone [CKANCrawler](https://github.com/varunmaitreya/CKANCrawler) into src/ckancrawler in the created virtual env.

Configuration
==================


Configuration can be skipped as folder creation will be done in runtime based on ckanurl. If it fails use this step.

To create the necessary folders you will need to run init.sh script:
```
./init.sh
```

This will create the data folder with necessary subfolders. The scraped data will be stored there.

```
data
└── demo
```

Crawling Process
=================


An effort is made to extend a data linked crawler SQUIRREL to crawl CKAN dataportals instead of regular web crawling the portals.

A CKAN URL is identified by Squirrel and sent to CKAN Crawler using RabbitMQ messaging service.
CKANCrawler listens to a specific queue and upon recieveing URL starts crawling.
CkanAPI's CLI is offers dump all datasets function. It will crawl and dump all the datasets for specific portal
Learn more about dump datasets function at https://github.com/ckan/ckanapi#bulk-dumping-and-loading-operations

CLI command:
ckanapi dump datasets --all -O datasetcanada.jsonl.gz -z -p 1 -r https://demo.ckan.org/

CKAN dump is created into a gzip file ckan.jsonl.gz; a JSON Lines format. JSONLines provides functionality to unzip and seperate each Line into complete Dictionary for the dump.
In this process, CKAN dictionaries can be coverted into keys and values. Each key and value are combined to form a URI
URI = <key,value>

Using CKAN DCAT extention further mapping can be done.
Learn more about at https://github.com/ckan/ckanext-dcat#rdf-dcat-to-ckan-dataset-mapping

URIs are send back to Squirrel crawler using a different queue.
Reason for not using same queue for communication: For a specific queue there will be one procuder and one consumer. But CKANCrawler need a two way communication as it need to send back data to Squirrel or a message describing why crawling has failed. This pattern is explained in detail using an anti pattern.
Learn more at https://derickbailey.com/2015/07/22/airport-baggage-claims-selective-consumers-and-rabbitmq-anti-patterns/


Known Issues:
==============


CkanAPI:
In Windows, it is only possible to enable only one worker and can cause issues. In Linux, it might cause similar issues. Feel free to reopen issue #30.
CkanAPI does not have a worker alive mechanism, for example, if a worker fails, it will throw error and stop crawling.
If CkanAPI is fed with a non CKAN URL it will instantly throw an exception. There is no functionality to handle specific exceptions from CLI. Learn more about at issue #89.

RabbitMQ:
It has a limit of 1GB as maximum limit per message. Often it takes long wait time for message to reach to consumer depending on size of message and number of queues.
It is not adviced to open a queue and send few messages and close it immediately.

CKAN DCAT extention:
It relies on ckan harvester extention and ckan. pip install ckanext-harvest and pip install ckan in general might result in some issues. Please refer to respective github pages for issues.
https://github.com/ckan/ckanext-harvest
https://github.com/ckan/ckan
For installation of ckan, please use "install from source" mentioned in http://docs.ckan.org/en/2.8/

HISTORY:
==============

This crawler was made taking ckan-aggregator-py as inspiration. ckan-aggregator-py could have been directly used but ckanclient library is DEPRECATED. Alternative and more robust library, ckanapi is used to give similar functionality.
Plan of action was to adapt ckan-aggregator-py into Jython and directly use it to incorporate into Squirrel but Jython has it's own issues with ckanapi library. Jython uses urllib3 implementation for ckanapi instead of requests. Last stable update for Jython has support yet it failed to work as ckanapi uses https requests and Jython only supports http requests. From JAVA9 Jython will have much more security protocol issues. Alternative was to implement everything in Python and use message queue for passing data between Java and Python. Only limition is maximum message size = 1GigaByte.

