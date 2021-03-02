import json
import os
import tempfile

import pytest

from .app import app, db


@pytest.fixture
def client():
    #print(app, dir(app))
    #db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        #with app.app_context():
            #app.init_db()
        #print(app.config.database)
        yield client

    #os.close(db_fd)
    #os.unlink(app.config['DATABASE'])


@pytest.fixture
def load_data():
    with db.cursor() as cur:
        cur.execute('TRUNCATE movies')
        cur.execute('TRUNCATE links')
        cur.execute('TRUNCATE tags')
        cur.execute('TRUNCATE ratings')

        cur.execute('INSERT INTO movies VALUES (1, \'movie1\', \'drama|romance\r\')')
        cur.execute('INSERT INTO movies VALUES (2, \'movie2\', \'romance|horror\r\')')
        cur.execute('INSERT INTO movies VALUES (3, \'movie3\', \'comedy\r\')')
        cur.execute('INSERT INTO movies VALUES (4, \'movie4\', \'thriller\')')

        cur.execute('INSERT INTO links VALUES (1, 101, 201)')
        cur.execute('INSERT INTO links VALUES (2, 102, 202)')
        cur.execute('INSERT INTO links VALUES (3, 103, 203)')

        cur.execute('INSERT INTO tags VALUES (1, 1, \'tag1\', 0)')
        cur.execute('INSERT INTO tags VALUES (2, 3, \'tag1\', 0)')
        cur.execute('INSERT INTO tags VALUES (1, 2, \'tag2\', 0)')

        cur.execute('INSERT INTO ratings VALUES (1, 1, 7, 0)')
        cur.execute('INSERT INTO ratings VALUES (1, 1, 9, 0)')
        cur.execute('INSERT INTO ratings VALUES (2, 3, 6, 0)')

        db.commit()


def test_search(client, load_data):
    movies_exp_return = [['movie1', ['drama', 'romance'], 8.0, 'www.imdb.com/title/101', 'www.themoviedb.org/movie/201'],
                         ['movie2', ['romance', 'horror'], None, 'www.imdb.com/title/102', 'www.themoviedb.org/movie/202'],
                         ['movie3', ['comedy'], 6.0, 'www.imdb.com/title/103', 'www.themoviedb.org/movie/203'],
                         ['movie4', ['thriller'], None, None, None]
                         ]

    d = client.get('/search_movies?limit=2&page=1')
    data = json.loads(d.data)['data']
    assert data == movies_exp_return[:2]

    d = client.get('/search_movies?limit=2&page=2')
    data = json.loads(d.data)['data']
    assert data == movies_exp_return[2:]

    d = client.get('/search_movies?limit=10&page=1&movie_id=1')
    data = json.loads(d.data)['data']
    assert data == [movies_exp_return[0]]

    d = client.get('/search_movies?limit=10&page=1&genre=romance')
    data = json.loads(d.data)['data']
    assert data == movies_exp_return[:2]

    d = client.get('/search_movies?limit=10&page=1&genre=romance&title=ie2')
    data = json.loads(d.data)['data']
    assert data == [movies_exp_return[1]]

    d = client.get('/search_movies?limit=10&page=1&tag=tag1')
    data = json.loads(d.data)['data']
    assert data == [movies_exp_return[0], movies_exp_return[2]]

    d = client.get('/search_movies?limit=10&page=1&tag_user_id=1')
    data = json.loads(d.data)['data']
    assert data == movies_exp_return[:2]

    d = client.get('/search_movies?limit=10&page=1&rating_user_id=2')
    data = json.loads(d.data)['data']
    assert data == [movies_exp_return[2]]

