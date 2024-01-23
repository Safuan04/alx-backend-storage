#!/usr/bin/env python3
"""This is a  Python script that provides
    some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs
    nginx = logs.nginx
    
    doc_num = nginx.count_documents({})
    get_meth = nginx.count_documents({'method':'GET'})
    post_meth = nginx.count_documents({'method':'POST'})
    put_meth = nginx.count_documents({'method':'PUT'})
    patch_meth = nginx.count_documents({'method':'PATCH'})
    delete_meth = nginx.count_documents({'method':'DELETE'})
    status_get_path = nginx.count_documents({'$and': [{'method': 'GET'}, {'path': '/status'}]})
    
    print(f'{doc_num} logs\n'
        'Methods:\n'
        f'\tmethod GET: {get_meth}\n'
        f'\tmethod POST: {post_meth}\n'
        f'\tmethod PUT: {put_meth}\n'
        f'\tmethod PATCH: {patch_meth}\n'
        f'\tmethod DELETE: {delete_meth}\n'
        f'{status_get_path} status check')

