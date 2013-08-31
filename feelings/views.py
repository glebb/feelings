from flask import render_template
from flask import jsonify
from flask import request
from flask import send_from_directory
from flask import make_response
import os
import datetime
import calendar

from feelings import app
from feelings import database

DEFAULT_CATEGORY = 'test'
ALL = '_all_'

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
            'favicon.ico', mimetype = 'image/vnd.microsoft.icon')        

@app.route('/_clear_data')
def clear_data():
    database.query_db('DELETE FROM feelings')
    database.save_db()
    return show_data()
    
@app.route('/_show_data')
def show_data():
    cat = request.args.get('category')
    query = "select * from feelings"
    args = []
    if cat:
        query = query + " WHERE category LIKE ?"
        args.append(cat)
    query = query + " order by date"
    resp = database.query_db(query, args)
    return render_template('data.html', data = resp)

@app.route('/')
def index():
    category = request.args.get('category')
    if not category:
        category = DEFAULT_CATEGORY
    return render_template('index.html', cat = category, today = datetime.date.today().strftime('%d.%m.%Y'))

@app.route('/show_avg')
def show_avg():
    resp = database.get_averages(request.args.get('category'))
    return render_template('data_avg.html', data = resp)

@app.route('/results')
def results():
    return render_template('results.html', category = request.args.get('category'))

@app.route('/thanks', methods = ['POST'])
def add_entry():
    today = datetime.date.today()
    query = 'insert into feelings (date, feeling, category, comment) values (?, ?, ?, ?)'
    args = [today, int(request.form['feeling']),
            request.form['category'],
            request.form['comment']]
    
    database.query_db(query, args)
    database.save_db()
    return render_template('thanks.html', category = request.form['category'])


@app.route('/json_nikoniko_data')
def json_data():
    cat = request.args.get('category')
    args = []

    query = "select date, group_concat(feeling) as feelings from feelings"
    if cat:
        query = query + " WHERE category LIKE ?"
        args.append(cat)
    
    query = query + " group by date order by date ASC"
    resp = database.query_db(query, args)
    for row in resp:
        temp = []
        date_from_data = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
        temp.append(calendar.timegm(date_from_data.timetuple()) * 1000)
        row['feelings'] = row['feelings'].split(',')
        row['feelings'].sort() 
    return jsonify(data = resp[-20:])

@app.route('/json_graph_data')
def create_javascript_graph():
    category = request.args.get('category')
    resp = database.get_averages(category)

    results = []
    for row in resp:
        temp = []
        temp.append(_convert_to_javascript_timestamp(row['date']))
        temp.append(row['feelingavg'])
        results.append(temp)
    return jsonify(data = results[-20:])

def _convert_to_javascript_timestamp(date):
    date_from_data = datetime.datetime.strptime(date, '%Y-%m-%d')
    return calendar.timegm(date_from_data.timetuple()) * 1000
