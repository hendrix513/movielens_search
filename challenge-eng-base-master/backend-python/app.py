import io
import os
import zipfile

import flask
import pymysql
import requests

TMP_DIR = '/tmp'

app = flask.Flask(__name__)
db = pymysql.connect(
    user="root",
    password="testpass",
    host="db",
    database="challenge",
)


@app.route("/test")
def test():
    with db.cursor() as cur:
        cur.execute("SELECT col FROM test;")
        (result,) = cur.fetchone()
        return flask.jsonify(dict(result=result, backend="python"))


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

                cur.execute('SELECT * FROM {} LIMIT 10'.format(table_name))
