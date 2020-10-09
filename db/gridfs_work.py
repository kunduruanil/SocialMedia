
## We start by creating a GridFS instance to use:

from pymongo import MongoClient
import gridfs

db = MongoClient().gridfs_example
fs = gridfs.GridFS(db)

a = fs.put(open(r"E:\phone videos\VID-20160921-WA0000.mp4","rb"),filename="video1")

print(a)

print(fs.get(a))

