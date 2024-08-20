from functools import lru_cache
from flask import Flask
from redis import Redis

app = Flask(__name__)

@app.get("/")
def index():
    page_views = get_redis().incr("page_views")
    return f"This page has been seen {page_views} times."

@lru_cache(maxsize=None)
def get_redis():
    return Redis()
