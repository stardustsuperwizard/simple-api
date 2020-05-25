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
    return 'Hello world!'

@app.route('/api/records')
@app.route('/api/records/')
def get_api_records():
    data = []
    message = "All records available"
    status = "normal"
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    results = None
    parameters = []
    if not request.args:
        query = '''SELECT * FROM nba_elo'''
    else:
        query = "SELECT * FROM nba_elo WHERE"
        parameters, query = query_builder(request.args, parameters, query, 'nba_elo')

    results = c.execute(query, tuple(parameters)).fetchall()
    if results:
        data = [dict(i) for i in results]
        status = "success"
        code = 200
    
    return jsonify({ 'code': code, 'message': message, 'status': status, 'data': data }), code


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)