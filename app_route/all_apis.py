"""
@author  Anil Kumar Reddy Kunduru
@Date 3nd oct 2020
"""

import config.configs as config
from db.mongo import insert_one,get_db

db = get_db(db_name=config.db)


def create_user(data):
    """

    :param data:
    :return:
    """
    obj = insert_one(db=db, collection=config.app_users, record=dict(data))
    return str(obj.inserted_id)
