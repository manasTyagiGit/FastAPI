from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from random import randrange
# for schema validation
from pydantic import BaseModel

app = FastAPI()

# class for extension of BaseModel
class PostBody (BaseModel) :
    title: str
    content: str
    #Defaultable optional
    published: bool = True
    #Truly Optional
    rating: Optional[int] = None

#Storing posts here, i.e., a list of dictionaries
all_posts = [{"title": "title of post 1", "content": "content of post 1", "id" : 1},
             {"title": "title of post 2", "content": "content of post 2", "id" : 2}
            ]


@app.get("/")
def first_api() :
    return {"Hello" : "Welcome to my first api!"}

@app.get("/posts")
def get_posts() :
    return {"Hey user, posts are" : all_posts}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: PostBody) :

    post_dict = post.model_dump()
    
    post_dict['id'] = randrange (0, 10000000)

    all_posts.append(post_dict)

    # This is good, but we can do in decorator too, 
    # response.status_code = status.HTTP_201_CREATED

    return {"post_data" : post_dict}



def find_by_id (id: int) :
    for post in all_posts :
        if post["id"] == id :
            return post
    
    return None

@app.get("/posts/{id}")         # 'id' is a path parameter
def get_post_by_id (id: int) :  # add this to use hardcode resp -> (resp: Response) 
    post = find_by_id (id)

    if post != None:
        return {"detail" : post}

    ''' The below is like hardcoding

    resp.status_code = status.HTTP_404_NOT_FOUND
    return {"detail": f"post with id : {id} not found"}

    '''
    raise HTTPException (status_code= status.HTTP_404_NOT_FOUND, 
                         detail= f"post with id : {id} not found")

### DELETE Requests ####

def find_post(id: int):
    for i, p in enumerate(all_posts):
        if id == p['id']:
            return i
    return None

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int):
    post_idx = find_post(id)

    if post_idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found, 404"
        )

    all_posts.pop(post_idx)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


### UPDATE/PUT Requests ###

@app.put("/posts/{id}", status_code = status.HTTP_200_OK)
def update_by_id (id: int, post: PostBody) :
    post_idx = find_post(id)

    if post_idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found, 404"
        )

    dict_post = post.model_dump()

    dict_post['id'] = id
    all_posts[post_idx] = dict_post

    return {"new post is udpated as: " : dict_post}