import click
import json
with open("tasks.json") as f:
    data = json.load(f)
all_tasks = data["tasks"]
@click.group()
def todo():
    pass
@todo.command(help="lets you add tasks!")
@click.argument("task")
def add(task):
    new_task = {
        "title" : task,
        "status" : "pending"
    }
    if len(all_tasks) > 0:
        new_task["id"] = all_tasks.index(all_tasks[-1]) + 1
    else:
        new_task["id"] = 0
    all_tasks.append(new_task)
    with open("tasks.json", 'w') as f:
        json.dump(data, f)
@todo.command(help="lists all the current tasks! ")
def show():
    if len(all_tasks) > 0:
        for task in all_tasks:
            click.echo(f"title : {task["title"]}, status : {task["status"]}, id : {task["id"]}")
    else:
        click.echo("No tasks right now!")
@todo.command(help="lets you delete tasks!")
@click.argument("id")
def delete(id):
    if id.lower()=="all":
        all_tasks.clear()
    else:
        del all_tasks[int(id)]
        for t in all_tasks:
            t["id"] = all_tasks.index(t)
    with open("tasks.json", "w") as f:
        json.dump(data, f)
@todo.command(help="lets you change the status of a task")
@click.argument("task_id", nargs=1)
@click.argument("status", nargs=1)
def status(task_id, status):
    all_tasks[int(task_id)]["status"] = status
    with open("tasks.json", "w") as f:
        json.dump(data, f)

if __name__ == '__main__':
    todo()