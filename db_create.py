from application import db
from application.models import Recipes, Fridge, Store

db.create_all()

print("DB created.")
