import typer
from rich.prompt import Prompt
from rich import print
from rich.console import Console
import json
import pendulum
from rich.table import Table
from rich.columns import Columns

app = typer.Typer()
task_file = "task.json"
console = Console()

def load_task():
    try:
        with open(task_file, "r") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_task(tasks):
    with open(task_file, "w") as file:
        json.dump(tasks, file, indent=4)

def get_next_available_key(tasks):
    """Finds the smallest positive integer key not currently in use."""
    existing = set(map(int, tasks.keys()))
    i = 1
    while i in existing:
        i += 1
    return str(i)

def renumber_tasks(tasks):
    """Renumber tasks so keys are sequential, starting from 1."""
    new_tasks = {}
    for idx, (old_key, value) in enumerate(sorted(tasks.items(), key=lambda x: int(x[0])), start=1):
        new_tasks[str(idx)] = value
    return new_tasks

def add():
    tasks = load_task()
    key = get_next_available_key(tasks)
    task = Prompt.ask("[bold green]Enter Task: [/]")    
    timestamp = pendulum.now()
    new_task = {
        "task": task,
        "status": "pending",
        "datetime": timestamp.format('DD-MM-YYYY HH:mm')
    }
    tasks[key] = new_task
    save_task(tasks)
    console.print(f"Task Added ", style="bold cyan")


def delete(force: bool = False):
    tasks = load_task()
    if not tasks:
        print("[red]No Tasks to delete[/]")
        raise typer.Exit()
    print("[bold]Current tasks:[/bold]")
    for k, t in tasks.items():
        print(f"[cyan]{k}[/]: {t['task']} ({t['status']})")
    key = Prompt.ask("[bold green]Enter Task Key: [/]")   
    if key in tasks:
        if not force:
            confirm = typer.confirm(f"Delete task #{key}: {tasks[key]['task']}?")
            if not confirm:
                print("[yellow]Operation cancelled[/]")
                raise typer.Exit()
        deleted = tasks.pop(key)
        save_task(tasks)
        print(f"[bold red]Deleted:[/] {deleted['task']}")
    else:
        print("[bold red]Invalid Task Key[/]")

def view():
    tasks = load_task()
    if not tasks:
        print("[red]No tasks found.[/]")
        return

    # Filter tasks
    pending_tasks = {k: v for k, v in tasks.items() if v.get("status") == "pending"}
    completed_tasks = {k: v for k, v in tasks.items() if v.get("status") == "completed"}

    console = Console()

    # Pending table
    pending_table = Table(title="Pending Tasks")
    pending_table.add_column("Task #", style="cyan", justify="right")
    pending_table.add_column("Task", style="green")
    pending_table.add_column("Status", style="magenta")
    pending_table.add_column("Date", style="yellow")
    for key in sorted(pending_tasks, key=int):
        t = pending_tasks[key]
        pending_table.add_row(str(key), t.get("task", ""), t.get("status", ""), t.get("datetime", ""))

    # Completed table
    completed_table = Table(title="Completed Tasks")
    completed_table.add_column("Task #", style="cyan", justify="right")
    completed_table.add_column("Task", style="green")
    completed_table.add_column("Status", style="magenta")
    completed_table.add_column("Date", style="yellow")
    for key in sorted(completed_tasks, key=int):
        t = completed_tasks[key]
        completed_table.add_row(str(key), t.get("task", ""), t.get("status", ""), t.get("datetime", ""))

    console=Console()
    console.print(Columns([pending_table,completed_table]))
    
def status():
    tasks = load_task()
    if not tasks:
        print("[red]No tasks available.[/]")
        return
    
    # Show all tasks for selection
    print("Current tasks:")
    for k in sorted(tasks, key=int):
        print(f"[cyan]{k}[/]: {tasks[k]['task']} ({tasks[k]['status']})")
    
    key = Prompt.ask("[bold green]Enter Task Key: [/]")   
    if key not in tasks:
        print("[red]Invalid Task Key[/]")
        return

    # Ask user for new status
    status = Prompt.ask("Enter new status", choices=["pending", "completed"], default=tasks[key]["status"])
    tasks[key]["status"] = status
    save_task(tasks)
    print(f"[bold green]Status for task '{tasks[key]['task']}' updated to {status}[/]")
    

def menu():
    while True:
        print("\n[bold yellow]Choose an option:[/]")
        print("[cyan]1[/] View To-Do")
        print("[cyan]2[/] Add a new task")
        print("[cyan]3[/] Delete a task")
        print("[cyan]4[/] Update Task Status")
        print("[cyan]5[/] Exit")
        choice = Prompt.ask("[bold green]Enter choice (1/2/3)[/]")
        if choice == "1":
            view()
        elif choice == "2":
            add()
        elif choice == "3":
            delete()
        elif choice == "4":
            status()
        elif choice == "5":
            print("[magenta]Goodbye![/]")
            break
        else:
            print("[red]Invalid option. Try again.[/]")

if __name__ == "__main__":
    menu()  # Directly call the menu for dynamic interaction
