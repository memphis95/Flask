import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error":message}), code

@app.route('/')
@app.route('/tasks/')
def getTasks():
    """
    Endpoint for getting all tasks 
    """
    # return json.dumps({"tasks": DB.get_all_tasks()}), 200
    return success_response(DB.get_all_tasks())


@app.route("/tasks/", methods=["POST"])
def createTask():
    """
    Endpoint for creating a task
    """
    body = json.loads(request.data)
    description = body.get("description")
    # done = body.get("done")
    task_id = DB.insert_task_table(description, False)
    task = DB.get_task_by_id(task_id)
    if task is not None:
        return success_response(task, 201)
    return failure_response("Something went wrong while creating task!")
        


@app.route("/tasks/<int:task_id>/")
def getTask(task_id):
    """
    Endpoint for getting task by its id
    """
    task = DB.get_task_by_id(task_id)
    if task is not None:
        return success_response(task)
    return failure_response("Task not found!")

@app.route("/tasks/<int:task_id>/", methods=["PUT"])
def updateTask(task_id):
    """
    Endpoint for updating the task
    """
    body = json.loads(request.data)
    description = body.get("description")
    done = bool(body.get("done"))
    DB.update_task_by_id(description, done, task_id)

    task = DB.get_task_by_id(task_id)
    if task is not None:
        return success_response(task)
    return failure_response("Task not found!")

@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def deleteTask(task_id):
    """
    Endpoint for deleting a task from the database
    """
    task = DB.get_task_by_id(task_id)
    if task is None:
        return json.dumps({"error":"Task not found."}), 404
    DB.delete_task_by_id(task_id)
    return json.dumps(task), 200

    
#--------------------------Subtasks--------------------------------#    
    


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host="0.0.0.0", port=5000, debug=True)

 

