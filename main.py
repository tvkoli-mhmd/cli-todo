import click
import json
from rich.console import Console
from rich.table import Table
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
@click.option("--arrange", default="status", type=click.Choice(["status", "priority"]))
def show(status, priority, arrange):
    filtered_tasks = []
    def sort_by_status(task:dict):
        flag=None
        if task["status"]=="pending":
            flag=0
        else:
            flag=1
        return flag
    def sort_by_priority(task:dict):
        flag=None
        if task["priority"]=="low":
            flag=0
        elif task["priority"]=="medium":
            flag=1
        else:
            flag=2
        return flag
    if status!="all" and priority=="all":
        for task in all_tasks:
            if task["status"]==status:
                filtered_tasks.append(task)
    elif status!= "all" and priority!="all":
        for task in all_tasks:
            if task["status"]==status and task["priority"]==priority:
                filtered_tasks.append(task)
    elif status=="all" and priority!="all":
        for task in all_tasks:
            if task["priority"]==priority:
                filtered_tasks.append(task)
    elif status == "all" and priority == "all":
        if len(all_tasks)>0:
            for task in all_tasks:
                filtered_tasks.append(task)
        else:
            click.echo("No tasks right now!")
    if arrange=="status":
        filtered_tasks.sort(key=sort_by_status) 
    else:
        filtered_tasks.sort(key=sort_by_priority, reverse=True)
    if len(all_tasks)>0:
        table = Table(title="Todo", show_lines=True, padding=1)
        table.add_column("title", style="cyan", justify="left", width=25, overflow="ellipsis")
        table.add_column("status", justify="center", width=10)
        table.add_column("priority", justify="center", width=10)
        table.add_column("id", style="dim", justify="center", width=5)
        for t in filtered_tasks:
            status_color = ""
            priority_color = ""
            if t["status"]=="done":
                status_color=f":white_heavy_check_mark: [green]{t["status"]}[/green]"
            else:
                status_color=f":hourglass: [yellow]{t["status"]}[/yellow]"
            if t["priority"]=="low":
                priority_color=f"[green]{t["priority"]}[/green]"
            elif t["priority"]=="medium":
                priority_color=f"[yellow]{t["priority"]}[/yellow]"
            else:
                priority_color=f"[red]{t["priority"]}[/red]"
            table.add_row(str(t["title"]), status_color, priority_color, str(t["id"]))
        console = Console()
        console.print(table)
@todo.command(help="lets you delete tasks!")
@click.argument("id")
def delete(id):
    if id.lower()=="all":
        all_tasks.clear()
    elif len(all_tasks) ==0:
        click.echo("there is nothing to delete!")
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