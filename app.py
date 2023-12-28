import json
from flask import Flask, jsonify, request



app = Flask(__name__)
# https://code.visualstudio.com/docs/python/tutorial-flask

# tasks = json.load(open('table.json'))

# @app.route("/")
# def hello():
#     return jsonify({'tasks': tasks})

tasks = {
    1: {"id":1, "description":"Do Laundry", "done": "False"},
    2: {"id":2, "description":"Do Homework", "done": "False"}
}

task_current_id = 2

@app.route('/')
@app.route('/tasks/')
def getTasks():
    """
    Get all tasks
    """
    res = {"tasks": list(tasks.values())}
    return json.dumps(res)

@app.route("/tasks/", methods=["POST"])
def createTasks():
    """
    create a new task
    """
    global task_current_id
    body = json.loads(request.data)
    description = body.get("description")
    # return json.dumps(body)
    task_current_id += 1
    task = {"id":task_current_id, "description":description, "done": "False"}
    tasks[task_current_id] = task
    return json.dumps(task), 201

@app.route("/tasks/<int:task_id>/")
def getOneTask(task_id):
    """
    Get task with specific id
    """
    task = tasks.get(task_id)
    if task is None:
        return json.dumps({"error":"Task not found"}), 404
    return json.dumps(task), 200

@app.route("/tasks/<int:task_id>/", methods=["PUT"])
def updateTask(task_id):
    """
    update task if taskid is present or send error
    """
    task = tasks.get(task_id)
    if task is None:
        return json.dumps({"error":"Task not found"}), 404
    # return json.dumps(task), 200

    body = json.loads(request.data)
    task['description'] = body.get('description')
    task['done'] = body.get('done')
    return json.dumps(task)

@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def deleteTask(task_id):
    task = tasks.get(task_id)
    if task is None:
        return json.dumps({"error":"Task not found"}), 404
    del tasks[task_id]
    return json.dumps(task), 200
        
    


if __name__ == "__main__":
    print(tasks)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host="0.0.0.0", port=5000, debug=True)

 
"""
error -  File "/Users/ankit/Documents/GitHub/Flask/.venv/lib/python3.9/site-packages/werkzeug/serving.py", line 231, in write
    status < 200 or status in (204, 304)):
TypeError: '<' not supported between instances of 'str' and 'int'
resolution - https://stackoverflow.com/questions/52085099/werkzeug-on-python-3-raises-not-supported-between-instances-of-str-and-int 
"""

