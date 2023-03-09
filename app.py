import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for

db = "database.db"

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
  if request.method == 'POST':
    url = request.form['url']
    if not url:
      # flash('The URL is required!')
      return redirect(url_for('index'))

    with sqlite3.connect(db) as con:
      cur = con.cursor()
      url_data = cur.execute('INSERT INTO urls (original_url) VALUES (?)', (url,))
      con.commit()

    url_id = url_data.lastrowid
    short_url = request.host_url + str(url_id)

    return render_template('index.html', short_url=short_url)

  return render_template('index.html')


@app.route('/<id>')
def url_redirect(id):
  with sqlite3.connect(db) as con:
    cur = con.cursor()
    cur.execute('SELECT original_url, clicks FROM urls'
                                ' WHERE id = (?)', (id,)
                                )
    url_data = cur.fetchone()
    print(url_data)
    original_url, clicks = url_data

    cur.execute('UPDATE urls SET clicks = ? WHERE id = ?', (clicks+1, id))
    con.commit()
  return redirect(f"http://{original_url}")

@app.route('/stats')
def stats():
  with sqlite3.connect(db) as con:
    cur = con.cursor()
    db_urls = cur.execute('SELECT id, created, original_url, clicks FROM urls'
                           )
    db_urls = cur.fetchall()
  urls = []
  for urli in db_urls:
    url = {}
    url['id'], url['created'], url['original_url'], url['clicks'] = urli
    url['short_url'] = request.host_url + str(url['id'])
    urls.append(url)

  return render_template('stats.html', urls=urls)

if __name__ == '__main__':
  app.run()