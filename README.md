# **Building an Insights Agent Using FastAPI and OpenAI**

This project implements an **Insights Assistant Agent** that leverages FastAPI and the OpenAI API to provide insights into invoice data. The agent can handle queries related to invoices, such as listing top invoices for a project, summarizing invoices with the highest balance, and gracefully handling out-of-scope questions.

---

## **Features**

1. **Upload Invoice Data**: Upload raw JSON invoice data into an SQLite database.
2. **Query Insights**: Use natural language queries to retrieve insights such as:
   - Top invoices for a specific project.
   - Summary of the invoice with the highest balance.
3. **Handle Out-of-Scope Questions**: Return appropriate responses for queries unrelated to the invoice data (e.g., sports scores or weather updates).
4. **Dynamic SQL Generation**: Use OpenAI's API to generate SQL queries dynamically based on user input.

---

## **Technologies Used**

- **FastAPI**: For building the RESTful API.
- **SQLite**: For storing invoice data.
- **OpenAI API**: For generating SQL queries and insights.
- **Pydantic**: For data validation.
- **Uvicorn**: For running the FastAPI server.

---

## **Project Structure**

```
BUILDING_AN_INSIGHTS_AGENT/
│-- app.py
│-- requirements.txt
│-- insights_agent.db (created during runtime)
│-- README.md
```

- **`app.py`**: Contains the FastAPI application, database setup, and endpoints.
- **`requirements.txt`**: Lists the dependencies required for the project.
- **`insights_agent.db`**: The SQLite database (generated at runtime).
- **`README.md`**: Documentation for the project.

---

## **Endpoints**

### **1. Upload Data**

**Endpoint**: `/upload-data`  
**Method**: `POST`  
**Description**: Uploads invoice data to the SQLite database.

**Request Body Example**:

```json
{
  "data": [
    {
      "id": 58820,
      "project_id": 789,
      "vendor_name": "Ernie's Electrical",
      "invoice_number": "123",
      "total_claimed_amount": 100.00,
      "balance_amount": 1268346.55,
      "billing_date": "2013-11-20",
      "summary": {
        "balance_to_finish_including_retainage": 1268346.55
      },
      "summary_text": {
        "project_name": "Project X"
      }
    },
    {
      "id": 58821,
      "project_id": 789,
      "vendor_name": "Ernie's Electrical",
      "invoice_number": "124",
      "total_claimed_amount": 250.00,
      "balance_amount": 1000000.00,
      "billing_date": "2013-11-21",
      "summary": {
        "balance_to_finish_including_retainage": 1000000.00
      },
      "summary_text": {
        "project_name": "Project X"
      }
    },
    {
      "id": 58822,
      "project_id": 789,
      "vendor_name": "Ernie's Electrical",
      "invoice_number": "125",
      "total_claimed_amount": 500.00,
      "balance_amount": 800000.00,
      "billing_date": "2013-11-22",
      "summary": {
        "balance_to_finish_including_retainage": 800000.00
      },
      "summary_text": {
        "project_name": "Project X"
      }
    },
    {
      "id": 58823,
      "project_id": 789,
      "vendor_name": "Ernie's Electrical",
      "invoice_number": "126",
      "total_claimed_amount": 600.00,
      "balance_amount": 700000.00,
      "billing_date": "2013-11-23",
      "summary": {
        "balance_to_finish_including_retainage": 700000.00
      },
      "summary_text": {
        "project_name": "Project X"
      }
    },
    {
      "id": 58824,
      "project_id": 789,
      "vendor_name": "Ernie's Electrical",
      "invoice_number": "127",
      "total_claimed_amount": 550.00,
      "balance_amount": 650000.00,
      "billing_date": "2013-11-24",
      "summary": {
        "balance_to_finish_including_retainage": 650000.00
      },
      "summary_text": {
        "project_name": "Project X"
      }
    },
    {
      "id": 58825,
      "project_id": 789,
      "vendor_name": "Ernie's Electrical",
      "invoice_number": "128",
      "total_claimed_amount": 350.00,
      "balance_amount": 500000.00,
      "billing_date": "2013-11-25",
      "summary": {
        "balance_to_finish_including_retainage": 500000.00
      },
      "summary_text": {
        "project_name": "Project X"
      }
    },
    {
      "id": 58826,
      "project_id": 789,
      "vendor_name": "Ernie's Electrical",
      "invoice_number": "129",
      "total_claimed_amount": 450.00,
      "balance_amount": 400000.00,
      "billing_date": "2013-11-26",
      "summary": {
        "balance_to_finish_including_retainage": 400000.00
      },
      "summary_text": {
        "project_name": "Project X"
      }
    },
    {
      "id": 58827,
      "project_id": 789,
      "vendor_name": "Ernie's Electrical",
      "invoice_number": "130",
      "total_claimed_amount": 700.00,
      "balance_amount": 350000.00,
      "billing_date": "2013-11-27",
      "summary": {
        "balance_to_finish_including_retainage": 350000.00
      },
      "summary_text": {
        "project_name": "Project X"
      }
    },
    {
      "id": 58828,
      "project_id": 789,
      "vendor_name": "Ernie's Electrical",
      "invoice_number": "131",
      "total_claimed_amount": 800.00,
      "balance_amount": 300000.00,
      "billing_date": "2013-11-28",
      "summary": {
        "balance_to_finish_including_retainage": 300000.00
      },
      "summary_text": {
        "project_name": "Project X"
      }
    },
    {
      "id": 58829,
      "project_id": 789,
      "vendor_name": "Ernie's Electrical",
      "invoice_number": "132",
      "total_claimed_amount": 900.00,
      "balance_amount": 250000.00,
      "billing_date": "2013-11-29",
      "summary": {
        "balance_to_finish_including_retainage": 250000.00
      },
      "summary_text": {
        "project_name": "Project X"
      }
    },
    {
      "id": 58830,
      "project_id": 790,
      "vendor_name": "Lighting Solutions",
      "invoice_number": "133",
      "total_claimed_amount": 150.00,
      "balance_amount": 150000.00,
      "billing_date": "2013-11-20",
      "summary": {
        "balance_to_finish_including_retainage": 150000.00
      },
      "summary_text": {
        "project_name": "Project Y"
      }
    },
    {
      "id": 58831,
      "project_id": 790,
      "vendor_name": "Lighting Solutions",
      "invoice_number": "134",
      "total_claimed_amount": 200.00,
      "balance_amount": 140000.00,
      "billing_date": "2013-11-21",
      "summary": {
        "balance_to_finish_including_retainage": 140000.00
      },
      "summary_text": {
        "project_name": "Project Y"
      }
    },
    {
      "id": 58832,
      "project_id": 790,
      "vendor_name": "Lighting Solutions",
      "invoice_number": "135",
      "total_claimed_amount": 250.00,
      "balance_amount": 130000.00,
      "billing_date": "2013-11-22",
      "summary": {
        "balance_to_finish_including_retainage": 130000.00
      },
      "summary_text": {
        "project_name": "Project Y"
      }
    },
    {
      "id": 58833,
      "project_id": 790,
      "vendor_name": "Lighting Solutions",
      "invoice_number": "136",
      "total_claimed_amount": 300.00,
      "balance_amount": 120000.00,
      "billing_date": "2013-11-23",
      "summary": {
        "balance_to_finish_including_retainage": 120000.00
      },
      "summary_text": {
        "project_name": "Project Y"
      }
    },
    {
      "id": 58834,
      "project_id": 790,
      "vendor_name": "Lighting Solutions",
      "invoice_number": "137",
      "total_claimed_amount": 350.00,
      "balance_amount": 110000.00,
      "billing_date": "2013-11-24",
      "summary": {
        "balance_to_finish_including_retainage": 110000.00
      },
      "summary_text": {
        "project_name": "Project Y"
      }
    },
    {
      "id": 58835,
      "project_id": 790,
      "vendor_name": "Lighting Solutions",
      "invoice_number": "138",
      "total_claimed_amount": 400.00,
      "balance_amount": 100000.00,
      "billing_date": "2013-11-25",
      "summary": {
        "balance_to_finish_including_retainage": 100000.00
      },
      "summary_text": {
        "project_name": "Project Y"
      }
    },
    {
      "id": 58836,
      "project_id": 790,
      "vendor_name": "Lighting Solutions",
      "invoice_number": "139",
      "total_claimed_amount": 450.00,
      "balance_amount": 90000.00,
      "billing_date": "2013-11-26",
      "summary": {
        "balance_to_finish_including_retainage": 90000.00
      },
      "summary_text": {
        "project_name": "Project Y"
      }
    },
    {
      "id": 58837,
      "project_id": 790,
      "vendor_name": "Lighting Solutions",
      "invoice_number": "140",
      "total_claimed_amount": 500.00,
      "balance_amount": 80000.00,
      "billing_date": "2013-11-27",
      "summary": {
        "balance_to_finish_including_retainage": 80000.00
      },
      "summary_text": {
        "project_name": "Project Y"
      }
    },
    {
      "id": 58838,
      "project_id": 790,
      "vendor_name": "Lighting Solutions",
      "invoice_number": "141",
      "total_claimed_amount": 550.00,
      "balance_amount": 70000.00,
      "billing_date": "2013-11-28",
      "summary": {
        "balance_to_finish_including_retainage": 70000.00
      },
      "summary_text": {
        "project_name": "Project Y"
      }
    },
    {
      "id": 58839,
      "project_id": 790,
      "vendor_name": "Lighting Solutions",
      "invoice_number": "142",
      "total_claimed_amount": 600.00,
      "balance_amount": 60000.00,
      "billing_date": "2013-11-29",
      "summary": {
        "balance_to_finish_including_retainage": 60000.00
      },
      "summary_text": {
        "project_name": "Project Y"
      }
    },
    {
      "id": 58840,
      "project_id": 791,
      "vendor_name": "Acme Construction",
      "invoice_number": "143",
      "total_claimed_amount": 150.00,
      "balance_amount": 200000.00,
      "billing_date": "2013-11-20",
      "summary": {
        "balance_to_finish_including_retainage": 200000.00
      },
      "summary_text": {
        "project_name": "Project Z"
      }
    },
    {
      "id": 58841,
      "project_id": 791,
      "vendor_name": "Acme Construction",
      "invoice_number": "144",
      "total_claimed_amount": 200.00,
      "balance_amount": 180000.00,
      "billing_date": "2013-11-21",
      "summary": {
        "balance_to_finish_including_retainage": 180000.00
      },
      "summary_text": {
        "project_name": "Project Z"
      }
    },
    {
      "id": 58842,
      "project_id": 791,
      "vendor_name": "Acme Construction",
      "invoice_number": "145",
      "total_claimed_amount": 250.00,
      "balance_amount": 170000.00,
      "billing_date": "2013-11-22",
      "summary": {
        "balance_to_finish_including_retainage": 170000.00
      },
      "summary_text": {
        "project_name": "Project Z"
      }
    },
    {
      "id": 58843,
      "project_id": 791,
      "vendor_name": "Acme Construction",
      "invoice_number": "146",
      "total_claimed_amount": 300.00,
      "balance_amount": 160000.00,
      "billing_date": "2013-11-23",
      "summary": {
        "balance_to_finish_including_retainage": 160000.00
      },
      "summary_text": {
        "project_name": "Project Z"
      }
    },
    {
      "id": 58844,
      "project_id": 791,
      "vendor_name": "Acme Construction",
      "invoice_number": "147",
      "total_claimed_amount": 350.00,
      "balance_amount": 150000.00,
      "billing_date": "2013-11-24",
      "summary": {
        "balance_to_finish_including_retainage": 150000.00
      },
      "summary_text": {
        "project_name": "Project Z"
      }
    },
    {
      "id": 58845,
      "project_id": 791,
      "vendor_name": "Acme Construction",
      "invoice_number": "148",
      "total_claimed_amount": 400.00,
      "balance_amount": 140000.00,
      "billing_date": "2013-11-25",
      "summary": {
        "balance_to_finish_including_retainage": 140000.00
      },
      "summary_text": {
        "project_name": "Project Z"
      }
    },
    {
      "id": 58846,
      "project_id": 791,
      "vendor_name": "Acme Construction",
      "invoice_number": "149",
      "total_claimed_amount": 450.00,
      "balance_amount": 130000.00,
      "billing_date": "2013-11-26",
      "summary": {
        "balance_to_finish_including_retainage": 130000.00
      },
      "summary_text": {
        "project_name": "Project Z"
      }
    },
    {
      "id": 58847,
      "project_id": 791,
      "vendor_name": "Acme Construction",
      "invoice_number": "150",
      "total_claimed_amount": 500.00,
      "balance_amount": 120000.00,
      "billing_date": "2013-11-27",
      "summary": {
        "balance_to_finish_including_retainage": 120000.00
      },
      "summary_text": {
        "project_name": "Project Z"
      }
    },
    {
      "id": 58848,
      "project_id": 791,
      "vendor_name": "Acme Construction",
      "invoice_number": "151",
      "total_claimed_amount": 550.00,
      "balance_amount": 110000.00,
      "billing_date": "2013-11-28",
      "summary": {
        "balance_to_finish_including_retainage": 110000.00
      },
      "summary_text": {
        "project_name": "Project Z"
      }
    },
    {
      "id": 58849,
      "project_id": 791,
      "vendor_name": "Acme Construction",
      "invoice_number": "152",
      "total_claimed_amount": 600.00,
      "balance_amount": 100000.00,
      "billing_date": "2013-11-29",
      "summary": {
        "balance_to_finish_including_retainage": 100000.00
      },
      "summary_text": {
        "project_name": "Project Z"
      }
    }
  ]
}

```

**Response**:

```json
{"message": "Data uploaded successfully."}
```

---

### **2. Query Insights**

**Endpoint**: `/query`  
**Method**: `POST`  
**Description**: Accepts a natural language query and returns insights based on the invoice data.

**Request Body Example**:

```json
{
  "natural_query": "List down the top 5 invoices for Project X"
}
```

**Response Example**:

```json
{
    "result": "Top 5 invoices for project 'Project X' retrieved successfully.",
    "details": [
        {
            "Invoice ID": 58829,
            "Vendor Name": "Ernie's Electrical",
            "Invoice Amount": 900.0
        },
        {
            "Invoice ID": 58828,
            "Vendor Name": "Ernie's Electrical",
            "Invoice Amount": 800.0
        },
        {
            "Invoice ID": 58827,
            "Vendor Name": "Ernie's Electrical",
            "Invoice Amount": 700.0
        },
        {
            "Invoice ID": 58823,
            "Vendor Name": "Ernie's Electrical",
            "Invoice Amount": 600.0
        },
        {
            "Invoice ID": 58824,
            "Vendor Name": "Ernie's Electrical",
            "Invoice Amount": 550.0
        }
    ]
}
```

**Out-of-Scope Example**:

```json
{
  "natural_query": "What's the current score of the match?"
}
```

**Response**:

```json
{
    "result": "I'm sorry, but I am not able to provide real-time updates on sports scores. You may want to check a sports website or app for the most up-to-date information on the match you are interested in.",
    "details": []
}
```

---

### **3. Get Highest Balance Invoice**

**Endpoint**: `/query`  
**Method**: `POST` 
**Description**: Returns the invoice with the highest balance amount.

**Request Body Example**:

```json
{
  "natural_query": "Show me the summary of the Invoice which has the highest balance"
}
```


**Response Example**:

```json
{
  "result": "Invoice with the highest balance retrieved successfully.",
  "details": [
    {
      "invoice_id": 58820,
      "vendor_name": "Ernie's Electrical",
      "balance": 1268346.55
    }
  ]
}
```

---

## **Setup and Installation**

### **1. Clone the Repository**

```bash
git clone https://github.com/your-username/BUILDING_AN_INSIGHTS_AGENT.git
cd BUILDING_AN_INSIGHTS_AGENT
```

### **2. Create and Activate a Virtual Environment**

```bash
python -m venv venv
# Activate on Windows
venv\Scripts\activate
# Activate on macOS/Linux
source venv/bin/activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Set Up OpenAI API Key**

Replace `"YOUR_OPENAI_API_KEY"` in `app.py` with your actual OpenAI API key:

```python
OPENAI_API_KEY = "your-api-key-here"
```

Alternatively, use environment variables for security:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### **5. Run the Server**

```bash
uvicorn app:app --reload
```

### **6. Access the API**

Open your browser and navigate to:

- **Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## **Testing the API**

### **Using Curl**

1. **Upload Data**

   ```bash
   curl -X POST "http://127.0.0.1:8000/upload-data" -H "Content-Type: application/json" -d '{
     "data": [
       {
         "id": 58820,
         "project_id": 789,
         "vendor_name": "Ernie's Electrical",
         "invoice_number": "123",
         "total_claimed_amount": 23000.00,
         "summary": {
           "balance_to_finish_including_retainage": 1268346.55
         },
         "billing_date": "2023-11-20",
         "summary_text": {
           "project_name": "Project X"
         }
       }
     ]
   }'
   ```

2. **Query for Top Invoices**

   ```bash
   curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d '{"natural_query": "List down the top 5 invoices for Project X"}'
   ```

---

## **Future Enhancements**

1. **Add Authentication**: Secure the endpoints with authentication tokens (e.g., JWT).
2. **Pagination**: Implement pagination for large datasets.
3. **More Query Types**: Add more capabilities for querying different insights.
4. **Error Logging**: Integrate logging for better error tracking.
5. **Frontend**: Develop a frontend interface for interacting with the API.

---

## **License**

This project is licensed under the **MIT License**.

---

## **Contributing**

Contributions are welcome! Please open an issue or submit a pull request.
