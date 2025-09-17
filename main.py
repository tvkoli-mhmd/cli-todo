import click
import json
with open("tasks.json") as f:
    data = json.load(f)
all_tasks = data["tasks"]
@click.group()
def todo():
    pass
@todo.command(help="lets you add tasks!")
@click.argument("task", nargs=1, default="task1")
@click.argument("priority", nargs=1, default="low", type=click.Choice(["low", "medium", "high"]))
def add(task, priority):
    new_task = {
        "title" : task,
        "status" : "pending",
        "priority" : priority
    }
    if len(all_tasks) > 0:
        new_task["id"] = all_tasks.index(all_tasks[-1]) + 1
    else:
        new_task["id"] = 0
    all_tasks.append(new_task)
    with open("tasks.json", 'w') as f:
        json.dump(data, f)
@todo.command(help="lists all the current tasks! ")
@click.option("--status", help="only shows tasks with specified status by the user", default="all", type=click.Choice(["done", "pending", "all"]))
@click.option("--priority", help="only shows tasks with specified priority by the user", default="all", type=click.Choice(["low", "medium", "high", "all"]))
def show(status, priority):
    if status!="all" and priority=="all":
        for task in all_tasks:
            if task["status"]==status:
                click.echo(f"title : {task["title"]}, priority : {task["priority"]}, id : {task["id"]}")
    elif status!= "all" and priority!="all":
        for task in all_tasks:
            if task["status"]==status and task["priority"]==priority:
                click.echo(f"title : {task["title"]}, id : {task["id"]}")
    elif status=="all" and priority!="all":
        for task in all_tasks:
            if task["priority"]==priority:
                click.echo(f"title : {task["title"]}, status : {task["status"]}, id : {task["id"]}")
    elif status == "all" and priority == "all":
        if len(all_tasks)>0:
            for task in all_tasks:
                click.echo(f"title : {task["title"]}, status : {task["status"]}, priority : {task["priority"]}, id : {task["id"]}")
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
@click.argument("status", nargs=1, type=click.Choice(["done", "pending"]), default="done")
def status(task_id, status):
    all_tasks[int(task_id)]["status"] = status
    with open("tasks.json", "w") as f:
        json.dump(data, f)
@todo.command(help="lets you edit your tasks including title and priority")
@click.argument("task_id", nargs=1)
@click.option("--title", help="lets you change the title of a task")
@click.option("--priority", help="lets you change the priority of a task", type=click.Choice(["low", "medium", "high"]))
def edit(task_id, title, priority):
    if title!=None:
        all_tasks[int(task_id)]["title"] = title
    if priority!=None:
        all_tasks[int(task_id)]["priority"] = priority
    with open("tasks.json", "w") as f:
        json.dump(data, f)

if __name__ == '__main__':
    todo() 