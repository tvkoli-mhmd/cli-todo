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

todo.add_command(add)
if __name__ == '__main__':
    todo()