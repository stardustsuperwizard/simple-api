import json
import sqlite3

from flask import Flask, jsonify, request
from querybuilder import query_builder

app = Flask(__name__)

DB = "instance/data.sqlite"


#CORS Response
def _corsify_response(response):
    response.headers.add("Access-Controls-Allow-Origin","*")

@app.route('/')
@app.route('/index')
def index():
    return "Please use \"/api/records/\" and then a table name (such as \"nba_elo\") to get started."


@app.route('/api/records')
@app.route('/api/records/')
def get_api_records():
    message = "Please enter a table name in the address bar."
    return jsonify({ 'code': 200, 'message': message, 'status': 'success', 'data': [] }), 200


@app.route('/api/records/<string:table_name>')
@app.route('/api/records/<string:table_name>/') # Firefox adds a "/" at the end of URL
def get_api_records_table(table_name):
    data = []
    message = "All records available"
    status = "normal"
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    results = None
    parameters = []
    if not request.args:
        query = f'''SELECT * FROM {table_name}'''
    else:
        query = f"SELECT * FROM {table_name} WHERE"
        parameters, query = query_builder(request.args, parameters, query, table_name)

    try:
        results = c.execute(query, tuple(parameters)).fetchall()
        if results:
            data = [dict(i) for i in results]
            status = "success"
            code = 200
        else:
            message = f"Your query did not return any results."
            status = "not found"
            code = 404
    except sqlite3.OperationalError as err:
        message = str(err)
        status = "error"
        code = 400
    
    return jsonify({ 'code': code, 'message': message, 'status': status, 'data': data }), code


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)