from flask import Flask, jsonify, request, g
import sqlite3
#from model.company import Company, CompanySchema
#from model.news_item import NewsItem, NewsItemSchema

app = Flask(__name__)

def get_db():
    db = getattr(g,"_database",None)
    if db is None:
        print('Connecting to db')
        db = g._database  = sqlite3.connect('miami_db')
    return db


@app.route("/")
def hello_world():
    cur = get_db().cursor()
    cur.execute('SELECT * FROM jamaican_news')
    row = cur.fetchall()

    return "<p> str(row) </p>"


@app.route('/findAll')
def get_all_companies():
    # schema = CompanySchema(many=True)
    # companies = schema.dump()
    # return jsonify(companies)

    cur = get_db().cursor()
    cur.execute('SELECT * FROM jamaican_news')
    row = cur.fetchall()
    response = [{'name': task[0], 'overallAnalysis': 0.5, 'overalRating': 'Positive',
                 'companyAnalysis': [
                     {
                         'date': task[1],
                         'analysis': -2,
                         'rating': 'negative',
                         'title': task[3],
                         'link': task[2],
                         'text': task[4]
                     },
                     {'date': task[1],
                      'analysis': 1,
                      'rating': 'Positive',
                      'title': task[3],
                      'link': task[2],
                      'text': task[4]}]
                 } for task in row]
    return jsonify(response)

@app.route('/findOne')
def get_one_company():
    company = request.args.get('company')
    cur = get_db().cursor()
    cur.execute(f"SELECT * FROM jamaican_news where Company = '{company}'")
    row = cur.fetchall()
    response = [{'name': task[0], 'overallAnalysis': 0.5, 'overalRating': 'Positive',
                 'companyAnalysis': [
                     {
                         'date': task[1],
                         'analysis': -2,
                         'rating': 'negative',
                         'title': task[3],
                         'link': task[2],
                         'text': task[4]
                     },
                     {'date': task[1],
                      'analysis': 1,
                      'rating': 'Positive',
                      'title': task[3],
                      'link': task[2],
                      'text': task[4]}]
                 } for task in row]
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    




