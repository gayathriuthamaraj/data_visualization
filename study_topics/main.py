from fastapi import FastAPI
from pydantic import BaseModel
import crud

app = FastAPI()

items = []

class Review(BaseModel):
    id: int
    content: str
    score: int

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/reviews")
def review_print():
    return items

@app.get("/hello")
def hello(name: str = "May"):
    return {"message" : f"Hello {name}"}

@app.post("/reviews")
def post_review(review: Review):
    items.append(review)
    return "review posted"