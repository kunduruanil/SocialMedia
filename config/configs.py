"""
@author : Anil kumar Reddy
@Date : 24th sep 2020
"""

env = "dev"

def get_db_congigs():
    if env=="dev":
        port_number = 27017
        host = "127.0.0.1"
        db = "socialmedia"
        myTable = "twitter"
    else:
        port_number = 27017
        host = "127.0.0.1"
        db = "socialmedia"
        myTable = "twitter"
    return port_number,host,db,myTable



