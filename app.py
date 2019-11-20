from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def  __repr__(self):
    return f'<Todo {self.id} {self.description}>'

db.create_all()

# # Route listening to route /todos/create which 
# # has information submited via the form

# @app.route('/todos/create', methods=['POST'])
# def create_todo():
#   # reading form data using imported request method in Flask
#   description = request.form.get('description', '')
#   # create new record in our todo table
#   # create todo object
#   todo = Todo(description=description)
#   db.session.add(todo)
#   db.session.commit()
#   # Render the view with new data
#   return redirect(url_for('index'))

# AJAX updata TODOs list via json

@app.route('/todos/create', methods=['POST'])
def create_todo():
  # get_json fetches the body send by fetch method
  description = request.get_json()['description']
  # create new record in our todo table
  # create todo object
  todo = Todo(description=description)
  db.session.add(todo)
  db.session.commit()
  # Send data via json to be appended to todos list
  return jsonify({
   'description' : todo.description
  })

@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.all())

