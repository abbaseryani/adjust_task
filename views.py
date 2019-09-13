import sqlite3
import pandas as pd
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

data = {
        "date": [],
        "channel": [],
        "country": [],
        "os": [],
        "impressions": [],
        "clicks": [],
        "installs": [],
        "spend": [],
        "revenue": []
      }


@app.route('/', methods=['GET'])
def home():
    return "<h1>HELLO ADJUST PEOPLE :)<h1>"


@app.route('/performance-api', methods=["GET"])
def performance_api():
    select = str(request.args.getlist("select")[0])
    table_name = 'performance '
    where = str(request.args.getlist("where")[0])
    group_by = str(request.args.getlist("groupby")[0])
    try:
        order_by = str(request.args.getlist("orderby")[0])
    except:
        order_by = None
    conn = sqlite3.connect('dataset')
    result = check_table(conn)
    if result is None:
        create_table(conn)

    qry = '''
            SELECT 
          '''
    qry += select
    qry += " FROM "
    qry += table_name
    qry += "where "
    qry += where
    qry += "\n"
    qry += "group by "
    qry += group_by
    if order_by is not None:
        qry += " order by "
        qry += order_by

    result = conn.execute(qry).fetchall()

    for row in result:
        data["channel"].append(row[0])
        data["country"].append(row[1])
        data["impressions"].append(row[2])
        data["clicks"].append(row[3])
    conn.close()

    return "{'success': True, 'result': %s }" % data, 200, \
           {'ContentType': 'application/json'}


def check_table(conn):
    qry = '''
            SELECT name from sqlite_master
            WHERE type='table' AND name = 'performance'
          '''
    try:
        result = conn.execute(qry).fetchone()[0]
    except:
        result = None

    return result


def create_table(conn):
    df = pd.read_csv("dataset.csv", index_col=None)

    conn.execute('''
                CREATE TABLE performance
                (
                    date DATE,
                    channel text,
                    country text,
                    os text,
                    impressions integer,
                    clicks integer,
                    installs integer,
                    spend float,
                    revenue float
                )
                ''')
    df.to_sql('performance', conn, if_exists='append', index=False)
    conn.commit()


app.run()
