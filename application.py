'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''
import sqlite3


from flask import Flask, render_template, request, g
from application import db
from application.models import Data
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from collections import Counter

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

class Recipes(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    cuisine = db.Column(db.String(20))
    ingredient0 = db.Column(db.String(20))
    ing0quantity = db.Column(db.String(20))
    ingredient1 = db.Column(db.String(20))
    ing1quantity = db.Column(db.String(20))
    ingredient2 = db.Column(db.String(20))
    ing2quantity = db.Column(db.String(20))
    ingredient3 = db.Column(db.String(20))
    ing3quantity = db.Column(db.String(20))
    ingredient4 = db.Column(db.String(20))
    ing4quantity = db.Column(db.String(20))
    ingredient5 = db.Column(db.String(20))
    ing5quantity = db.Column(db.String(20))
    ingredient6 = db.Column(db.String(20))
    ing6quantity = db.Column(db.String(20))
    ingredient7 = db.Column(db.String(20))
    ing7quantity = db.Column(db.String(20))

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    result = Recipes.query.all()

    # below query is simple filter by, ordered by ID
    #result = Recipes.query.filter_by(cuisine = "mexican").order_by(desc(calories))
    return render_template('index.html', result=result)

@application.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM reciesp""")
    return '<br>'.join(str(row) for row in rows)


@application.route('/countme/<input_str>')
def count_me(input_str):
    input_counter = Counter(input_str)
    response = []
    for letter, count in input_counter.most_common():
        response.append('"{}":{}'.format(letter, count))
    return '<br>'.join(response)

application.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://krajput96:cs336proj@whatshouldieat.c8rryuxgrrfa.us-east-1.rds.amazonaws.com:3306/whatshouldieat/recipes'
db = SQLAlchemy(application)




# DATABASE = 'mysql+pymysql://krajput96:cs336proj@whatshouldieat.c8rryuxgrrfa.us-east-1.rds.amazonaws.com:3306/whatshouldieat'
#
# engine = create_engine(DATABASE)
#
# print(engine.table_names())




if __name__ == '__main__':
    application.run()
    #host='0.0.0.0'
