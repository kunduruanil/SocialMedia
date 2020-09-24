"""
@author : Anil kumar Reddy
@Date : 24th sep 2020
"""


from pymongo import MongoClient
from config.configs import get_db_congigs

port_number,host,db,myTable = get_db_congigs()

client = MongoClient(host=host, port=port_number)


def get_db(db_name):
    return client[db_name]

mydatabase = get_db(db_name=db)

def get_collection(db=mydatabase,collection_name=myTable):
    return db[collection_name]

mycollection = get_collection(db=mydatabase,collection_name=myTable)

def count(db=mydatabase,myTable=mycollection,q={}):
    return db.myTable.count_documents(q)

def insert_one(db=mydatabase,myTable=mycollection,record={}):
    return db.myTable.insert_one(record)

def insert_many(db=mydatabase,myTable=mycollection,records=[{},{}]):
    return db.myTable.insert_many(records)


print(count())
print(insert_one())
print(insert_many())
print(count())
