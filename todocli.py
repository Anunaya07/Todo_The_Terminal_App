import typer
from rich.console import Console
from rich.table import Table
from model import Todo
from database import get_all_todos, delete_todo, insert_todo, complete_todo, update_todo

console =  Console()

app = typer.Typer()


@app.command(short_help='adds a todo')
def add(task: str, category: str):
    typer.echo(f"adding {task}, {category}")
    todo = Todo(task, category)
    insert_todo(todo)
    show()


@app.command(short_help='deletes a todo')
def delete(position: int):
       typer.echo(f"deleting {position}")
       # in UI begin at 1, but in database at 0
       delete_todo(position-1)
       show()


@app.command(short_help='update a todo')
def update(position: int,task: str=None, category: str=None):
       typer.echo(f"updating {position}")
       update_todo(position-1, task, category)
       show()
        

@app.command(short_help='used is mark a todo as complete')
def complete(position: int):
       typer.echo(f"complete {position}")
       complete_todo(position-1)
       show()


@app.command(short_help='shows all the todos')
def show():
    tasks = get_all_todos()
    console.print("[bold magenta]Todos[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue",padding=(1,0),expand=True)
    table.add_column("#", style="dim", width=6,justify="center")
    table.add_column("Todo", min_width=20, justify="center")
    table.add_column("Category", min_width=12, justify="center")
    table.add_column("Done", min_width=12, justify="center")

    def get_category_color(category):
        COLORS = {'Learn Python': 'cyan', 'Learn Java': 'red', 'Learn C++': 'blue', 'Learn C': 'green'}
        if category in COLORS:
            return COLORS[category]
        return 'white'

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = '✅' if task.status == 1 else '❌'
        table.add_row(str(idx), task.task, f'[{c}]{task.category}[/{c}]', is_done_str)
    console.print(table)


if __name__ == "__main__":
    app()