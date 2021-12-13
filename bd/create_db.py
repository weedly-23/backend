from bd.models import db
from weedly_app import create_app
db.create_all(app=create_app())