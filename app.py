from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
from flask_pymongo import PyMongo
from flask import session
from flask import redirect, url_for
import bcrypt


# -- Initialization section --
app = Flask(__name__)
app.secret_key = "bhwefbiuvwhfewbivewbiu"

#name of database
app.config['MONGO_DBNAME'] = 'database'

#URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:rVrCKMSHrAxIzxth@cluster0.ly81w.mongodb.net/database?retryWrites=true&w=majority'

mongo = PyMongo(app)


# -- Routes section -- 

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',time=datetime.now())

@app.route('/login', methods=["GET", "POST"])
def login():
  session.clear()
  if request.method == "GET":
    return render_template("login.html", time=datetime.now())
  else:
    #login
    if request.form["action"] == "Login":
      username = request.form["username"]
      password = request.form["password"]
      users = mongo.db.users
      login_user = users.find_one({'username' : username})
      if bcrypt.hashpw(password.encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
        session['username'] = login_user["username"]
        return redirect(url_for('index'))
      else:
        return 'Invalid username/password combination'
    
    #signup
    elif request.form["action"] == "Sign Up":
      users = mongo.db.users
      existing_user = users.find_one({'username' : request.form['new_username']})
      if existing_user is None:
        username = request.form["new_username"]
        password = request.form["new_password"]
        users.insert({'username': username, 'password': str(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()), 'utf-8'), 'title': "", "tasks": ["Example 1"]})
        session['username'] = username
        return redirect(url_for('index'))
      return 'That username already exists! Try logging in.'
    
    return "Hello"
    

@app.route('/todo', methods=["GET", "POST"])
def todo():
  collection = mongo.db.users
  query = list(collection.find({"username": session['username']}))
  userTitle = query[0]['title']
  userTasks = query[0]['tasks']
  return render_template('todo.html', title = userTitle, tasks = userTasks, time=datetime.now())

@app.route('/setTitle', methods=["GET", "POST"])
def setTitle():
  if request.method == "POST":
    collection = mongo.db.users
    query = list(collection.find({"username": session['username']}))
    print(query)
    print(request.form['docTitle'])

    origTitle = { "title": query[0]['title'] }
    newTitle = { "$set": { "title": request.form['docTitle']}}
    collection.update_one(origTitle, newTitle)
    query = list(collection.find({"username": session['username']}))
    print("new title", query[0]['title'])

  return redirect('/todo')

@app.route('/addTask', methods=["GET", "POST"])
def addTask():
  collection = mongo.db.users
  query = list(collection.find({"username": session['username']}))
  print(query)
  if request.method == "POST":
    collection = mongo.db.users
    print(request.form['task'])
    task = request.form['task']
    collection.update({'username': session['username']}, {'$push': {'tasks': task}})
    query = list(collection.find({"username": session['username']}))
    userTasks = query[0]['tasks']
    print(userTasks)

  return redirect('/todo')

# @app.route('/post', methods=["GET", "POST"])
# def post():
#   return render_template('post.html', time=datetime.now())

@app.route('/post', methods=["GET", "POST"])
def post():
    if 'username' in session:
        if request.method == "POST":
            post_collection = mongo.db.posts
            username = session['username']
            title = request.form["post-title"]
            message = request.form["post-message"]
            date = datetime.now()
            post = {
                "title" : title,
                "message" : message,
                "date" : date,
                "author" : username
            }
            post_collection.insert(post)
            query = list(post_collection.find({"author": session['username']}))
            print(query)#This query is an array
            #FIXED IT BRB GONNA EAT
            return render_template("post.html", posts = query,time=datetime.now())
        else: 
            return render_template("post.html", time=datetime.now())
    if 'username' in session:
        username = session['username']
        user = users.find_one({'username': username})
        posts = post_collection.find({'author': username})
        print(posts) #maybe i can route it to a new page and have the posts displayed there? Iguess? I dont know uhmm when I submit a post, where is it supposed to go in the code, this if statemnt? it's supposed to add it to the db and add it to the html page ok i am going to try that
        return render_template("login.html", user = user, posts = posts)
    else:
        return "Please log in."


    #     users = mongo.db.users
    # post_collection = mongo.db.posts
    # if 'name' in session:
    #     username = session['username']
    #     user = users.find_one({'username': username})
    #     posts = post_collection.find({'author': username})
    #     return render_template("bio.html", user = user, posts = posts)
    # else:
    #     return "Please log in."

  
  
