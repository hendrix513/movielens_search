import io
import os
import zipfile

import flask
import pymysql
import requests
from flask import request

TMP_DIR = '/tmp'

app = flask.Flask(__name__)
db = pymysql.connect(
    user="root",
    password="testpass",
    host="db",
    database="challenge",
    local_infile="challenge"
)

'''
The application can
support basic keyword queries, and support filtering such as by user id/name,
movie id/name, and movie tags
'''
@app.route("/search_movies")
def search_movies():
    request_args = request.args
    title = request_args.get('title')
    genre = request_args.get('genre')
    tag = request_args.get('tag')
    tag_user_id = request_args.get('tag_user_id')
    rating_user_id = request_args.get('rating_user_id')
    movie_id = request_args.get('movie_id')

    limit = int(request_args.get('limit'))
    page = int(request_args.get('page'))

    where_clauses = []
    from_clause = 'movies m left outer join ratings r on m.movieId=r.movieId left outer' \
                  ' join links l on l.movieId=m.movieId'

    if tag_user_id or tag:
        from_clause = '{} {}'.format(from_clause, ' join tags t on t.movieId=m.movieId')

        if tag_user_id:
            where_clauses.append('t.userId={}'.format(tag_user_id))

        if tag:
            where_clauses.append('t.tag=\'{}\''.format(tag))

    if rating_user_id:
        where_clauses.append('m.movieId in (SELECT DISTINCT'
                             ' m.movieId FROM movies m join ratings'
                             ' r ON m.movieId=r.movieId WHERE r.userId={})'.format(rating_user_id))

    if title:
        where_clauses.append('m.title like \'%{}%\''.format(title))

    if genre:
        where_clauses.append('m.genres like \'%{}%\''.format(genre))

    if movie_id:
        where_clauses.append('m.movieId={}'.format(movie_id))

    where_clause = ' WHERE {}'.format(' AND '.join(where_clauses)) if where_clauses else ''
    query = 'SELECT m.title, m.genres, AVG(r.rating), l.imdbId, l.tmdbId FROM {}{} GROUP BY' \
            ' m.movieId ORDER BY m.movieId ASC LIMIT {} OFFSET {}'.format(from_clause, where_clause,
                                                   limit, (page-1)*limit)

    with db.cursor() as cur:
        cur.execute(query)
        return flask.jsonify(
            {'data':
                 [[title, genres.strip().split('|'), float(avg_rating) if avg_rating else None,
                   'www.imdb.com/title/{}'.format(imdb_id) if imdb_id else None,
                   'www.themoviedb.org/movie/{}'.format(tmdb_id) if tmdb_id else None]
                  for title, genres, avg_rating, imdb_id, tmdb_id in cur.fetchall()]})


@app.cli.command("load-movielens")
def load_movielens():
    r = requests.get("http://files.grouplens.org/datasets/movielens/ml-latest-small.zip")
    assert r.ok

    with db.cursor() as cur:
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            for filename in z.namelist():
                sp = filename.rsplit('.csv', 1)
                if len(sp) != 2:
                    continue
                table_name = os.path.basename(sp[0])

                z.extract(filename, TMP_DIR)
                s = 'LOAD DATA LOCAL INFILE  \'{}\' into table {}' \
                    ' fields terminated by \',\' IGNORE 1 LINES'.format(
                    os.path.join(TMP_DIR, filename), table_name)
                cur.execute(s)
        db.commit()

