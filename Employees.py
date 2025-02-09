import csv
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from deducts_raises import deduct_raise
from Top_worst import top_worst

# Detect if the program is running as an exe or as a script
if getattr(sys, 'frozen', False):
    # Running as an exe, use the temp folder
    application_path = sys._MEIPASS
else:
    # Running as a script, use the current directory
    application_path = os.path.dirname(os.path.abspath(__file__))

csv_file_path = os.path.join(application_path, 'employees.csv')

# Now you can use csv_file_path to read the 


sys.path.append(str(Path(__file__).resolve().parent.parent))


console = Console()


def load_employees(file_path="employees.csv"):
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []


def save_employees(employees, file_path="employees.csv"):
    if not employees:
        return  # Avoid writing empty CSV with no headers

    with open(file_path, "w", newline="") as file:
        fieldnames = employees[0].keys()  # Get column names from the first dictionary
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()  # Write headers
        writer.writerows(employees)  # Write employee data


def add_employee(employees):
    employee = {
        "name": input("Enter a new employee: ").strip(),
        "salary": input("Enter salary: ").strip(),
        "position": input("Enter position: ").strip(),
        "KPIs": input("Enter KPI: ").strip(),
    }
    employees.append(employee)
    save_employees(employees)
    console.print("[bold green]Employee added successfully![/bold green]")


def update_employee(employees):
    view_employees(employees)  # Display all employees first
    try:
        # Get the employee number to update
        index = int(input("Enter employee number to update: ")) - 1
        if 0 <= index < len(employees):
            employee = employees[index]
            print(f"Updating details for {employee['name']}:")

            # Ask what information to update
            update_menu = """ 
            [bold cyan]What would you like to update?[/bold cyan]
            [bold white]1.[/bold white] Name
            [bold white]2.[/bold white] Salary
            [bold white]3.[/bold white] Position
            [bold white]4.[/bold white] KPIs
            """
            console.print(
                Panel(
                    update_menu,
                    title="[bold yellow]Update Menu[/bold yellow]",
                    border_style="blue",
                )
            )
            field_choice = input("Enter your choice: ").strip()

            if field_choice == "1":
                new_name = input(
                    f"Enter new name (current: {employee['name']}): "
                ).strip()
                employee["name"] = new_name
            elif field_choice == "2":
                new_salary = input(
                    f"Enter new salary (current: {employee['salary']}): "
                ).strip()
                employee["salary"] = new_salary
            elif field_choice == "3":
                new_position = input(
                    f"Enter new position (current: {employee['position']}): "
                ).strip()
                employee["position"] = new_position
            elif field_choice == "4":
                new_kpis = input(
                    f"Enter new KPIs (current: {employee['KPIs']}): "
                ).strip()
                employee["KPIs"] = new_kpis
            else:
                console.print("[bold red]Invalid choice. No changes made.[/bold red]")
                return

            console.print(
                f"[bold green]Employee {employee['name']}'s information updated successfully![/bold green]"
            )
            save_employees(employees)  # Save the updated employee list
        else:
            console.print("[bold red]Invalid employee number.[/bold red]")
    except ValueError:
        console.print("[bold yellow]Please enter a valid number.[/bold yellow]")


def view_employees(employees):
    if not employees:
        console.print("[bold red]No employees found![/bold red]")
        return

    table = Table(title="Employee List", show_lines=True)
    table.add_column("No.", justify="right", style="cyan")
    table.add_column("Name", style="bold magenta")
    table.add_column("Salary", justify="right", style="green")
    table.add_column("Position", style="blue")
    table.add_column("KPIs", style="yellow")

    for i, employee in enumerate(employees, 1):
        table.add_row(
            str(i),
            employee["name"],
            employee["salary"],
            employee["position"],
            employee["KPIs"],
        )
    console.print(table)


def delete_employee(employees):
    view_employees(employees)
    try:
        index = int(input("Enter employee number to delete: ")) - 1
        if 0 <= index < len(employees):
            deleted_employee = employees.pop(index)
            save_employees(employees)
            console.print(
                f"[bold green]Deleted: {deleted_employee['name']}[/bold green]"
            )
        else:
            console.print("[bold red]Error: Invalid employee number[/bold red]")
    except ValueError:
        console.print("[bold yellow]Hint: Enter a valid number.[/bold yellow]")


def search_employees(employees):
    search_criteria = (
        input("Enter search criteria (name, position, or KPIs): ").strip().lower()
    )

    # Filter employees based on the search criteria
    matching_employees = [
        emp
        for emp in employees
        if search_criteria in emp["name"].lower()
        or search_criteria in emp["position"].lower()
        or search_criteria in str(emp["KPIs"]).lower()
    ]

    if matching_employees:
        console.print("\n--- Search Results ---")
        table = Table(title="Employee List", show_lines=True)
        table.add_column("No.", justify="right", style="cyan")
        table.add_column("Name", style="bold magenta")
        table.add_column("Salary", justify="right", style="green")
        table.add_column("Position", style="blue")
        table.add_column("KPIs", style="yellow")

        for i, employee in enumerate(matching_employees, 1):
            table.add_row(
                str(i),
                employee["name"],
                employee["salary"],
                employee["position"],
                employee["KPIs"],
            )
        console.print(table)
    else:
        console.print(
            "[bold red]No employees found with that search criteria.[/bold red]"
        )


def sort_employees(employees):
    # Ask the user which field they want to sort by
    print("\nSort by: 1. Name 2. Salary 3. Position")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        field = "name"
    elif choice == "2":
        field = "salary"
    elif choice == "3":
        field = "position"
    else:
        console.print("[bold red]Invalid choice, sorting by name.[/bold red]")

    # Ask if the user wants to sort in ascending or descending order
    order = input("Enter sorting order (asc/desc): ").strip().lower()

    if order == "asc":
        employees.sort(
            key=lambda x: x[field].lower() if isinstance(x[field], str) else x[field]
        )
    elif order == "desc":
        employees.sort(
            key=lambda x: x[field].lower() if isinstance(x[field], str) else x[field],
            reverse=True,
        )
    else:
        print("[bold red]Invalid order, defaulting to ascending.[/bold red]")
        employees.sort(
            key=lambda x: x[field].lower() if isinstance(x[field], str) else x[field]
        )

    console.print("[bold green]Employees sorted successfully![/bold green]")


def show_menu():
    menu_text = """
    [bold cyan]Employee Management System[/bold cyan]
    [bold white]1.[/bold white] Add Employee
    [bold white]2.[/bold white] View Employees
    [bold white]3.[/bold white] Delete Employee
    [bold white]4.[/bold white] Update Employee
    [bold white]5.[/bold white] Top & worst analysis
    [bold white]6.[/bold white] Search Employees
    [bold white]7.[/bold white] Sort Employees
    [bold white]8.[/bold white] Calculate deductions
    [bold white]0.[/bold white] Exit
    """
    console.print(
        Panel(menu_text, title="[bold yellow]Menu[/bold yellow]", border_style="blue")
    )


def main():
    employees = load_employees()
    while True:
        show_menu()
        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_employee(employees)
        elif choice == "2":
            view_employees(employees)
        elif choice == "3":
            delete_employee(employees)
        elif choice == "4":
            update_employee(employees)
        elif choice == "5":
            top_worst()
        elif choice == "6":
            search_employees(employees)
        elif choice == "7":
            sort_employees(employees)
        elif choice == "8":
            deduct_raise()
        elif choice == "0":
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")
    console.print("[bold cyan]Goodbye![/bold cyan]")


if __name__ == "__main__":
    main()
