from flask import Flask, render_template, request, redirect, url_for
from models import *
from flask_security import Security, SQLAlchemyUserDatastore, current_user, login_user, logout_user, roles_accepted, login_required
import os
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./kanban.sqlite3'

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

def prepare_rbac():
    admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_role = user_datastore.find_or_create_role(name='user', description='User')
    db.session.commit()

def create_admin():
    email = 'admin@abc.com'
    password = 'admin'
    admin_user = user_datastore.find_user(email=email) # user = User.query.filter(User.email == email).first()
    if not admin_user:
        admin_user = user_datastore.create_user(email=email, password=password)
        user_datastore.add_role_to_user(admin_user, 'admin')
        db.session.commit()

with app.app_context():
    prepare_rbac()
    create_admin()


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = user_datastore.find_user(email=email)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        return 'Invalid email or password try with a different set'
    return render_template('login.html')

@app.route('/api/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
        user_check = user_datastore.find_user(email=email)
        if not user_check:
            general_user = user_datastore.create_user(email=email, password=password)
            user_datastore.add_role_to_user(general_user, 'user')
            db.session.commit()
            return redirect(url_for('login')) # redirect('/test/api')
        return 'email is already registered, try with a different email id'
    if request.method == 'GET':
        return render_template('register.html')

@app.route('/')
def index():
    if current_user.is_authenticated: # user = User.query.filter(User.id == 1).first()
        return redirect(url_for('dash'))
        # return 'you are on the root endpoint, you are logged in and your email is ' + current_user.email + ' and your role is ' + current_user.roles[0].name + ' and this is the description for that role ' + current_user.roles[0].description
    return redirect(url_for('login'))
    # return 'you are on the root endpoint, you are not logged in'

@app.route('/list/create', methods=["GET", "POST"])    #list create
@login_required
def create_list():
    if request.method == "GET":
        return render_template('clist.html', p=current_user.email)
    if request.method == "POST":
        name = request.form.get('l_name')
        key = request.form.get('l_desc')
        today = date.today()
        userid = current_user.id
        print(name, key, today, userid)
        try:
            print("inside try")
            add_list=List(name=name, desc=key, user_id=userid, c_date=today)
            print(add_list)
            db.session.add(add_list)
            db.session.commit()		
            return redirect(url_for('dash'))
        except:
            db.session.rollback()
            return ("error in creating")

@app.route('/list/<lid>/update', methods=["GET", "POST"])  #list update
@login_required
def update_list(lid):
    if request.method == "GET":
        lists=List.query.filter(List.id==lid).first()
        print(lists)
        if lists:
            print(lists.name)
            return render_template('ulist.html', list=lists, p=current_user)
        return "list not available"
    if request.method == "POST":
        name = request.form.get('l_name')
        desc = request.form.get('l_desc')
        today = date.today()
        print(name, desc, today)
        try:
            List.query.filter(List.id==lid).update({'name':name, 'desc': desc, 'u_date':today})
            db.session.commit()
            
            return redirect(url_for('dash'))
        except:
            db.session.rollback()
            return ("error in updating")

@app.route('/list/<lid>/delete', methods=["GET", "POST"]) #list delete
@login_required
def delete_list(lid):
    if request.method == "GET":
        if not List.query.filter_by(id=lid).first():
            return "list does not exist"
        return render_template('delete.html')
    if request.method == "POST":
        try:
            print("inside try")

            if Task.query.filter_by(list_id=lid).first():
                Task.query.filter_by(list_id=lid).delete()
            if List.query.filter_by(id=lid).first():
                List.query.filter_by(id=lid).delete()
            db.session.commit()
            return redirect(url_for('dash'))
        except:
            db.session.rollback()
            return ("error in removing")


@app.route('/<lid>/task/create', methods=["GET", "POST"])  #task create, and it needs list id so there should be a list id in the db
@login_required
def create_task(lid):
    if request.method == "GET":
        usern = User.query.filter(User.id == current_user.id).first()
        get_list = List.query.filter(List.id == lid).order_by(List.id).first()
        if get_list:
            return render_template('task.html', get_list=get_list, p=usern)
        return "list not available"
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        deadline = request.form.get('deadline')
        complete = request.form.get('check')
        today = date.today()
        try:
            add_task=Task(list_id=lid, title=title, content=content, deadline=deadline, complete=complete, c_date=today)
            db.session.add(add_task)
            db.session.commit()		
            return redirect(url_for('dash'))
        except:
            db.session.rollback()
            return ("error in creating / updating")

@app.route('/task/<tid>/update', methods=["GET", "POST"])
@login_required
def update_task(tid):
    if request.method == "GET":
        usern = User.query.filter(User.id == current_user.id).first()
        get_list = List.query.filter(List.user_id == current_user.id).order_by(List.name).all()
        task=Task.query.filter(Task.id==tid).first()
        if task and get_list:
            return render_template('utask.html', get_list=get_list, task1=task, id=task.id, p=usern)
        return "task or list not available"
    if request.method == "POST":
        list1 = request.form.get('lists')
        title = request.form.get('title')
        content = request.form.get('content')
        deadline = request.form.get('deadline')
        today = date.today()
        try:
            print("inside try")
            Task.query.filter(Task.id==tid).update({'list_id':list1, 'title':title, 'content':content, 'deadline':deadline, 'complete':"0", 'u_date':today})
            db.session.commit()		
            return redirect(url_for('dash'))
        except:
            db.session.rollback()
            return ("error in updating")

@app.route('/task/<tid>/delete', methods=["GET", "POST"])
@login_required
def delete_task(tid):
    if request.method == "GET":
        usern = User.query.filter(User.id == current_user.id).first()
        if not Task.query.filter_by(id=tid).first():
            return "task not available"
        return render_template('delete.html', p=usern)
    if request.method == "POST":
        try:
            if Task.query.filter_by(id=tid).first():
                print("task found to delete")
                Task.query.filter_by(id=tid).delete()
                db.session.commit()
                return redirect(url_for('dash'))
        except:
            db.session.rollback()
            return ("error in deleting" )	

@app.route('/task/<tid>/complete')
@roles_accepted('admin', 'user')
def complete_task(tid):
    if request.method == "GET":
        today = date.today()
        task1=	Task.query.filter_by(id=tid).first()
        list1=	List.query.filter(List.id==task1.list_id).first()
        listId=list1.id
        if task1 and list1:
            try:
                Task.query.filter(Task.id==tid).update({'list_id':"0", 'd_date':today, 'complete':listId})
                db.session.commit()		
                return redirect(url_for('dash'))
            except:
                db.session.rollback()
                return ("error in updating")

@app.route('/dashboard', methods=["GET","POST"])
# @roles_accepted('admin', 'user')
@login_required
def dash():
    if request.method == "GET":
        list=List.query.filter(List.user_id == current_user.id).order_by(List.id).all()
        n = len(list)
        task=Task.query.order_by(Task.deadline).all()
        #user1=user.query.filter(user.userid == i).order_by(user.userid).first()
        today = date.today()
        return render_template('dash.html', lists=list, tasks=task, len=n, p=current_user, today=today)
    if request.method == "POST":
        lname=request.form.get('l_name')
        found = list.query.filter_by(list_name=lname).all()
        if found:
            return "ok"
        else:
            return "not found"


@app.route('/dashboard/complete', methods=["GET","POST"])
@login_required
def cdash():
    if request.method == "GET":
        list1=List.query.filter(List.user_id == current_user.id).order_by(List.id).all()
        n = len(list1)
        task1=Task.query.order_by(Task.d_date).all()
        #user1=user.query.filter(user.userid == i).order_by(user.userid).first()
        return render_template('cdash.html', user=list1, task=task1, len=n, p=current_user.email, a=current_user.id)
    if request.method == "POST":
        lname=request.form.get('l_name')
        found = list.query.filter_by(list_name=lname).all()
        if found:
            return "ok"
        else:
            return "not found"

@app.route('/summary', methods=["GET", "POST"])
@login_required
def summary():
    if request.method == "GET":
        list1=List.query.filter(List.user_id == current_user.id).order_by(List.id).all()
        n = len(list1)
        task0=Task.query.filter(Task.list_id == "0").all()
        task1=Task.query.order_by(Task.d_date).all()
        return render_template('summary.html', list=list1, task0=task0, task1=task1, len=n, p=current_user.email)


@app.route('/summary/<lid>', methods=["GET", "POST"])
@login_required
def summary_list(lid):
    if request.method == "GET":
        list1=List.query.filter(List.id == lid).first()
        #n = len(list1)
        task1 = Task.query.filter(Task.complete == lid).all()
        ltask1=len(task1)
        task0 = Task.query.filter(Task.list_id == lid).all()
        ltask0=len(task0)
        total = ltask0 + ltask1
        #user1=user.query.filter(user.userid == i).order_by(user.userid).first()
        return render_template('listsummary.html', list=list1, task0=task0, ltask0=ltask0, task1=task1, ltask1=ltask1, p=current_user.email, total=total)


@app.route('/user/<uid>')
def test_api(uid):
    user1=User.query.filter(User.id == uid).first()
    return user1.email

@app.route('/api/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))
    return 'you are not logged in'

if __name__ == '__main__':
    app.run(debug=True) #app.run(debug=True, port=5241)