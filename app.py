# ./app.py

from flask import Flask, render_template, request, jsonify
from pusher import Pusher
import json

# create flask app
app = Flask(__name__)

# configure pusher object
pusher = Pusher(
  app_id='1640980',
  key='88a49679717a81a3c207',
  secret='53be691da358265d8b75',
  cluster='ap1',
  ssl=True
)

# index route, shows index.html view
@app.route('/')
def index():
  return render_template('index.html')

# endpoint for storing todo item
@app.route('/add-todo', methods = ['POST'])
def addTodo():
  data = json.loads(request.data) # load JSON data from request
  pusher.trigger('flask-pusher', 'item-added', data) # trigger `item-added` event on `todo` channel
  return jsonify(data)

# endpoint for deleting todo item
@app.route('/remove-todo/<item_id>')
def removeTodo(item_id):
  data = {'id': item_id }
  pusher.trigger('flask-pusher', 'item-removed', data)
  return jsonify(data)

# endpoint for updating todo item
@app.route('/update-todo/<item_id>', methods = ['POST'])
def updateTodo(item_id):
  data = {
    'id': item_id,
    'completed': json.loads(request.data).get('completed', 0)
  }
  pusher.trigger('flask-pusher', 'item-updated', data)
  return jsonify(data)

# run Flask app in debug mode
app.run(debug=True)

