"""
@author : Anil kumar Reddy
@Date : 24th sep 2020
"""

env = "dev"

def get_db_congigs():
    if env=="dev":
        port_number = 27017
        host = "127.0.0.1"
    else:
        port_number = 27017
        host = "127.0.0.1"
    return port_number,host


db = "socialmedia"
app_users = "app_users"
streem_config = "streem_config"
user_timeline = "user_timeline"
serach_keywords = "serach_keywords"
