import click
import json
with open("tasks.json") as f:
    all_tasks = json.load(f)
@click.group()
def todo():
    pass
@click.command()
@click.argument("task")
def add(task):
    new_task = {
        "title" : task,
        "status" : "pending"
    }
    all_tasks['tasks'].append(new_task)
    with open("tasks.json", 'w') as f:
        json.dump(all_tasks, f)
@click.command()
def show():
    if len(all_tasks['tasks']) > 0:
        for task in all_tasks['tasks']:
            click.echo(f"title : {task["title"]}, status : {task["status"]}")
    else:
        click.echo("No tasks right now!")
todo.add_command(add)
todo.add_command(show)
if __name__ == '__main__':
    todo()