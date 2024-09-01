from flask import Flask
from models import db
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)
@app.route('/')
def index():
    return 'Welcome to blog API!'


if __name__ =='__main__':
    app.run(debug=True)