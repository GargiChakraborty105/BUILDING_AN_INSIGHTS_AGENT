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
  "natural_query": "List down the top 5 invoices for Project X."
}
```

**Response Example**:

```json
{
  "result": "Query executed successfully.",
  "details": [
    {
      "invoice_id": 58820,
      "vendor_name": "Ernie's Electrical",
      "amount": 23000.00
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
  "result": "Sorry, I cannot provide sports scores or game updates."
}
```

---

### **3. Get Highest Balance Invoice**

**Endpoint**: `/invoices/highest-balance`  
**Method**: `GET`  
**Description**: Returns the invoice with the highest balance amount.

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
   curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d '{"natural_query": "List down the top 5 invoices for Project X."}'
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
