from flask import Flask
from flask import request
from flask import jsonify
# from flaskext.mysql import MySQL
import MySQLdb

app = Flask(__name__)

db = MySQLdb.connect(host="localhost",  # your host
                     user="root",       # username
                     passwd="",     # password
                     db="Clothes")   # name of the database

cursor = db.cursor()

@app.route('/clothes/term/<search_term>')
def get_clothes_by_term(search_term):
    query = get_mysql_like_clause_from_search_term('image_title', search_term)
    cursor.execute(query)
    a = {}
    for row in cursor.fetchall():
        a[row[1]] = {'id': row[1], 'image_link': row[2], 'image_title': row[3], 'source_link': row[4]}
    return jsonify(a)


@app.route('/clothes/id/<clothes_id>')
def get_clothes_by_id(clothes_id):
    query = get_mysql_clause_from_id_search(clothes_id)
    print(query)
    cursor.execute(query)
    a = {}
    for row in cursor.fetchall():
        a[row[1]] = {'id': row[1], 'image_link': row[2], 'image_title': row[3], 'source_link': row[4]}
    return jsonify(a)

@app.route('/clothes', methods=['POST'])
def post_ids_to_model():
    clothesId = request.data
    return jsonify(clothesId['ids'])


def get_mysql_clause_from_id_search(ids):
    final_sql = 'select * from Clothes where'
    for term in ids.split(' '):
        sql_wrapper = " id=" + term + " or "
        final_sql += sql_wrapper

    final_sql = final_sql[:-3] + ';'
    return final_sql


def get_mysql_like_clause_from_search_term(search_type, search_term):
    final_sql = 'select * from Clothes where'
    for term in search_term.split(' '):
        sql_wrapper = " image_title like '%" + term + "%' and "
        final_sql += sql_wrapper

    print(final_sql)
    final_sql = final_sql[:-5] + ';'
    return final_sql


if __name__ == '__main__':
    app.run(debug=True)