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
def index():
    connection = get_db_connection()

    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        
        url_data = connection.execute('INSERT INTO urls (original_url) VALUES (?)', (url,))
        connection.commit()
        connection.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        hash_url = request.host_url + hashid

        return render_template('index.html', hash_url=hash_url)

    return render_template('index.html')

@app.route("/<hash>")
def url_redirect(hash):
    connection = get_db_connection()

    id = hashids.decode(hash)
    if id:
        id = id[0]
        url_data = connection.execute('SELECT original_url, clicks FROM urls'' WHERE id = (?)', (id,)).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']

        connection.execute('UPDATE urls SET clicks = ? WHERE id = ?', (clicks + 1, id))
        connection.commit()
        connection.close()
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

@app.route("/stats")
def stats():
    connection = get_db_connection()
    db_urls = connection.execute('SELECT id, created, original_url, clicks, FROM urls').fetchall()
    connection.close()

    urls = []
    for url in db_urls:
        url = dict(url)
        url['hash_url'] = request.host_ur. + hashids.encode(url['id'])
        urls.append(url)
    
    return render_template('stats.html', urls=urls)

if __name__ == "__main__":
    app.run(debug=True)