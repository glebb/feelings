import sqlite3
from flask import g

from feelings import app

DATABASE = 'feelings.sqlite'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
        
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    r_value = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (r_value[0] if r_value else None) if one else r_value        

def save_db():
    g.db.commit()

def get_averages(cat):
    query = "select date, AVG(feeling) as feelingavg, group_concat(comment) \
        as comments, count(*) as votes from feelings"
    args = []
    if cat:
        query = query + " WHERE category LIKE ?"
        args.append(cat)
    query = query + " group by date order by date"
    return query_db(query, args)
    