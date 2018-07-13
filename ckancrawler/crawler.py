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

'''

import subprocess
import jsonlines
import json
import gzip
import pathlib
import shutil
import sys
from tld import get_tld

def dump(str):
    """
    dump function will crawl and dump all the datasets for specific portal
    This function can be used in conjuction with datajson to see all the datasets

    @type str: string
    @param str: CKANURL is received in string format
    @rtype a: number
    @param a: Value of a is 0 if crawling successful, Value of a is 1 if crawling unsuccessful
    @rtype b: number
    @param b: Value of b is always 0 to send crawler is exited
    """
    str2 = str
    res = get_tld(str2, as_object=True)  #top level domain name is extracted from CKANURL for naming dataset.
    str2= res.domain+".jsonl.gz"
    a = 0
    pathlib.Path('/data/' + res.domain + '').mkdir(parents=True, exist_ok=True)
    i = "1"  #change this value to upto 4 for increasing number of workers. also make sure it is always string
    try:

        subprocess.check_output(["sudo","ckanapi","dump","datasets","--all","-O",str2,"-z","-p",i,"-r",str])
    except:
        print("ckan dumping failed unexpectedly")
        a = 1
    finally:
        print("exiting ckancrawler")
        b = 0
    return a,b,str2

def datajson(file):
    """
    datajson function will open the gzip file and unzip to temp.jsonl file. using jsonlines will dump jsonlines to dictionary and all keys and values are loaded.
    This function can be used to see all the datasets either specific keys or builtin pretty format of jsonlines library

    @type file: file
    @param file: CKAN dump file
    @rtype data: list
    @param data: <key,values> is collectively called as URI
    """
    data = []
    da = {}

    #dump file is unzipped using gzip
    with gzip.open(file, 'rb') as f_in:
        with open('temp.jsonl', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    #jsonlines is used to open JSONLines file and read each line as object
    with jsonlines.open('temp.jsonl') as reader:
        for obj in reader:
            # print '+++++'
            # print obj
            # print '#####'


            try:
                #using json.dumps will dump all objects into a dictionary
                dict = json.dumps(obj)

                #using json.load will load all keys of a dictionary
                key = json.loads(dict)

                #print values of a specific key. can be used in conjunction for example: key["url"] key["id"] key["title"]
                print key["url"]

                #can be used to see each line in pretty print format
                #print(json.dumps(obj, indent=4))

                #we are trying to extract each key and value of each key as lists and send it back for further processing
                for d in dict:
                    for key, value in d.iteritems():
                        print key,value
                        for subkey, subvalue in value.iteritems():
                            print subkey,subvalue

                        if key not in da:
                            da[key] = value
                        else:
                            da = {}
                            da[key] = value
                    data.append(da)
            except Exception, err:
                sys.stderr.write('Exception Error: %s' % str(err))

    return data











