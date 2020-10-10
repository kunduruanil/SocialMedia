"""
@author  Anil Kumar Reddy Kunduru
@Date 3nd oct 2020
"""

import json
import configration.constants as config
from db.mongo import insert_one,get_db,insert_many,find,update_one
from bson.objectid import ObjectId

db = get_db(db_name=config.db)


def create_user(data):
    """

    :param data:
    :return:
    """
    obj = insert_one(db=db, collection=config.app_users, record=dict(data))
    return str(obj.inserted_id)


def create_config(data):
    """

    :param data:
    :return:
    """
    obj = insert_one(db=db, collection=config.streem_config, record=dict(data))
    return str(obj.inserted_id)

def update_config(data):
    """

    :param query:
    :return:
    """
    query = {"_id":ObjectId(data["config_id"])}
    data.pop('config_id', None)
    newvalues = {"$set": data}
    obj = update_one(db=db, collection=config.streem_config,query=query,newvalues=newvalues)
    return obj.matched_count > 0




def insert_search_keyword_sentiment(data,collection):
    """

    :param data:
    :return:
    """
    obj = insert_one(db=db, collection=collection, record=dict(data))
    return str(obj.inserted_id)

def get_all_cofig_by_userid(query):
    """

    :param query:
    :return:
    """
    list_cofigs = find(db=db, collection=config.streem_config, query=dict(query))
    list_cofigs = list(list_cofigs)
    return list_cofigs

def add_dataframe(df,collection_name):
    """

    :param data:
    :return:
    """
    df = df.transpose()
    data = json.loads(df.to_json())
    obj = insert_many(db=db, collection=collection_name,records=data.values())
    return obj

def check_user_login(query):
    """

    :param data:
    :return:
    """
    #query = {"_id":ObjectId(data["user_id"])}
    user = find(db=db, collection=config.streem_config, query=dict(query))
    if user:
        return True
    else:
        return False

if __name__ == '__main__':
    data = {"config_id":"5f816d9facc009815c4dbcec","source":"twitter","frequency":"Daily",
            "list_of_search_words":["data science"],"list_of_users":["kunduruanil"]}
    result = update_config(data)
    print(result)
    print(type(result))
    print(result.matched_count > 0)