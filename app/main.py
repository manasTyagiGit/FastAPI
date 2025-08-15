from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
# for schema validation
from pydantic import BaseModel
import psycopg2                         # for connection to DB
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

#To create all models via the engine in database.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# class for extension of BaseModel
class PostBody (BaseModel) :
    title: str
    content: str
    #Defaultable optional
    published: bool = True
    #Truly Optional
    #rating: Optional[int] = None

### CONNECTION TO DATABASE ###

conn_try_count = 0

while conn_try_count < 3 :

    try:
        conn = psycopg2.connect (host= 'localhost', database= 'fastapi', 
                                user= 'postgres', password= 'password',
                                cursor_factory= RealDictCursor)
        
        cursor = conn.cursor()

        print ("DB connection successful")
        break

    except Exception as error:
        print (f"Connection error: {error}")
        time.sleep(2)
        conn_try_count += 1
    

#Storing posts here, i.e., a list of dictionaries
all_posts = [{"title": "title of post 1", "content": "content of post 1", "id" : 1},
             {"title": "title of post 2", "content": "content of post 2", "id" : 2}
            ]


# TESTING THE SQLALCHEMY ORM STUFF
@app.get("/sqlalchemy")
def test_sqlorm(db: Session = Depends(get_db)) :
    posts = db.query(models.Post).all()
    return {"posts" : posts}


@app.get("/")
def first_api() :
    return {"Hello" : "Welcome to my first api!"}

@app.get("/posts")
def get_posts() :
    cursor.execute ("""SELECT * FROM posts""")
    posts = cursor.fetchall()

    print (posts)
    return {"Hey user, posts are" : posts}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: PostBody, db: Session = Depends(get_db)) :

    # post_dict = post.model_dump()
    
    # post_dict['id'] = randrange (0, 10000000)

    # all_posts.append(post_dict)

    # # This is good, but we can do in decorator too, 
    # # response.status_code = status.HTTP_201_CREATED

    # DO not use this, as this is open to SQL injection attacks
    # cursor.execute (f"INSERT INTO posts (title, content, published)"
    #                 f"VALUES('{post.title}', '{post.content}', {post.published})")

    # USE this method

    # cursor.execute("""INSERT INTO posts(title, content, published) 
    #                VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    
    # created_post = cursor.fetchone()
    
    # conn.commit()

    #created_post = models.Post(title = post.title, content = post.content, published = post.published)

    # instead of the above, we can also use :
    created_post = models.Post(**post.model_dump()) #which unpacks a dictionary

    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    return {"post_data" : created_post}



def find_by_id (id: int) :
    for post in all_posts :
        if post["id"] == id :
            return post
    
    return None

@app.get("/posts/{id}")         # 'id' is a path parameter
def get_post_by_id (id: int, db: Session = Depends(get_db)) :  # add this to use hardcode resp -> (resp: Response)
    
    # cursor.execute ("""SELECT * FROM posts where id = %s""", (str(id)))
    # post = cursor.fetchone()

    # post = find_by_id (id)

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND, 
                         detail= f"post with id : {id} not found")
        

    ''' The below is like hardcoding

    resp.status_code = status.HTTP_404_NOT_FOUND
    return {"detail": f"post with id : {id} not found"}

    '''

    return {"detail" : post}
    

### DELETE Requests ####

def find_post(id: int):
    for i, p in enumerate(all_posts):
        if id == p['id']:
            return i
    return None

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session = Depends(get_db)):

    # cursor.execute ("""DELETE FROM posts where id = %s RETURNING *""", (str(id)))
    # post_idx = cursor.fetchone()  

    # conn.commit() 

    post_idx = db.query(models.Post).filter(models.Post.id == id)



    # post_idx = find_post(id)

    if post_idx.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found, 404"
        )

    # all_posts.pop(post_idx)

    post_idx.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


### UPDATE/PUT Requests ###

@app.put("/posts/{id}", status_code = status.HTTP_200_OK)
def update_by_id (id: int, post: PostBody, db: Session = Depends(get_db)) :
    # post_idx = find_post(id)

    # cursor.execute ("""UPDATE posts SET title = %s, content = %s,
    #                 published = %s where id = %s RETURNING *""", 
    #                 (post.title, post.content, post.published, str(id)))

    # post_idx = cursor.fetchone()

    # conn.commit()

    post_idx = db.query(models.Post).filter(models.Post.id == id)

    if post_idx.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found, 404"
        )

    # dict_post = post.model_dump()

    # dict_post['id'] = id
    # all_posts[post_idx] = dict_post

    post_idx.update(post.model_dump(), synchronize_session = False)
    db.commit()

    return {"new post is udpated as: " : post_idx.first()}