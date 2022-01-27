from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
import models
from db import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host='******', database='fastapi',
                                user='postgres', password='******', cursor_factory=RealDictCursor)

        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print('DB connection was successfull!')
        break
    except Exception as error:
        print('Connection to DB failed')
        print("Error: ", error)
        time.sleep(2)

        # Execute a query
        # cur.execute("SELECT * FROM my_data")

# setting up the schema that API should recieve.  using pydantic models


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # by default set to true
    # rating: Optional[int] = None


my_posts = [{"title": "title of the first post",
             "content": "content of the first post", "id": 1}, {
                 "title": "Favorite car", "content": "My favorite car is BMW & Tesla", "id": 2}]


@app.get('/')
def root():
    return {"message": "Hello World!!!"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


# Getting all posts
@app.get('/mypost')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    # FastAPI automatically serialize the array (turn to JSON)
    return {'data': posts}

# Creating a post


@app.post('/posts', status_code=status.HTTP_201_CREATED)
# gets all the fields from Body, stores it in dictionary and stores it in payload
def create_post(post: Post):
    # execute SQL command
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    # fetch the data
    new_post = cursor.fetchone()
    # to save to DB need to commit
    conn.commit()
    return {"data": new_post}


@app.get('/posts/{id}')
# converts to integer so no need convert in future and validation so only int can be passed as a param.
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        # more cleaner version
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}


def findPostIdex(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# Delete a post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, response: Response):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def updatePost(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return {"data": updated_post}
