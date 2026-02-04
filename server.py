from fastmcp import FastMCP
import os

mcp = FastMCP("Employee Manager")
DB_FILE = "employees.md"

@mcp.tool
def read_employees() -> str:
    """
    Reads the employee database.
    """
    if not os.path.exists(DB_FILE):
        return "No employee records found"
    with open(DB_FILE, "r") as f:
        return f.read()

@mcp.tool
def update_employee_record(name: str, content: str) -> str:
    """
    Update or add an employee record.
    Provide the full markdown block for that employee.
    """
    with open(DB_FILE, "a") as f:
        f.write(f"\n{content}\n")
        return f"Updated record for {name}."

if __name__ == "__main__":
    mcp.run()