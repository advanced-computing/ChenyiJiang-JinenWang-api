# Loan Data API

This is a simple RESTful API built with Flask that provides access to the Kiva Loans dataset. It follows **Documentation-Driven Development** principles.

## Dataset
The API is powered by `data.csv`, containing loan applications with unique identifiers (`id`), borrower names, sectors, countries, and loan amounts.

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-folder>
    ```

2.  **Install dependencies:**
    You need Python 3 installed. Then run:
    ```bash
    pip install flask pandas
    ```

3.  **Run the application:**
    ```bash
    python app.py
    ```
    The API will start at `http://127.0.0.1:5000/`.

---

## API Documentation

### 1. List & Filter Records
Retrieve a list of loans. You can filter by column, paginate results, and choose the output format (JSON or CSV).

* **Endpoint:** `/data`
* **Method:** `GET`

#### Query Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `limit` | `int` | `10000` | Number of records to return. |
| `offset` | `int` | `0` | Number of records to skip (pagination). |
| `format` | `string` | `json` | Output format: `json` or `csv`. |
| `<column>` | `string` | - | Filter by any column (e.g., `country=Peru`, `age=30`). |

#### Filter Examples

**Filter by specific column (e.g., Country):**
> `GET /data?country=Peru`

**Filter by numerical value (e.g., Loan Amount):**
> `GET /data?loan_amount=575`

**Combined Filter (Sector + Country):**
> `GET /data?sector=Agriculture&country=Kenya`

**Pagination (Limit & Offset):**
> `GET /data?limit=5&offset=10`

**Download as CSV:**
> `GET /data?format=csv`

---

### 2. Retrieve Single Record
Retrieve details for a specific loan by its unique ID.

* **Endpoint:** `/data/<id>`
* **Method:** `GET`

#### Parameters
* `id`: The unique identifier of the loan (e.g., `350525`).

#### Example

**Get details for loan ID 350525:**
> `GET /data/350525`

**Response (JSON):**
```json
[
  {
    "id": 350525,
    "name": "Jovita",
    "gender": "F",
    "loan_amount": 575,
    "activity": "Agriculture",
    "sector": "Agriculture",
    "country": "Peru",
    ...
  }
]