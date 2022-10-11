import sqlite3
from uuid import uuid4
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().hex

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

@app.route("/", methods=('GET', 'POST'))
def hash_url():
    connection = get_db_connection()

    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        
        url_data = connection.execute('INSERT INTO urls (original_rl) VALUES (?)', (url,))
        connection.commit()
        connection.close()

        

    return render_template('index.html')