import click
import json
with open("tasks.json") as f:
    all_tasks = json.load(f)
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
    if len(all_tasks["tasks"]) > 0:
        new_task["id"] = all_tasks["tasks"].index(all_tasks["tasks"][-1]) + 1
    else:
        new_task["id"] = 0
    all_tasks['tasks'].append(new_task)
    with open("tasks.json", 'w') as f:
        json.dump(all_tasks, f)
@todo.command(help="lists all the current tasks! ")
def show():
    if len(all_tasks['tasks']) > 0:
        for task in all_tasks['tasks']:
            click.echo(f"title : {task["title"]}, status : {task["status"]}, id : {task["id"]}")
    else:
        click.echo("No tasks right now!")
if __name__ == '__main__':
    todo()