from flask import render_template
from flask import jsonify
from flask import request
from flask import send_from_directory
from flask import make_response
import os
import datetime

from feelings import app
from feelings import database

from graphs import create_graph

DEFAULT_CATEGORY = 'test'

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

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

@app.route('/json_data')
def json_data():
    cat = request.args.get('category')
    query = "select date, group_concat(feeling) as feelings from feelings"
    args = []
    if cat:
        query = query + " WHERE category LIKE ?"
        args.append(cat)
    query = query + " group by date order by date ASC, feeling DESC"
    resp = database.query_db(query, args)
    for r in resp:
        r['feelings'] = r['feelings'].split(',') 
    return jsonify(data=resp)

    
@app.route('/nikoniko')
def nikoniko():
    return render_template('nikoniko.html')


@app.route('/show_avg')
def show_avg():
    resp = database.get_averages(request.args.get('category'))
    return render_template('data_avg.html', data=resp)

@app.route('/show_graph')
def show_graph():
    category = request.args.get('category')
    resp = database.get_averages(category)
    if not category:
        category = DEFAULT_CATEGORY
    return render_template('data_graph.html', data=resp, category=category)


@app.route('/thanks', methods=['POST'])
def add_entry():
    today = datetime.date.today()
    query = 'insert into feelings (date, feeling, category, comment) values (?, ?, ?, ?)'
    args = [today, int(request.form['feeling']),
            request.form['category'],
            request.form['comment']]
    
    database.query_db(query, args)
    database.save_db()
    return render_template('thanks.html', category=request.form['category'])

@app.route('/')
def index():
    category = request.args.get('category')
    if not category:
        category = DEFAULT_CATEGORY
    return render_template('index.html', cat=category, today=datetime.date.today().strftime('%d.%m.%Y'))

@app.route("/<category>/graph.png")
def simple(category):
    cat = category
    resp = database.get_averages(cat)
    png = create_graph(resp, cat)
    if png:
        response=make_response(png)
        response.headers['Content-Type'] = 'image/png'
        return response
    else:
        return "No data for: " + cat

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')
        