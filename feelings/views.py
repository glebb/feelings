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
    resp = database.query_db('select * from feelings')
    return render_template('data.html', data=resp)

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
    return render_template('index.html', cat='test')