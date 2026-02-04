import re
import os
from fastmcp import FastMCP

mcp = FastMCP("EmployeeManager")
DB_FILE = "employees.md"


@mcp.tool()
def update_employee_record(name: str, new_details: str) -> str:
    """
    Updates an existing employee's details or adds a new one.
    'new_details' should be the bullet points (e.g., - Role: Engineer...)
    """
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f: f.write("# Employees\n")

    with open(DB_FILE, "r") as f:
        content = f.read()

    # Search for the header ## Name and everything until the next ##
    pattern = rf"## {re.escape(name)}.*?(?=\n##|$)"
    new_entry = f"## {name}\n{new_details}"

    if re.search(pattern, content, re.DOTALL):
        # Update existing
        updated_content = re.sub(pattern, new_entry, content, flags=re.DOTALL)
        msg = f"Updated {name}'s record."
    else:
        # Add new
        updated_content = content + f"\n\n{new_entry}"
        msg = f"Added new record for {name}."

    with open(DB_FILE, "w") as f:
        f.write(updated_content.strip() + "\n")

    return msg