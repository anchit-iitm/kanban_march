from flask import Flask, request, render_template, redirect, url_for, session
from models import *
from flask_security import Security, SQLAlchemyUserDatastore
import os, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./kanban.sqlite3'
# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config['SECURITY_REGISTERABLE'] = True
# Don't worry if email has findable domain
app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_POST_REGISTER_VIEW'] = '/test'
app.config['SECURITY_POST_LOGIN_VIEW'] = '/get_data_abcd'
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/test'



db.init_app(app)
app.app_context().push()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/')
def index():
    return 'you are on the root endpoint'

@app.route('/test', methods=['GET', 'POST', 'PUT'])
def hello_world():
    if request.method == 'POST':
        name = request.form.get('l_name')
        key = request.form.get('l_desc')
        var24= "python var that is hard coded"
        print(var24)
        print(name, key)
        return 'Hello, World! this is a post request'
    if request.method == 'PUT':
        return 'Hello, World! this is a put request'
    if request.method == 'GET':
        test_var = 'changed Hello, World! this is a get request, and this is a variable from my flask server!'

        return render_template('form_test.html', jinja_var1=test_var, jinja_var2='this is another variable from server')



@app.route('/add_data', methods=['GET', 'POST'])
def hello_world_2():
    if request.method == 'POST':
        name = request.form.get('l_name')
        key = request.form.get('l_desc')
        add_user_data=User(username=name, passkey=key)
        db.session.add(add_user_data)
        db.session.commit()
        return 'data was added to the db'
    if request.method == 'GET':
        return render_template('form_test.html')

@app.route('/get_data_abcd', methods=['GET'])
def get_data():
    users_data = User.query.all() # user_data = User.query.first() # user_data = User.query.filter_by(User.email="abc@abc.com").all()
    print(users_data)
    for user in users_data:
        print(user.email)
        print(user.password)
        print(user.id)
    # print(users.username)
    # print(users.passkey)    
    # print(users.userid)
    # return 'data was fetched from the db'
    return render_template('test.html', users=users_data)

'''@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        name = request.form.get('user')
        key = request.form.get('pass')
        print(name, key)
        users_data = User.query.filter_by(username=name).first()
        if users_data and users_data.passkey == key:
            print(url_for('get_data'))
            session["session_user"] = users_data.userid
            return redirect(url_for('get_data'))
        else:
            return 'user is not present' #redirect(url_for('register'))'''

@app.route('/list/create', methods=["GET", "POST"])
def create_list():
     if request.method == "GET":
           return render_template('clist.html')
     if request.method == "POST":
            title = request.form.get('l_name')
            content = request.form.get('l_desc')
            c_date = datetime.date.today()
            try:
                add_list=list(list_name=title, list_desc=content, list_c_date=c_date, user_id='1')
                db.session.add(add_list)
                db.session.commit()
                return "yes it was added to the db" #redirect(url_for('dash'))
            except:
                db.session.rollback()
                return ("error in creating")
      

@app.route('/task/<int:list_id>/create', methods=["GET", "POST"])
def taskfn(list_id):
      if request.method == "GET":
            return render_template('ctask.html')
      if request.method == "POST":
            title = request.form.get('t_name')
            content = request.form.get('t_content')
            deadline = request.form.get('t_deadline')
            c_date = datetime.date.today()

            try:
                    add_task=task(list_id=list_id, task_title=title, task_content=content, task_deadline=deadline, task_complete=0, task_c_date=c_date)
                    db.session.add(add_task)
                    db.session.commit()
                    return "yes task was added to the db" #redirect(url_for('dash'))
            except:
                    db.session.rollback()
                    return ("error in creating")




if __name__ == '__main__':
    db.create_all()
    # add_data()
    app.run(debug=True)
