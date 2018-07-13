import sys
from setuptools import setup

setup(
    name = "ckancrawler",        # what you want to call the archive/egg
    version = "0.1",
    packages=['ckancrawler'],    # here you can ckancrawler.tests, ckancrawler.cli, ckancrawler.mock if needed
                                
    dependency_links = [],      # here add ckanext-dcat, ckanext-harvest, ckan eggs installation but not good practice. Refer to documentation
    install_requires=[      	# here add ckanext-dcat, ckanext-harvest, ckan as prerequisites
		'gzip',
		'json',
		'jsonlines',
		'pika',
		're',
		'shutil',
		'subprocess'
		],
    extras_require={},      # optional features that other packages can require
                            #   like 'helloworld[foo]'
    package_data = {},
    author="Varun Maitreya Eranki",
    author_email = "varun.maitreya@gmail.com",
    description = "CKANCrawler for crawling CKAN datastores",
    license = "BSD",
    keywords= "",
    url = "http://github.com/varunmaitreya/CKANCrawler",
    entry_points = {
        "console_scripts": [        # command-line executables to expose
            "ckancrawler = ckancrawler.main:main",
        ],
        "gui_scripts": []       # GUI executables (creates pyw on Windows)
    }
)
