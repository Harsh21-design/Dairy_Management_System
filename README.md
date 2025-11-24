# 🥛 Dairy Management System  
### A Simple MCP-Based Milk Collection & Billing System Using FastMCP, SQLite, and Streamlit

This project is a full-stack dairy management solution built using:

- **FastMCP** (Model Context Protocol Server)  
- **SQLite** (Lightweight local database)   
- **Claude Desktop** as an AI-powered MCP client 
- **Streamlit** (Web-based UI) as an Interactive MCP Client App

The system allows you to manage dairy customers, milk entries, and generate monthly bills — all via MCP tools.

---

## 🚀 Features

### 🧠 MCP Server (Backend)
The FastMCP server provides the following tools:

- **Add Customer**  
- **Add Milk Entry**  
- **Get Customer List**  
- **Get Milk Entries for a Customer**  
- **Calculate Monthly Bill**

All database operations are handled using SQLite.

---

## 🧩 MCP Clients

This project includes **two independent MCP clients**, both using the same server.

### 1️⃣ Streamlit Web Client (Main UI)

A clean and interactive web dashboard to:

- Add customers  
- Add milk entries  
- View customer list  
- View milk entry history  
- Generate monthly bills  

---

### 2️⃣ Claude Desktop Client

Claude Desktop can connect to your MCP server and use tools via natural language.

Example:

> “Add a milk entry for Ramesh of 2 litres for 120 Rupees today.”

Claude will automatically call the correct MCP tool.

---

### 📁 Project Structure
Files:
- main.py # FastMCP server
- dairy.db # SQLite database (auto-created)
- streamlit_client.py # Streamlit UI client
- README.md

---
