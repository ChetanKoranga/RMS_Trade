import pymongo as pm
from pymongo import MongoClient
# from flask import Flask
import random
from random import randint
import datetime
from time import sleep
import time
# app = Flask(__name__)


# app.config[""]

client=MongoClient()


db=client["algo_db"]


collection=db["abc"]



i = 1
while True:
    # timestamp = datetime.datetime.now()
    dict={str(i):randint(100,100000),'timestamp':str(datetime.datetime.now().time())}
    post = [dict]
    posts=db.posts
    posts.insert(post)
    i += 1
    sleep(5)