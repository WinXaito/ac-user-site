from flask import g, current_app as app
from os import path as ospath
import sqlite3

APP_ROOT = ospath.dirname(__file__)
DATABASE = '{}/../database.db'.format(APP_ROOT)


def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row

    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert(table, fields=(), values=()):
    # g.db is the database connection
    cur = get_db().cursor()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    get_db().commit()
    id = cur.lastrowid
    cur.close()
    return id


def delete(table, where, value):
    cur = get_db().cursor()
    query = 'DELETE FROM %s WHERE %s = %s' % (
        table,
        where,
        value
    )
    cur.execute(query)
    get_db().commit()



def init_db():
    print('Initialisation de la base de données')
    open(DATABASE, 'a').close()

    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            print('Schema')
        db.commit()
