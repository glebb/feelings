from flask import render_template
from flask import jsonify
from flask import request
import datetime

from feelings import app
from feelings import database
from feelings import custom_views

@app.route('/_clear_data')
def clear_data():
    database.query_db('DELETE FROM feelings')
    database.save_db()
    return show_data()
    
@app.route('/show_data')
def show_data():
    cat = request.args.get('category')
    query = "select * from feelings"
    args = []
    if cat:
        query = query + " WHERE category LIKE ?"
        args.append(cat)
    query = query + " order by date"
    resp = database.query_db(query, args)
    return render_template('data.html', data=resp)

@app.route('/show_avg')
def show_avg():
    cat = request.args.get('category')
    query = "select date, AVG(feeling) as feelingavg, group_concat(comment) as comments, count(*) as votes from feelings"
    args = []
    if cat:
        query = query + " WHERE category LIKE ?"
        args.append(cat)
    query = query + " group by date order by date"
    resp = database.query_db(query, args)
    return render_template('data_avg.html', data=resp)
    

@app.route('/thanks', methods=['POST'])
def add_entry():
    today = datetime.date.today()
    query = 'insert into feelings (date, feeling, category, comment) values (?, ?, ?, ?)'
    args = [today, int(request.form['feeling']),
            request.form['category'],
            request.form['comment']]
    
    database.query_db(query, args)
    database.save_db()
    return render_template('thanks.html')

@app.route('/')
def index():
    category = request.args.get('category')
    if not category:
        category = 'test'
    return render_template('index.html', cat=category)

