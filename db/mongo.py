"""
@author : Anil kumar Reddy kunduru
@Date : 24th sep 2020
"""


from pymongo import MongoClient
import gridfs
import configration.constants as config

port_number,host = config.get_db_configs()


client = MongoClient(host=host, port=port_number)



def get_db(db_name):
    return client[db_name]

# mydatabase = get_db(db_name=db)

def get_collection(db,collection_name):
    return db[collection_name]

# mycollection = get_collection(db=mydatabase,collection_name=myTable)

def get_db_collection(db_name,collection_name):
    db = client[db_name]
    return db,db[collection_name]

def count(db,collection,q):
    return db[collection].count_documents(q)

def insert_one(db,collection,record):
    return db[collection].insert_one(record)

def insert_many(db,collection,records):
    return db[collection].insert_many(records)

def find(db,collection,query):
    return db[collection].find(query)

#print(list(find(db=get_db(db_name=config.db),collection=config.streem_config,query={"user_id":"5f7c88d305dd5ed504a5e0d3"})))
# print(count())
# print(insert_one())
# print(insert_many())
# print(count())
