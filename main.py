import os
import json
import sqlite3
from fastmcp import FastMCP

DB_PATH = os.path.join(os.path.dirname(__file__),"dairy.db")

mcp = FastMCP("DAIRY_MANAGEMENT")

# Create Tables in database
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        # customers table
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS customers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
        # milk records table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS milk_entry(
                sr_no INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                quantity_in_litres REAL NOT NULL,
                additional_qty REAL NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        """)
               
init_db()

# FIRST TOOL - Add customer
@mcp.tool()
def add_customer(name,phone,date):
    # ADD CUSTOMER DETAILS INTO DATABASE
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""INSERT INTO customers(name,phone,date)
                       VALUES(?, ?, ?)""",
                       (name, phone, date)
        )
        conn.commit()
        # return {"status":"ok","id":cur.lastrowid}
        return cur.lastrowid

# SECOND TOOL - Add milk entry
@mcp.tool()
def add_milk_entry(customer_id,quantity_in_litres,additional_qty,amount,date):
    # ADD MILK ENTRY INTO DATABASE
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""INSERT INTO milk_entry(customer_id,quantity_in_litres,additional_qty,amount,date)
                       VALUES(?, ?, ?, ?, ?)""",
                       (customer_id,quantity_in_litres,additional_qty,amount,date)
        )

        conn.commit()
        # return {"status":"ok","id":cur.lastrowid}
        return cur.lastrowid

# THIRD TOOL - Total Monthly Bill for a single customer
@mcp.tool()
def monthly_bill(customer_id,month,year):
    # FETCH THE TOTAL BILL FOR A PARTICULAR CUSTOMER IN A GIVEN MONTH AND YEAR
    with sqlite3.connect(DB_PATH) as conn:
        month = str(month).zfill(2)
        year = str(year)
        cur = conn.cursor()
        cur.execute("""SELECT SUM(amount) 
                        FROM milk_entry 
                        WHERE customer_id=? 
                        AND strftime('%m',date)=?
                        AND strftime('%Y',date)=?""",
                        (customer_id,month,year))
        total = cur.fetchone()[0]

        if total is None:
            total = 0
        # return {"status":"ok","total_bill":total} 
        return total  

# FOURTH TOOL - Customer List
@mcp.tool()
def customer_list():
    # FETCH ALL CUSTOMERS FROM DATABASE
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers")
        customers = cur.fetchall()
        
        # return {"status":"ok","customers":customers}
        if len(customers) == 0:
            return {"status":"no customers found"}
        return json.dumps(customers)

# FIFTH TOOL - Milk Entries for a Customer
@mcp.tool()
def milk_entries(customer_id):
    # FETCH ALL MILK ENTRIES FOR A PARTICULAR CUSTOMER ID
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT * 
        FROM milk_entry 
        WHERE customer_id = ?""",
        (customer_id,))
        entries = cur.fetchall()

        if len(entries) > 0:
            return entries
        else:
            return {"status":"no entries found"}
            
    
# RUN THE MCP
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="localhost", port=8000)   