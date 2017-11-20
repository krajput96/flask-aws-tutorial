from application import db
from sqlalchemy.orm import relationship

class Fridge(db.Model):
    Ingredient = db.Column(db.String(128), primary_key=True)
    Quantity = db.Column(db.Integer, unique=False)
    fridgerecipes = db.relationship('recipes', primaryjoin=
    "or_(fridge.Ingredient==recipes.ingredient0, fridge.Ingredient==recipes.ingredient3, fridge.Ingredient==recipes.ingredient4, fridge.Ingredient==recipes.ingredient7)",
    lazy='dynamic')

    def __repr__(self):
        return '<fridge %r>' % self.Ingredient

#fridge.Ingredient==recipes.ingredient1, fridge.Ingredient==recipes.ingredient2,  fridge.Ingredient==recipes.ingredient4,fridge.Ingredient==recipes.ingredient5,
class Store(db.Model):
    Store = db.Column(db.String(128), unique=False)
    Ingredient = db.Column(db.String(128), db.ForeignKey('fridge.Ingredient'), primary_key=True)
    Quantity = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<store %r>' % self.Store

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False)
    cuisine = db.Column(db.String(128), unique=False)
    ingredient0 = db.Column(db.String(128), db.ForeignKey('fridge.Ingredient'), unique=False)
    ing0quantity = db.Column(db.Integer, unique=False)
    ingredient1 = db.Column(db.String(128), db.ForeignKey('fridge.Ingredient'),unique=False)
    ing1quantity = db.Column(db.Integer, unique=False)
    ingredient2 = db.Column(db.String(128), db.ForeignKey('fridge.Ingredient'),unique=False)
    ing2quantity = db.Column(db.Integer, unique=False)
    ingredient3 = db.Column(db.String(128), db.ForeignKey('fridge.Ingredient'), unique=False)
    ing3quantity = db.Column(db.Integer, unique=False)
    ingredient4 = db.Column(db.String(128), db.ForeignKey('fridge.Ingredient'), unique=False)
    ing4quantity = db.Column(db.Integer, unique=False)
    ingredient5 = db.Column(db.String(128), db.ForeignKey('fridge.Ingredient'), unique=False)
    ing5quantity = db.Column(db.Integer, unique=False)
    ingredient6 = db.Column(db.String(128), db.ForeignKey('fridge.Ingredient'), unique=False)
    ing6quantity = db.Column(db.Integer, unique=False)
    ingredient7 = db.Column(db.String(128), db.ForeignKey('fridge.Ingredient'), unique=False)
    ing7quantity = db.Column(db.Integer, unique=False)
    instructions = db.Column(db.String(128), unique=False)
    calories = db.Column(db.Integer, unique=False)
    protein = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return self.id, self.ingredient0, self.ingredient1, self.ingredient2, self.ingredient3, self.ingredient4, self.ingredient5, self.ingredient6, self.ingredient7
