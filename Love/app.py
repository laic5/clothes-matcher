from flask import Flask
from flask import request
from flask import jsonify
import MySQLdb
import numpy as np
import pandas as pd
import pickle

from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

db = MySQLdb.connect(host="localhost",  # your host
                     user="root",       # username
                     passwd="",     # password
                     db="Clothes")   # name of the database

cursor = db.cursor()

PICKLED_FILE = 'google1937.p'

with open(PICKLED_FILE, 'rb') as pickle_file:
    content = pickle.load(pickle_file)

google_cnn_output = pd.DataFrame(content)

@app.route('/clothes/term/<search_term>')
def get_clothes_by_term(search_term):
    query = get_mysql_like_clause_from_search_term(search_term)
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
    l = []
    user_selected_ids = request.form
    print(user_selected_ids)
    output = get_top_k_indices(google_cnn_output, user_selected_ids, 20)
    print(output)
    return get_clothes_by_id(output)
    # return jsonify(output['ids'])


def get_mysql_clause_from_id_search(ids):
    final_sql = 'select * from Clothes where'
    for term in ids:
        print(term)
        term = str(term)
        sql_wrapper = " id=" + term + " or "
        final_sql += sql_wrapper

    final_sql = final_sql[:-3] + ';'
    return final_sql


def get_mysql_like_clause_from_search_term(search_term):
    final_sql = 'select * from Clothes where'
    for term in search_term.split(' '):
        sql_wrapper = " image_title like '%" + term + "%' and "
        final_sql += sql_wrapper

    print(final_sql)
    final_sql = final_sql[:-5] + ';;'
    return final_sql



def get_top_k_indices(google_cnn_output, user_selected_ids, k):
    '''
    NOTE: user_selected_imgs NEEDS TO BE A LIST! Even if it's only 1 item.
    It does not handle 0 items at this moment.

    Both google_cnn_output and user_selected_imgs are output from the CNN and a np.array
    '''

    user_selected_imgs = google_cnn_output.loc[user_selected_ids]

    if len(google_cnn_output.shape) == 1:
        google_cnn_output = google_cnn_output.reshape(1, -1)
    if len(user_selected_imgs.shape) == 1:
        user_selected_imgs = user_selected_imgs.reshape(1, -1)

    similarity_results = np.zeros((len(user_selected_imgs), len(google_cnn_output)))

    # for idx, img in enumerate(user_selected_imgs):
    #    print(img.shape)
    #    similarity_results[idx,:] = cosine_similarity(img.reshape(1, -1), google_cnn_output)

    for i in range(len(user_selected_ids)):
        similarity_results[i, :] = cosine_similarity(user_selected_imgs.iloc[i, :].reshape(1, -1), google_cnn_output)

    if similarity_results.shape[0] == 1:
        sorted_indices = np.argsort(similarity_results[0])

    else:
        means = np.mean(similarity_results, axis=0)
        sorted_indices = np.argsort(means)

    if k > len(google_cnn_output):
        return (sorted_indices)

    top_indices = sorted_indices[-k:]

    return (list(reversed(top_indices)))


if __name__ == '__main__':
    app.run(debug=True)