from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False, default=False)

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

# AJAX update TODOs list via json

@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    # get_json fetches the body send by fetch method
    description = request.get_json()['description']
    # create new record in our todo table
    # create todo object
    todo = Todo(description=description, completed=False)
    db.session.add(todo)
    db.session.commit()
    body['id'] = todo.id
    body['completed'] = todo.completed
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      abort(400)
    else:
      # Send data via json to be appended to todos list
      return jsonify(body)
      
# Route handler to update on checkbox event
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))
     
# route handler for delete request
@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
    return jsonify({ 'success': True})



@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.order_by('id').all())

