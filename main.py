from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def first_api() :
    return {"Hello" : "Welcome to my first api!"}

@app.get("/getposts")
def get_posts() :
    return {"Hey user_name" : "These are your posts"}