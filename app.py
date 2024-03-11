from flask import Flask, request, render_template
# from models import db, User, list, task
# from flask import *
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./mydb.sqlite3'


db.init_app(app)
app.app_context().push()

@app.route('/test', methods=['GET', 'POST', 'PUT'])
def hello_world():
    if request.method == 'POST':
        return 'Hello, World! this is a post request'
    if request.method == 'PUT':
        return 'Hello, World! this is a put request'
    if request.method == 'GET':
        test_var = 'changed Hello, World! this is a get request, and this is a variable from my flask server!'

        return render_template('test.html', jinja_var1=test_var, jinja_var2='this is another variable from server')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
