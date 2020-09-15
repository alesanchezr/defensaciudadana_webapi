from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from models import db
from endpoints import all_routes
import datetime
import os


path = "./pdf_store"
if not os.path.exists(path):
    os.mkdir(path)

app = Flask(__name__) # instancio la aplicación Flask
CORS(app)
MIGRATE = Migrate(app, db)
db.init_app(app)

#configuraciones de la app Flask
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')

app.register_blueprint(all_routes)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)