from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Class for Pydantic model which guides the post API body
class Post (BaseModel) :
    title: str
    content: str
    name: str = "Requestor"                 # defaulted optional
    published_at: Optional[int] = None      # truly optional


# We will also connect to the PostGre server in this file, we use psycopg2 for that
# DB Connection snippet

conn_try_count = 0

while conn_try_count < 3:
    try:
        conn_obj = psycopg2.connect (host= 'localhost', database= 'fastapi', 
                                user= 'postgres', password= 'password',
                                cursor_factory= RealDictCursor)
        
        cursor = conn_obj.cursor()
        print ("DB connection successful")
        break

    except Exception as error:
        print (f"Connection error: {error}")
        time.sleep(2)
        conn_try_count += 1


@app.get("/")                       # random test API via base path
def base_func() :
    return {"status" : "success"}

# R - Read all posts
@app.get("/posts", status_code= status.HTTP_200_OK)
def get_posts() :
    cursor.execute ("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()

    return {"posts": posts}