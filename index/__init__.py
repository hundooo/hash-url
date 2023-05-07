import sqlite3
import pypyodbc as odbc
import azure.functions as func
from uuid import uuid4
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().hex
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

username = 'azureuser'
password = 'userAzure!'
server = 'hash-url.database.windows.net'
database = 'hash-urls-database'
connection_string = 'DRIVER={ODBC Driver 18 for SQL server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO urls (original_url) VALUES (?)', (url,))
        conn.commit()

        url_id = cursor.rowcount
        hashid = hashids.encode(url_id)
        hash_url = request.host_url + hashid

        return render_template('index.html', hash_url=hash_url)

    return render_template('index.html')

@app.route("/<hash>")
def url_redirect(hash):
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    id = hashids.decode(hash)
    if id:
        id = id[0]
        url_data = cursor.execute('SELECT original_url, clicks FROM urls'' WHERE id = (?)', (id,)).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']

        cursor.execute('UPDATE urls SET clicks = ? WHERE id = ?', (clicks + 1, id))
        conn.commit()
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

@app.route("/stats")
def stats():
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    
    db_urls = cursor.execute('SELECT id, created, original_url, clicks FROM urls').fetchall()

    urls = []
    for url in db_urls:
        url = dict(url)
        url['hash_url'] = request.host_url + hashids.encode(url['id'])
        urls.append(url)
    
    return render_template('stats.html', urls=urls)