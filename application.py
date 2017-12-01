 # coding=utf-8

import sqlite3
import urllib.request, json
from pprint import pprint

from flask import Flask, render_template, request, g, redirect, flash, session
from application import db
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from collections import Counter
from application.forms import complexForm, moreInformation, patternVerf, addFridge
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.ext.wtf import Form
#from flask_bootstrap import Bootstrap
#from application.models import Fridge, Store, Recipes

# Elastic Beanstalk initalization
application = Flask(__name__)
application.secret_key = "bahhah"
#Bootstrap(application)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

db.init_app(application)


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

    Ingredient = db.Column(db.String(20), primary_key = True)
    Quantity = db.Column(db.Integer)

class Store(db.Model):
    Store = db.Column(db.String(128), unique=False)
    Ingredient = db.Column(db.String(128), db.ForeignKey('fridge.Ingredient'), primary_key=True)
    Quantity = db.Column(db.Integer, unique=False)

# class Store(db.Model):
#     __bind_key__ == 'store'
#     ingredient = db.Column(db.String(20), primary_key = True)
#     quantity = db.Column(db.Integer)

selectedCuisine = ''

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    #allRecipes = Recipes.query.order_by(Recipes.calories.desc())
    #allRecipesMinusZero = Recipes.query.all()

    engine = create_engine('mysql+pymysql://krajput96:cs336proj@whatshouldieat.c8rryuxgrrfa.us-east-1.rds.amazonaws.com:3306/whatshouldieat', isolation_level="READ UNCOMMITTED")
    connection1 = engine.connect()
    connection2 = engine.connect()
    connection3 = engine.connect()



    r = connection1.execute("select * from recipes")
    f = connection2.execute("select * from fridge")
    s = connection3.execute("select * from store")

    recipes_data = {}
    fridge_list = []
    fridge_dict = {}
    count_Recipe = {}
    store_data = {}
    recipe_calories_protein = {}
    store_location = {}

    store_location['me'] = "Edison,NJ"
    store_location['Costco'] = "205+Vineyard+Rd,+Edison,+NJ+08817"
    store_location['StopnShop'] = "1049+US+Highway+1+South,+Edison,+NJ+08837"
    store_location['Walmart'] = "360+US+Highway+9+Route+N,+Woodbridge,+NJ+07095"
    store_location['Shoprite'] = "3600+Park+Ave,+South+Plainfield,+NJ+07080"



    for rec in r:
        my_list = [(rec.ingredient0, rec.ing0quantity), (rec.ingredient1, rec.ing1quantity), (rec.ingredient2, rec.ing2quantity), (rec.ingredient3, rec.ing3quantity), (rec.ingredient4, rec.ing4quantity), (rec.ingredient5, rec.ing5quantity), (rec.ingredient6, rec.ing6quantity), (rec.ingredient7, rec.ing7quantity)]
        recipes_data[rec.id] = my_list

    for frid in f:
        fridge_list.append(frid[0])
        fridge_dict[frid[0]] = frid[1]

    for store in s:
        store_data[store.Ingredient] = [store.Store, store.Quantity]

    # print (recipes_data.get(1))
    # print (fridge_list)
    # for x in range(0, 1000):
    #     counter = 0
    #     for val in recipes_data.get(x):
    #         if val in fridge_list:
    #             counter = counter + 1
    #     count_Recipe[x] = counter
    #
    # for key, value in recipes_data.items():
    #     counter = 0
    #     for val in value:
    #         if (val[0] in fridge_list) and (val[1] >= fridge_dict[val[0]]) :
    #             counter = counter + 1
    #     count_Recipe[key] = counter
    #

    for key, value in recipes_data.items():
        counter = 0
        for val in value:
            if (val[0] in fridge_list) and (fridge_dict[val[0]] > val[1]):
                counter = counter + 1
        count_Recipe[key] = counter

    #print (count_Recipe)

    noIngredientMissing = []
    oneIngredientMissing = []
    twoIngredientMissing = []
    threeIngredientMissing = []

    for key, value in count_Recipe.items():
        if value == 8:
            noIngredientMissing.append(key)
        if value == 7:
            oneIngredientMissing.append(key)
        if value == 6:
            twoIngredientMissing.append(key)
        if value == 5:
            threeIngredientMissing.append(key)

    myAddress = "Edison,NJ"

    startString = "http://www.mapquestapi.com/directions/v2/route?key=Gb2lkXAUokk1OaZJt1a7jSik8RIAfGu5&from="
    middleString = "&to="

    directionQuery = startString + myAddress + middleString

    #print(directionQuery)
    with urllib.request.urlopen(directionQuery+store_location.get('Costco')) as url:
        data = json.loads(url.read().decode())
        #print(data)

    #print(data['route']['legs'][0]['maneuvers'][0]['narrative'])

    # for i in data['route']['legs'][0]['maneuvers']:
    #     print (i['narrative'])

    #send to phone



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
    complex_selection = complexForm(request.form)
    id_selection = moreInformation(request.form)
    pattern_verf = patternVerf(request.form)
    add_fridge = addFridge(request.form)

    allRecipesMinusZero = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).all()
    [next(s for s in allRecipesMinusZero if s.id == id) for id in noIngredientMissing]

    allRecipesMinusOne = Recipes.query.filter(Recipes.id.in_(oneIngredientMissing)).all()
    [next(s for s in allRecipesMinusOne if s.id == id) for id in oneIngredientMissing]

    allRecipesMinusTwo = Recipes.query.filter(Recipes.id.in_(twoIngredientMissing)).all()
    [next(s for s in allRecipesMinusTwo if s.id == id) for id in twoIngredientMissing]

    allRecipesMinusThree = Recipes.query.filter(Recipes.id.in_(threeIngredientMissing)).all()
    [next(s for s in allRecipesMinusThree if s.id == id) for id in threeIngredientMissing]


    if request.method == 'POST' and add_fridge.validate_on_submit():
        addIng = add_fridge.ing.data
        theQuan = add_fridge.quan.data
        print(theQuan)
        data_entered = [(addIng, theQuan)]
        if int(theQuan or 0) > 8 or int(theQuan or 0) < 3:
            flash('The input you entered does not satisfy our constraints! Try again')
            print('fuck this')
            return render_template('index.html',zeroMissing = allRecipesMinusZero, oneMissing=allRecipesMinusOne, twoMissing = allRecipesMinusTwo, threeMissing = allRecipesMinusThree, form3 = complex_selection, form4 = id_selection, form5 = pattern_verf, form6=add_fridge)
        else:
            try:
                db.add(data_entered)
                db.commit()
                db.session.close()
                print('success')
            except:
                output = 'Successfully Added! You added: '+str(addIng)+" with quantity: "+str(theQuan)+" to the fridge!!"
                flash(output)
                print('fuck this')
                return render_template('index.html',zeroMissing = allRecipesMinusZero, oneMissing=allRecipesMinusOne, twoMissing = allRecipesMinusTwo, threeMissing = allRecipesMinusThree, form3 = complex_selection, form4 = id_selection, form5 = pattern_verf, form6=add_fridge)



    if request.method == 'POST' and complex_selection.validate_on_submit():
        target_cuisine = complex_selection.cuisine.data
        target_calories_protein = complex_selection.calories_protein.data
        print('hello')
        if target_cuisine == ' ':
            if target_calories_protein == 'High Protein' or target_calories_protein == 'Low Protein':
                if target_calories_protein == 'High Protein':
                    tuples0 = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).order_by(Recipes.protein.desc()).all()
                    [next(s for s in allRecipesMinusZero if s.id == id) for id in noIngredientMissing]
                    tuples1 = Recipes.query.filter(Recipes.id.in_(oneIngredientMissing)).order_by(Recipes.protein.desc()).all()
                    [next(s for s in allRecipesMinusOne if s.id == id) for id in oneIngredientMissing]
                    tuples2 = Recipes.query.filter(Recipes.id.in_(twoIngredientMissing)).order_by(Recipes.protein.desc()).all()
                    [next(s for s in allRecipesMinusTwo if s.id == id) for id in twoIngredientMissing]
                    tuples3 = Recipes.query.filter(Recipes.id.in_(threeIngredientMissing)).order_by(Recipes.protein.desc()).all()
                    [next(s for s in allRecipesMinusThree if s.id == id) for id in threeIngredientMissing]
                else:
                    tuples0 = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).order_by(Recipes.protein).all()
                    [next(s for s in allRecipesMinusZero if s.id == id) for id in noIngredientMissing]
                    tuples1 = Recipes.query.filter(Recipes.id.in_(oneIngredientMissing)).order_by(Recipes.protein).all()
                    [next(s for s in allRecipesMinusOne if s.id == id) for id in oneIngredientMissing]
                    tuples2 = Recipes.query.filter(Recipes.id.in_(twoIngredientMissing)).order_by(Recipes.protein).all()
                    [next(s for s in allRecipesMinusTwo if s.id == id) for id in twoIngredientMissing]
                    tuples3 = Recipes.query.filter(Recipes.id.in_(threeIngredientMissing)).order_by(Recipes.protein).all()
                    [next(s for s in allRecipesMinusThree if s.id == id) for id in threeIngredientMissing]
            elif target_calories_protein == 'High Calories' or target_calories_protein == 'Low Calories':
                if target_calories_protein == 'High Calories':
                    tuples0 = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).order_by(Recipes.calories.desc()).all()
                    [next(s for s in allRecipesMinusZero if s.id == id) for id in noIngredientMissing]
                    tuples1 = Recipes.query.filter(Recipes.id.in_(oneIngredientMissing)).order_by(Recipes.calories.desc()).all()
                    [next(s for s in allRecipesMinusOne if s.id == id) for id in oneIngredientMissing]
                    tuples2 = Recipes.query.filter(Recipes.id.in_(twoIngredientMissing)).order_by(Recipes.calories.desc()).all()
                    [next(s for s in allRecipesMinusTwo if s.id == id) for id in twoIngredientMissing]
                    tuples3 = Recipes.query.filter(Recipes.id.in_(threeIngredientMissing)).order_by(Recipes.calories.desc()).all()
                    [next(s for s in allRecipesMinusThree if s.id == id) for id in threeIngredientMissing]
                else:
                    tuples0 = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).order_by(Recipes.calories).all()
                    [next(s for s in allRecipesMinusZero if s.id == id) for id in noIngredientMissing]
                    tuples1 = Recipes.query.filter(Recipes.id.in_(oneIngredientMissing)).order_by(Recipes.calories).all()
                    [next(s for s in allRecipesMinusOne if s.id == id) for id in oneIngredientMissing]
                    tuples2 = Recipes.query.filter(Recipes.id.in_(twoIngredientMissing)).order_by(Recipes.calpries).all()
                    [next(s for s in allRecipesMinusTwo if s.id == id) for id in twoIngredientMissing]
                    tuples3 = Recipes.query.filter(Recipes.id.in_(threeIngredientMissing)).order_by(Recipes.calories).all()
                    [next(s for s in allRecipesMinusThree if s.id == id) for id in threeIngredientMissing]
            else:
                tuples0 = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).all()
                [next(s for s in allRecipesMinusZero if s.id == id) for id in noIngredientMissing]
                tuples1 = Recipes.query.filter(Recipes.id.in_(oneIngredientMissing)).all()
                [next(s for s in allRecipesMinusOne if s.id == id) for id in oneIngredientMissing]
                tuples2 = Recipes.query.filter(Recipes.id.in_(twoIngredientMissing)).all()
                [next(s for s in allRecipesMinusTwo if s.id == id) for id in twoIngredientMissing]
                tuples3 = Recipes.query.filter(Recipes.id.in_(threeIngredientMissing)).all()
                [next(s for s in allRecipesMinusThree if s.id == id) for id in threeIngredientMissing]

        else:
            if target_calories_protein == 'High Protein' or target_calories_protein == 'Low Protein':
                if target_calories_protein == 'High Protein':
                    tuples0 = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.protein.desc()).all()
                    [next(s for s in allRecipesMinusZero if s.id == id) for id in noIngredientMissing]
                    tuples1 = Recipes.query.filter(Recipes.id.in_(oneIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.protein.desc()).all()
                    [next(s for s in allRecipesMinusOne if s.id == id) for id in oneIngredientMissing]
                    tuples2 = Recipes.query.filter(Recipes.id.in_(twoIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.protein.desc()).all()
                    [next(s for s in allRecipesMinusTwo if s.id == id) for id in twoIngredientMissing]
                    tuples3 = Recipes.query.filter(Recipes.id.in_(threeIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.protein.desc()).all()
                    [next(s for s in allRecipesMinusThree if s.id == id) for id in threeIngredientMissing]
                else:
                    tuples0 = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.protein).all()
                    [next(s for s in allRecipesMinusZero if s.id == id) for id in noIngredientMissing]
                    tuples1 = Recipes.query.filter(Recipes.id.in_(oneIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.protein).all()
                    [next(s for s in allRecipesMinusOne if s.id == id) for id in oneIngredientMissing]
                    tuples2 = Recipes.query.filter(Recipes.id.in_(twoIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.protein).all()
                    [next(s for s in allRecipesMinusTwo if s.id == id) for id in twoIngredientMissing]
                    tuples3 = Recipes.query.filter(Recipes.id.in_(threeIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.protein).all()
                    [next(s for s in allRecipesMinusThree if s.id == id) for id in threeIngredientMissing]
            elif  target_calories_protein == 'High Calories' or target_calories_protein == 'Low Calories':
                if target_calories_protein == 'High Calories':
                    tuples0 = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.calories.desc()).all()
                    [next(s for s in allRecipesMinusZero if s.id == id) for id in noIngredientMissing]
                    tuples1 = Recipes.query.filter(Recipes.id.in_(oneIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.calories.desc()).all()
                    [next(s for s in allRecipesMinusOne if s.id == id) for id in oneIngredientMissing]
                    tuples2 = Recipes.query.filter(Recipes.id.in_(twoIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.calories.desc()).all()
                    [next(s for s in allRecipesMinusTwo if s.id == id) for id in twoIngredientMissing]
                    tuples3 = Recipes.query.filter(Recipes.id.in_(threeIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.calories.desc()).all()
                    [next(s for s in allRecipesMinusThree if s.id == id) for id in threeIngredientMissing]
                else:
                    tuples0 = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.calories).all()
                    [next(s for s in allRecipesMinusZero if s.id == id) for id in noIngredientMissing]
                    tuples1 = Recipes.query.filter(Recipes.id.in_(oneIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.calories).all()
                    [next(s for s in allRecipesMinusOne if s.id == id) for id in oneIngredientMissing]
                    tuples2 = Recipes.query.filter(Recipes.id.in_(twoIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.calories).all()
                    [next(s for s in allRecipesMinusTwo if s.id == id) for id in twoIngredientMissing]
                    tuples3 = Recipes.query.filter(Recipes.id.in_(threeIngredientMissing)).filter(Recipes.cuisine==target_cuisine).order_by(Recipes.calories).all()
                    [next(s for s in allRecipesMinusThree if s.id == id) for id in threeIngredientMissing]
            else:
                tuples0 = Recipes.query.filter(Recipes.id.in_(noIngredientMissing)).filter(Recipes.cuisine==target_cuisine).all()
                [next(s for s in allRecipesMinusZero if s.id == id) for id in noIngredientMissing]
                tuples1 = Recipes.query.filter(Recipes.id.in_(oneIngredientMissing)).filter(Recipes.cuisine==target_cuisine).all()
                [next(s for s in allRecipesMinusOne if s.id == id) for id in oneIngredientMissing]
                tuples2 = Recipes.query.filter(Recipes.id.in_(twoIngredientMissing)).filter(Recipes.cuisine==target_cuisine).all()
                [next(s for s in allRecipesMinusTwo if s.id == id) for id in twoIngredientMissing]
                tuples3 = Recipes.query.filter(Recipes.id.in_(threeIngredientMissing)).filter(Recipes.cuisine==target_cuisine).all()
                [next(s for s in allRecipesMinusThree if s.id == id) for id in threeIngredientMissing]
        return render_template('both.html', zeroMissing = tuples0, oneMissing = tuples1, twoMissing = tuples2, threeMissing = tuples3, form4 = id_selection)
    if request.method == 'POST' and id_selection.validate_on_submit():
        targetId = id_selection.moreInfo.data
        #print(targetId)
        myList = []
        myMissingList = []
        storesNeeded = {}

        #print(recipes_data.get(int(targetId)))

        missingIngredients = {}



        for val in recipes_data.get(int(targetId)):
            if val[0]:
                myList.append((val[0], val[1]))
        #print(myList)

        # print(fridge_dict)

        for val in myList:
            if (val[0] not in fridge_list) or (fridge_dict[val[0]] < val[1]):
                myMissingList.append(val[0])
        #print(myMissingList)
        for val in myMissingList:
            storesNeeded[val] = store_data.get(val)

        # print ("here")
        # print (storesNeeded)
        #
        # print(myList)

        locationsNeeded = {}

        # print (myMissingList)

        for key, val in storesNeeded.items():
            locationsNeeded[val[0]] = []

        #print (locationsNeeded)

        for key, val in locationsNeeded.items():
            with urllib.request.urlopen(directionQuery+store_location.get(key)) as url:
                data = json.loads(url.read().decode())
                #print(data)

            #print(data['route']['legs'][0]['maneuvers'][0]['narrative'])
            for i in data['route']['legs'][0]['maneuvers']:
                list = locationsNeeded.get(key)
                list.append(i['narrative'])


        #print (locationsNeeded)


        return render_template('getInfo.html', result = targetId, allings = myList, stores = storesNeeded, directions = locationsNeeded)    # below query is simple filter by, ordered by ID
    #result = Recipes.query.filter_by(cuisine = "mexican").order_by(desc(calories))
    # if request.method == 'POST' and pattern_selection.submit():
    #     return render_template('pattern.html', mexicanData = mexicanCaloriesList)    # below query is simple filter by, ordered by ID

    if request.method == 'POST' and pattern_verf.validate_on_submit():
        count0100 = 0
        count101200 = 0
        count201300 = 0
        count301400 = 0
        count401500 = 0
        count501600 = 0
        count601700 = 0
        count701800 = 0
        count801900 = 0
        count9011000 = 0
        p05 = 0
        p610 = 0
        p1115 = 0
        p1620 = 0
        p2125 = 0
        p2630 = 0
        p3135 = 0
        p3640 = 0
        selectedCuisine = pattern_verf.cuisine.data
        alldata = Recipes.query.filter(Recipes.cuisine == selectedCuisine)
        for tuples in alldata:
            if(tuples.calories<=100):
                count0100+=1
            elif(tuples.calories>100 and tuples.calories<=200):
                count101200+=1
            elif(tuples.calories>200 and tuples.calories<=300):
                count201300+=1
            elif(tuples.calories>300 and tuples.calories<=400):
                count301400+=1
            elif(tuples.calories>400 and tuples.calories<=500):
                count401500+=1
            elif(tuples.calories>500 and tuples.calories<=600):
                count501600+=1
            elif(tuples.calories>600 and tuples.calories<=700):
                count601700+=1
            elif(tuples.calories>700 and tuples.calories<=800):
                count701800+=1
            elif(tuples.calories>800 and tuples.calories<=900):
                count801900+=1
            else:
                count9011000+=1
        for tuples in alldata:
            if(tuples.protein<=5):
                p05+=1
            elif(tuples.protein>5 and tuples.protein<=10):
                p610+=1
            elif(tuples.protein>10 and tuples.protein<=15):
                p1115+=1
            elif(tuples.protein>15 and tuples.protein<=20):
                p1620+=1
            elif(tuples.protein>20 and tuples.protein<=25):
                p2125+=1
            elif(tuples.protein>25 and tuples.protein<=30):
                p2630+=1
            elif(tuples.protein>30 and tuples.protein<=35):
                p3135+=1
            else:
                p3640+=1
        return render_template('chart.html', pickedCuisine = selectedCuisine, cal0100 = count0100, cal101200 = count101200, cal201300 = count201300,
    cal301400 = count301400, cal401500 = count401500, cal501600 = count501600, cal601700 = count601700,
    cal701800 = count701800, cal801900 = count801900, cal9011000 = count9011000, prot05 = p05, prot610 = p610,
    prot1115 = p1115, prot1620 = p1620, prot2125 = p2125, prot2630 = p2630, prot3135 = p3135, prot3640 = p3640)
    return render_template('index.html',zeroMissing = allRecipesMinusZero, oneMissing=allRecipesMinusOne, twoMissing = allRecipesMinusTwo, threeMissing = allRecipesMinusThree, form3 = complex_selection, form4 = id_selection, form5 = pattern_verf, form6=add_fridge)



@application.route('/recipes/<input_str>')
def count_me(input_str):
    if (input_str < 0) or (input_str > 10000):
        return NULL

    input_counter = Counter(input_str)
    response = []
    for letter, count in input_counter.most_common():
        response.append('"{}":{}'.format(letter, count))
    return '<br>'.join(response)

application.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://krajput96:cs336proj@whatshouldieat.c8rryuxgrrfa.us-east-1.rds.amazonaws.com:3306/whatshouldieat/recipes'
# application.config['SQLALCHEMY_BINDS'] =  {'fridge': 'mysql+pymysql://krajput96:cs336proj@whatshouldieat.c8rryuxgrrfa.us-east-1.rds.amazonaws.com:3306/whatshouldieat/fridge'}
#

db = SQLAlchemy(application)


if __name__ == '__main__':
    application.run(host='0.0.0.0')

    #host='0.0.0.0'
