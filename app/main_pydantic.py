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
    name: str = "Requestor"               # defaulted optional
    published: Optional[bool] = None      # truly optional
    id: Optional[int] = None


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


# R - Read post by id
@app.get("/posts/{id}", status_code= status.HTTP_200_OK)
def get_post_by_id (id: int) :

    cursor.execute ("SELECT * FROM posts WHERE id = %s", (id,))                 # new thing we learnt here, to always use a tuple for passing
    post = cursor.fetchone()

    if not post :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id = {id} not found in DB")

    return {"post" : post}


# C - Create a post
@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post(post: Post) :

    if post.id is not None:
        cursor.execute ("SELECT * FROM posts WHERE id = %s", (post.id,))

        found = cursor.fetchone()

        if not found :
            cursor.execute ("INSERT INTO posts(id, title, content, published) " \
                    "VALUES (%s, %s, %s, %s) RETURNING *", 
                    (post.id, post.title, post.content, post.published))
            
            created_post = cursor.fetchone()
            conn_obj.commit()
            return {"post": created_post}

        else :
            updated_post = update_post_by_id(post.id, post)
            return {"updated" : updated_post}


    cursor.execute ("INSERT INTO posts(title, content, published) " \
                    "VALUES (%s, %s, %s) RETURNING *", 
                    (post.title, post.content, post.published))

    created_post = cursor.fetchone()
    conn_obj.commit()    


# U - Update post by id
@app.put ("/posts/{id}", status_code= status.HTTP_200_OK)
def update_post_by_id (id: int, post: Post):
    cursor.execute ("UPDATE posts set title = %s, content = %s, " \
                    "published = %s WHERE ID = %s RETURNING *", 
                    (post.title, post.content, post.published, str(id)))
    fetched_post = cursor.fetchone()

    conn_obj.commit()

    if not fetched_post :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail= f"Post with id = {id} not found")
    
    
    return {"updated_post" : post}


# D - Delete post by id
@app.delete ("/posts/{id}", status_code= status.HTTP_202_ACCEPTED)
def delete_by_id (id: int) :
    cursor.execute ("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()

    if not deleted_post :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail= f"Post with id = {id} not found")
    
    conn_obj.commit()

    return {"deleted post" : deleted_post}