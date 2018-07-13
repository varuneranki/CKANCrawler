#!/usr/bin/python
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

import json
import gzip

def bytecal(file):
    """
    bytecal function will open the gzip file and read each line and calculates number of bytes.
    This function can be used to calculate size of the datasets or specific string size

    @type file: file
    @param file: CKAN dump file
    @rtype data: list
    @param data: any type of data depends on file you read.
    """

    #open a file and read size of all the data in file
    data = []
    with gzip.open(file, 'rb') as f:
        for line in f:
            data.append(json.loads(line))

        for d in data:
            print(len(d))
        print len(data)

    #this is a sample line of dump from https://demo.ckan.org
    string = b'{\"author\":\"TKKIM\",\"author_email\":\"misoh049@gmail.com\",\"creator_user_id\":\"bb970558-8d48-4874-9794-bd4740099474\",\"extras\":[],\"groups\":[],\"id\":\"62513382-3b26-4bc8-9096-40b6ce8383c0\",\"isopen\":true,\"license_id\":\"other-open\",\"license_title\":\"Other (Open)\",\"maintainer\":\"TKKIM\",\"maintainer_email\":\"misoh049@gmail.com\",\"metadata_created\":\"2017-08-05T03:16:52.857800\",\"metadata_modified\":\"2017-08-05T03:19:33.886925\",\"name\":\"100-validated-species-of-plants\",\"notes\":\"This data includes the typical plants for machine learning test.\",\"num_resources\":1,\"num_tags\":3,\"organization\":null,\"owner_org\":null,\"private\":false,\"relationships_as_object\":[],\"relationships_as_subject\":[],\"resources\":[{\"cache_last_updated\":null,\"cache_url\":null,\"created\":\"2017-08-05T03:17:44.192463\",\"datastore_active\":false,\"description\":\"This file includes 100 species list for machine learning test.\",\"format\":\"CSV\",\"hash\":\"\",\"id\":\"bf4d5116-634e-43f2-a41c-9ae22d362083\",\"last_modified\":null,\"mimetype\":null,\"mimetype_inner\":null,\"name\":\"validated_100_species.csv\",\"package_id\":\"62513382-3b26-4bc8-9096-40b6ce8383c0\",\"position\":0,\"resource_type\":null,\"revision_id\":\"9d6a7ee2-022e-4018-8de0-b9b628476b26\",\"size\":null,\"state\":\"active\",\"url\":\"https://demo.ckan.org/dataset/62513382-3b26-4bc8-9096-40b6ce8383c0/resource/bf4d5116-634e-43f2-a41c-9ae22d362083/download/validated_100_species.csv\",\"url_type\":\"upload\"}],\"revision_id\":\"3bbdcb05-6394-4285-8cc4-237ef77d1f15\",\"state\":\"active\",\"tags\":[{\"display_name\":\"flower\",\"id\":\"806b0369-bc31-4cc2-8147-861885f4e762\",\"name\":\"flower\",\"state\":\"active\",\"vocabulary_id\":null},{\"display_name\":\"image recognition\",\"id\":\"2e583787-08a5-4e28-a9d4-ec5ae94e19c5\",\"name\":\"image recognition\",\"state\":\"active\",\"vocabulary_id\":null},{\"display_name\":\"machine learning\",\"id\":\"7cfc3a49-2999-4aba-bf49-93678a30e62f\",\"name\":\"machine learning\",\"state\":\"active\",\"vocabulary_id\":null}],\"title\":\"100 Validated Species of Plants\",\"type\":\"dataset\",\"url\":\"\",\"version\":\"\"}'
    #multiplying same string to check how size increases and where it fails
    string2 = string*1024*1024
    #copying only first 1GB of string2 into string3
    string3 = string2[:1073741824] #these numbers are Giga bytes and not Giga bits.
    print(len(string3))
    print(len(string2))

    #TODO: USE A LOOP TO SPLIT EACH STRING INTO CUSTOM SIZE OF STRING PREFERABLY 0.5 GB SO THAT RABBITMQ CAN HANDLE MESSAGES FASTER
    #DO NOT TRY EXCEEDING SIZE OF STRING MORE THAN 2GB AND YOU CAN GET INTO OUT OF MEMORY ISSUES.

    return data

