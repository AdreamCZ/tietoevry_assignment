from flask import Flask, request, jsonify, abort, json
from werkzeug.exceptions import HTTPException
from collections import OrderedDict
# Use of OrderedDict is probably not necessary
# I use it so the outputed JSONs are identical to the examples given in the assignment
import sqlite3

# Connect to ( and possibly create ) the database
def connect_to_db():
    conn = sqlite3.connect('movies.db')
    return conn

# Create new table in the db ( If it doesn't already exist )
def create_movies_table():
    conn = connect_to_db()
    conn.execute('''
            CREATE TABLE IF NOT EXISTS movie
                (
                    id              INTEGER PRIMARY KEY NOT NULL,
                    title           TEXT,
                    description     TEXT,
                    release_year    INTEGER
                );
    ''')
    conn.commit()
    conn.close()

def convert_row_to_movie_dict(r):
    if r is None:
        return {}

    movie = OrderedDict() 
    movie["id"]          = r["id"]
    movie["title"]       = r["title"]
    movie["description"] = r["description"]
    movie["release_year"]= r["release_year"]
    return movie

#Returns list of all the movies in the DB
def get_all_movies():
    movies = []
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM movie")
    rows = cur.fetchall()
    #Convert row objects to list of dictionaries
    for r in rows:
        movie = convert_row_to_movie_dict(r)
        movies.append(movie)
    conn.close()
    return movies

#Return movie with specified id
def get_movie_by_id(movie_id):
    movie = OrderedDict()
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM movie WHERE id = ?", str(movie_id) )
    row = cur.fetchone()
    conn.close()
    return convert_row_to_movie_dict(row)

#Insert a new movie into the DB
def insert_movie(movie):
    try:
        year = int(movie["release_year"])
        if year < 0:
            abort(400)
    except:
        abort(400)        
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO movie (title, description, release_year) VALUES (?, ?, ?)
    ''', (movie["title"], movie["description"], movie["release_year"]))
    conn.commit()
    conn.close()
    return get_movie_by_id(cur.lastrowid)

#Updates existing movie
def update_movie(movie):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('''
        UPDATE movie SET title = ?, description = ?, release_year = ? WHERE id = ?''', 
        (movie["title"], movie["description"], movie["release_year"], movie["id"])
    )
    conn.commit()
    conn.close()
    return get_movie_by_id(movie["id"])

# REST API implementation :
app = Flask(__name__)

# Return JSON instead of HTML for HTTP errors.
@app.errorhandler(HTTPException)
def handle_exception(e):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route('/movies', methods=['GET'])
def api_get_all_movies():
    return jsonify(get_all_movies())

@app.route('/movies/<id>', methods=['GET'])
def api_get_movie(id):
    movie = get_movie_by_id(id)
    if movie == {}:
        abort(404)
    return jsonify(movie)

@app.route('/movies', methods=["POST"])
def api_create_movie():
    movie = request.get_json()
    return jsonify(insert_movie(movie))

@app.route('/movies/<id>', methods=['PUT'])
def api_update_movie(id):
    movie = request.get_json()
    movie["id"] = id
    return jsonify(update_movie(movie))
    
if __name__ == '__main__':
    create_movies_table()
    app.config['JSON_SORT_KEYS'] = False
    app.run(host="0.0.0.0")