import os
import sqlite3
from fastmcp import FastMCP

DB_PATH = os.path.join(os.path.dirname(__file__),"dairy.db")

mcp = FastMCP("DAIRY_MANAGEMENT")

# Create Tables in database
def init_db():
    with sqlite3.connect(DB_PATH) as c:
        # customers table
        c.execute("""
            CREATE TABLE IF NOT EXISTS customers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
        # milk records table
        c.execute("""
            CREATE TABLE IF NOT EXISTS milk_entry(
                sr_no INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                quantity_in_litres REAL NOT NULL,
                additional_qty REAL NOT NULL,
                amount REAL NOT NULL,
                day TEXT NOT NULL,
                month TEXT NOT NULL,
                year TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        """)
    
init_db()

# FIRST TOOL - Add customer
@mcp.tool()
def add_customer(name,phone,date):
    # ADD CUSTOMER DETAILS INTO DATABASE
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(""" INSERT INTO customers(name,phone,date)
                       VALUES(?, ?, ?)""",
                       (name, phone, date)
        )
        # return {"status":"ok","id":cur.lastrowid}
        return cur.lastrowid

# SECOND TOOL - Add milk entry
@mcp.tool()
def add_milk_entry(customer_id,quantity_in_litres,additional_qty,amount,day,month,year):
    # ADD MILK ENTRY INTO DATABASE
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(""" INSERT INTO milk_entry(customer_id,quantity_in_litres,additional_qty,amount,day,month,year)
                            VALUES(?,?,?,?,?,?,?)""",
                            (customer_id,quantity_in_litres,additional_qty,amount,day,month,year)
        )
        # return {"status":"ok","id":cur.lastrowid}
        return cur.lastrowid

# THIRD TOOL - Total Monthly Bill for a single customer
@mcp.tool()
def monthly_bill(customer_id, month, year):
    # FETCH THE TOTAL BILL FOR A PARTICULAR CUSTOMER IN A GIVEN MONTH AND YEAR
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("""SELECT SUM(amount) 
                        FROM milk_entry 
                        WHERE customer_id=? AND month=? AND year=?""",
                        (customer_id, month, year))
        total = cur.fetchone()[0]
        if total is None:
            total = 0
        # return {"status":"ok","total_bill":total} 
        return total  

# FOURTH TOOL - Customer List
@mcp.tool()
def customer_list():
    # FETCH ALL CUSTOMERS FROM DATABASE
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("SELECT * FROM customers")
        customers = cur.fetchall()
        # return {"status":"ok","customers":customers}
        return customers

# FIFTH TOOL - Milk Entries for a Customer
@mcp.tool()
def milk_entries(customer_id):
    # FETCH ALL MILK ENTRIES FOR A PARTICULAR CUSTOMER ID
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("""SELECT * 
        FROM milk_entry 
        WHERE customer_id = ?""",
        (customer_id,))
        entry = cur.fetchall()
        return entry
    
# RUN THE MCP
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="localhost", port=8000)   