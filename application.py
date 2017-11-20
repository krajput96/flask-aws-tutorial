'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''
import sqlite3


from flask import Flask, render_template, request, g
from application import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from collections import Counter
from application.forms import cuisineForm, caloriesForm, complexForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import Form
#from application.models import Fridge, Store, Recipes

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
    instructions = db.Column(db.String(20))
    calories = db.Column(db.Integer)
    protein = db.Column(db.Integer)


class Fridge(db.Model):
    __tablename__ = 'fridge'

    ingredient = db.Column(db.String(20), primary_key = True)
    quantity = db.Column(db.Integer)

# class Store(db.Model):
#     __bind_key__ == 'store'
#     ingredient = db.Column(db.String(20), primary_key = True)
#     quantity = db.Column(db.Integer)


@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    #allRecipes = Recipes.query.order_by(Recipes.calories.desc())
    allRecipes = Recipes.query.all()
    fridgeItems = Fridge.query.all()


    engine = create_engine('mysql+pymysql://krajput96:cs336proj@whatshouldieat.c8rryuxgrrfa.us-east-1.rds.amazonaws.com:3306/whatshouldieat', isolation_level="READ UNCOMMITTED")
    connection1 = engine.connect()
    connection2 = engine.connect()
    connection3 = engine.connect()


    r = connection1.execute("select * from recipes")
    f = connection2.execute("select * from fridge")

    recipes_data = {}
    fridge_list = []
    count_Recipe = {}

    for rec in r:
        my_list = [rec.ingredient0, rec.ingredient1, rec.ingredient2, rec.ingredient3, rec.ingredient4, rec.ingredient5, rec.ingredient6, rec.ingredient7]
        recipes_data[rec.id] = my_list

    for frid in f:
        fridge_list.append(frid[0])

    # print (recipes_data.get(1))
    # print (fridge_list)
    # for x in range(0, 1000):
    #     counter = 0
    #     for val in recipes_data.get(x):
    #         if val in fridge_list:
    #             counter = counter + 1
    #     count_Recipe[x] = counter

    for key, value in recipes_data.items():
        counter = 0
        for val in value:
            if val in fridge_list:
                counter = counter + 1
        count_Recipe[key] = counter


    #print (count_Recipe)

    noIngredientMissing = []
    oneIngredientMissing = []
    twoIngredientMissing = []
    threeIngredientMissing = []

    for key, value in count_Recipe.items():
        if value == 0:
            noIngredientMissing.append(key)
        if value == 1:
            oneIngredientMissing.append(key)
        if value == 2:
            twoIngredientMissing.append(key)
        if value == 3:
            threeIngredientMissing.append(key)



    #print (noIngredientMissing)


    # for x in range(1000):
    #     counter = 0
    #     for y, val in enumerate(recipes_data.get(x)):
    #         if val in fridge_list:
    #             counter += 1
    #     print(counter)


    #
    # for rec in r:
    #     count = 0
    #     for frid in f:
    #         if rec.ingredient0 == frid.Ingredient:
    #             print ('ayee')

    #mexicanRecipes = Recipes.query.filter_by(cuisine = "mexican")

    cuisine_selection = cuisineForm(request.form)
    calories_selection = caloriesForm(request.form)

    complex_selection = complexForm(request.form)


    allRecipes = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).all()
    [next(s for s in allRecipes if s.id == id) for id in noIngredientMissing]


    if request.method == 'POST' and complex_selection.validate_on_submit():
        target_cuisine = complex_selection.cuisine.data
        target_calories_protein = complex_selection.calories_protein.data

        if cuisine_selection == ' ':
            if target_calories_protein == 'High Protein' or target_calories_protein == 'Low Protein':
                if target_calories_protein == 'High Protein':
                    tuples = Recipes.query.order_by(Recipes.protein.desc()).all()
                else:
                    tuples = Recipes.query.order_by(Recipes.protein).all()
            elif  target_calories_protein == 'High Calories' or target_calories_protein == 'Low Calories':
                if target_calories_protein == 'High Calories':
                    tuples = Recipes.query.order_by(Recipes.calories.desc()).all()
                else:
                    tuples = Recipes.query.order_by(Recipes.calories).all()
            else:
                tuples = Recipes.query.all()


        else:
            if target_calories_protein == 'High Protein' or target_calories_protein == 'Low Protein':
                if target_calories_protein == 'High Protein':
                    tuples = Recipes.query.order_by(Recipes.protein.desc()).filter_by(cuisine = target_cuisine).all()
                else:
                    tuples = Recipes.query.order_by(Recipes.protein).filter_by(cuisine = target_cuisine).all()
            elif  target_calories_protein == 'High Calories' or target_calories_protein == 'Low Calories':
                if target_calories_protein == 'High Calories':
                    tuples = Recipes.query.order_by(Recipes.calories.desc()).filter_by(cuisine = target_cuisine).all()
                else:
                    tuples = Recipes.query.order_by(Recipes.calories).filter_by(cuisine = target_cuisine).all()
            else:
                tuples = Recipes.query.all()
        return render_template('both.html', result = tuples)







    if request.method == 'POST' and cuisine_selection.validate_on_submit():
        target_cuisine = cuisine_selection.cuisine.data
        print (target_cuisine)
        print ("Before Query")
        cuisine_tuples = Recipes.query.filter_by(cuisine = target_cuisine).all()
        print ("after Query")
        # for b in cuisine_tuples:
        #     print(b)
        return render_template('cuisines.html', result=cuisine_tuples)

    if request.method == 'POST' and calories_selection.validate_on_submit():
        target_calories = calories_selection.calories.data
        print (target_calories)
        print ('Before Query')
        if target_calories == 'High Calories':
            calories_tuples = Recipes.query.order_by(Recipes.calories.desc())
        else:
            calories_tuples = Recipes.query.order_by(Recipes.calories)
        print ('After Query')
        # for b in calories_tuples:
        #     print(b)
        return render_template('calories.html', result = calories_tuples)



    # below query is simple filter by, ordered by ID
    #result = Recipes.query.filter_by(cuisine = "mexican").order_by(desc(calories))
    return render_template('index.html', result=allRecipes, form1 = cuisine_selection, form2 = calories_selection, form3 = complex_selection)



@application.route('/countme/<input_str>')
def count_me(input_str):
    input_counter = Counter(input_str)
    response = []
    for letter, count in input_counter.most_common():
        response.append('"{}":{}'.format(letter, count))
    return '<br>'.join(response)



# DATABASE = 'mysql+pymysql://krajput96:cs336proj@whatshouldieat.c8rryuxgrrfa.us-east-1.rds.amazonaws.com:3306/whatshouldieat'
#
# engine = create_engine(DATABASE)
#
# print(engine.table_names())

application.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://krajput96:cs336proj@whatshouldieat.c8rryuxgrrfa.us-east-1.rds.amazonaws.com:3306/whatshouldieat/recipes'
# application.config['SQLALCHEMY_BINDS'] =  {'fridge': 'mysql+pymysql://krajput96:cs336proj@whatshouldieat.c8rryuxgrrfa.us-east-1.rds.amazonaws.com:3306/whatshouldieat/fridge'}
#

db = SQLAlchemy(application)


if __name__ == '__main__':
    application.run()
    #host='0.0.0.0'
