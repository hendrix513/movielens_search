import os
import tempfile

import pytest

from .app import app, db


@pytest.fixture
def client():
    print(app, dir(app))
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
        cur.execute('INSERT INTO movies VALUES (1, \'movie 1\', \'romance|horror\')')
        cur.execute('INSERT INTO movies VALUES (2, \'movie 2\', \'romance|horror\')')
        cur.execute('INSERT INTO movies VALUES (3, \'movie 3\', \'romance|horror\')')

        cur.execute('INSERT INTO links VALUES (1, 101, 201)')
        cur.execute('INSERT INTO links VALUES (2, 102, 202)')
        cur.execute('INSERT INTO links VALUES (3, 103, 203)')

        cur.execute('INSERT INTO tags VALUES (1, 101, 201)')
        cur.execute('INSERT INTO links VALUES (2, 102, 202)')
        cur.execute('INSERT INTO links VALUES (3, 103, 203)')


        db.commit()


def test_search(client, load_data):
    with db.cursor() as cur:
        cur.execute('SELECT COUNT(*) FROM movies')
        print(cur.fetchall())
        db.commit()

    d = client.get('/search_movies?limit=10&page=1')
    print(d)
    print(d.data)
