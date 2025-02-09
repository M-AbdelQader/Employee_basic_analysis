import csv
from rich.console import Console
from rich.panel import Panel


console = Console()

# if KPIs is less than 50% , auto calculate deductions to salary


def deduce_salary():
    deducted_employees = []
    with open("employees.csv", "r") as file:
        reader = csv.DictReader(file)
        employees = list(reader)

        for employee in employees:
            KPI = float(employee["KPIs"])
            salary = float(employee["salary"])
            try:
                if KPI < 0.50:
                    new_salary = salary * 0.70  # deduct 30%
                    employee["salary"] = round(new_salary, 2)
                    deducted_employees.append(employee)

                    console.print(
                        f"[white]Employee {employee['name']} - KPI: {KPI}% - Salary deducted to {new_salary}[/white]\n"
                    )
            except ValueError:
                print(
                    f"Error with data for employee {employee['name']} (invalid KPI or salary value)"
                )

    with open("deducted_employees.csv", "w", newline="") as file:
        fieldnames = ["name", "salary", "position", "KPIs"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')

        writer.writeheader()  # Write the header row
        writer.writerows(deducted_employees)  # Write only the deducted employee data


def raise_salary():
    raised_employees = []
    with open("employees.csv", "r") as file:
        reader = csv.DictReader(file)
        employees = list(reader)

        for employee in employees:
            KPI = float(employee["KPIs"])
            salary = float(employee["salary"])
            try:
                if KPI > 0.50 and KPI < 0.99:
                    new_salary = salary / 0.7  # raise 30%
                    employee["salary"] = round(new_salary, 2)
                    raised_employees.append(employee)

                    console.print(
                        Panel(
                            f"[white] Employee {employee['name']} - KPI: {KPI}% - Salary raised to {new_salary} [/white]\n",
                            border_style="blue",
                        )
                    )

            except ValueError:
                print(
                    f"Error with data for employee {employee['name']} (invalid KPI or salary value)"
                )

        with open("raised_employees.csv", "w", newline="") as file:
            fieldnames = ["name", "salary", "position", "KPIs"]
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')

            writer.writeheader()  # Write the header row
            writer.writerows(raised_employees)  # Write only the raised employee data


def deduct_raise():
    answer2 = input("do you want to check deductions or raises ?\n>")
    while True:
        if answer2 == "deductions":
            deduce_salary()
        elif answer2 == "raises":
            raise_salary()
        break


if __name__ == "__main__":
    deduct_raise()
