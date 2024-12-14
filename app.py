from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import re
import openai

# Initialize FastAPI app
app = FastAPI()

# Database setup
DB_PATH = "insights_agent.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY,
        project_id INTEGER,
        vendor_name TEXT,
        invoice_number TEXT,
        total_claimed_amount REAL,
        balance_amount REAL,
        billing_date TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        name TEXT
    )''')
    conn.commit()
    conn.close()

create_tables()

# Models
class UploadData(BaseModel):
    data: List[dict]

class QueryResponse(BaseModel):
    result: str
    details: Optional[List[dict]]

class NaturalQuery(BaseModel):
    natural_query: str

# Utility function to insert data into the database
def insert_data(data: List[dict]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for entry in data:
        # Extract relevant fields from provided data
        invoice_data = (
            entry['id'],  # invoice_id
            entry['project_id'],  # project_id
            entry['vendor_name'],  # vendor_name
            entry['invoice_number'],  # invoice_number
            float(entry['total_claimed_amount']),  # total_claimed_amount
            float(entry['summary']['balance_to_finish_including_retainage']),  # balance_amount
            entry['billing_date']  # billing_date
        )
        cursor.execute('''INSERT OR REPLACE INTO invoices (
            id, project_id, vendor_name, invoice_number, 
            total_claimed_amount, balance_amount, billing_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)''', invoice_data)

        # Insert project data (project name from summary_text)
        project_data = (entry['project_id'], entry['summary_text']['project_name'])
        cursor.execute('''INSERT OR REPLACE INTO projects (id, name) VALUES (?, ?)''', project_data)

    conn.commit()
    conn.close()

# OpenAI API setup
openai.api_key = "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"

def openai_query(prompt: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if needed
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with OpenAI API: {str(e)}")

@app.post("/upload-data")
def upload_data(payload: UploadData):
    try:
        insert_data(payload.data)
        return {"message": "Data uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading data: {str(e)}")

@app.post("/query", response_model=QueryResponse)
def query_input(payload: NaturalQuery):
    try:
        print(payload)
        natural_query = payload.natural_query
        print(natural_query)
        # Out-of-scope queries handled by OpenAI directly
        if any(keyword in natural_query.lower() for keyword in ["score", "weather", "forecast", "game"]):
            response = openai_query(f"{natural_query}. Apologize if out of domain.")
            return QueryResponse(result=response, details=[])

        # Top N invoices for a project
        if "top" in natural_query.lower() and "invoices" in natural_query.lower():
            #print("check")
            match = re.search(r'top (\d+) invoices for project (.+)', natural_query.lower())
            #print(match)
            if match:
                top_n = int(match.group(1))
                project_name = "Project " + match.group(2).strip().upper()

                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM projects WHERE name = ?', (project_name,))
                project = cursor.fetchone()
                conn.close()
                
                if not project:
                    raise HTTPException(status_code=404, detail=f"Project '{project_name}' not found.")
                project_id = project[0]

                # Query invoices for the project
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''SELECT id, vendor_name, total_claimed_amount 
                                  FROM invoices WHERE project_id = ? 
                                  ORDER BY total_claimed_amount DESC LIMIT ?''', (project_id, top_n))
                rows = cursor.fetchall()
                conn.close()
                
                if not rows:
                    return QueryResponse(result=f"No invoices found for project '{project_name}'.", details=[])

                result = [{"Invoice ID": row[0], "Vendor Name": row[1], "Invoice Amount": row[2]} for row in rows]
                return QueryResponse(result=f"Top {top_n} invoices for project '{project_name}' retrieved successfully.", details=result)

        # Invoice with the highest balance
        elif "highest balance" in natural_query.lower():
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT id, vendor_name, balance_amount 
                              FROM invoices 
                              ORDER BY balance_amount DESC LIMIT 1''')
            row = cursor.fetchone()
            conn.close()

            if not row:
                return QueryResponse(result="No invoices found.", details=[])

            details = {
                "Invoice ID": row[0],
                "Vendor Name": row[1],
                "Balance Amount": row[2]
            }
            return QueryResponse(result="Invoice with the highest balance retrieved successfully.", details=[details])

        # General fallback to OpenAI
        else:
            response = openai_query(f"{natural_query}. Provide relevant insights if possible.")
            return QueryResponse(result=response, details=[])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
