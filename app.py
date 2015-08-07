from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import make_response

import todo
from todo import Todo, User, db


app = Flask(__name__)
DATABASE = 'todos.db'
SECRET_KEY = 'todo'

app.config.from_object(__name__)


@app.route('/')
def index():
    user_id = request.cookies.get('user_id')
    todos = None
    if user_id:
        todos = Todo.query.filter(Todo.user_id == int(user_id)).all()
    return render_template('index.html', user_id=user_id, todos=todos)


@app.route('/sign', methods=['POST', 'GET'])
def sign():
    if request.method == 'POST':
        userdata = request.form.to_dict()
        print "sign  userdata : ", userdata
        if len(userdata['username']) < 3:
            flash("the length of username should be more than 2 bytes. please rename.")
        elif userdata['password'] != userdata['password1']:
            flash(" Your passwords are different ,please input again.")
        else:
            # since all the conditions are suitable, we can create a new user now.
            newUser = User(username=userdata['username'], password=userdata['password'], email=userdata['email'])
            todo.db.session.add(newUser)
            todo.db.session.commit()
            flash("you have sign in the TODO , now we will jump to your home page...")
            print newUser
            print newUser.id

            response = make_response(redirect(url_for('index')))
            response.set_cookie('user_id', str(newUser.id))
            return response
    return render_template('sign.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    print "log out id : ", request.cookies.get("user_id")
    # request.cookies.pop('user_id',None)
    request.cookies.pop('user_id', None)
    # FIXME TypeError: 'ImmutableTypeConversionDict' objects are immutable
    flash(' you have logged out ')
    return redirect(url_for('index'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        user = User.query.filter(User.username == user_data['username']).all()
        print user

        if user.password == user_data['password']:
            # FIXME AttributeError: 'BaseQuery' object has no attribute 'password'

            flash('log in successful.')
            response = make_response(redirect(url_for('index')))
            response.set_cookie('user_id', user.id)
            return response
    return render_template('login.html')


@app.route('/add/', methods=['POST'])
def add():
    user_id = request.cookies.get('user_id')

    t = request.form['todo']
    # use unicode(), not str(), for Chinese chars
    newTodo = todo.Todo(task=unicode(t), user_id=int(user_id))
    todo.db.session.add(newTodo)
    todo.db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete/<todo_id>/')
def delete(todo_id):
    user_id = request.cookies.get('user_id')
    t = todo.Todo.query.get(int(todo_id))
    if t.user_id == int(user_id):
        todo.db.session.delete(t)
        todo.db.session.commit()
    else:
        flash("sorry, you can't delete others' task... ")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
