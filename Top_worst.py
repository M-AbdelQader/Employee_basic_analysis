import csv
from rich.console import Console
from rich.table import Table

console = Console()
# analyze to get top 10 employees from each department


def Top():
    with open("employees.csv", "r") as file:
        reader = csv.DictReader(file)
        employees = list(reader)
        # Sort the employees by KPIs in descending order
    sorted_employees = sorted(
        employees, key=lambda emp: float(emp["KPIs"]), reverse=True
    )

    # Get the top 10 employees
    top_10 = sorted_employees[:10]
    # Print the top 10 employees
    console.print("\n--- Top 10 Employees Based on KPIs ---")
    table = Table(title="Top 10", show_lines=True)
    table.add_column("Name", style="bold magenta")
    table.add_column("Position", style="blue")
    table.add_column("KPIs", style="yellow")

    for i, emp in enumerate(top_10, 1):
        table.add_row(str(i), emp["name"], emp["position"], emp["KPIs"])
    console.print(table)


def worst():
    with open("employees.csv", "r") as file:
        reader = csv.DictReader(file)
        employees = list(reader)

    sorted_employees = sorted(
        employees, key=lambda emp: float(emp["KPIs"]), reverse=False
    )

    Worst_10 = sorted_employees[:10]

    console.print("\n--- worst 10 Employees Based on KPIs ---")
    table = Table(title="worst 10", show_lines=True)
    table.add_column("Name", style="bold magenta")
    table.add_column("Position", style="blue")
    table.add_column("KPIs", style="yellow")

    for i, emp in enumerate(Worst_10, 1):
        table.add_row(str(i), emp["name"], emp["position"], emp["KPIs"])
    console.print(table)


def top_worst():
    answer = input(
        "What analysis would you like to do ?\n 1- Top 10\n 2- Worst 10\n - "
    )
    if answer == "1":
        Top()
    elif answer == "2":
        worst()
    else:
        console.print("[bold red] please enter the correct number [/bold red]")


if __name__ == "__main__":
    top_worst()
