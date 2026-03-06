# Loan Data API

This is a RESTful API built with Flask that provides access to the Kiva Loans dataset. It follows **Documentation-Driven Development** principles and utilizes a **DuckDB persistent database** for efficient data querying and storage.

## Dataset & Database
The API is powered by a DuckDB database (`my_database.db`). The core loan data is initialized from `data.csv`, containing loan applications with unique identifiers (`id`), borrower names, sectors, countries, and loan amounts. It also features a `users` table to track API consumers.

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-folder>
    ```

2.  **Install dependencies:**
    You need Python 3 installed. Then run:
    ```bash
    pip install flask pandas duckdb
    ```

3.  **Initialize the database:**
    Before running the API for the first time, you must create the persistent database and load the initial data.
    ```bash
    python init_db.py
    ```
    *(This will generate a `my_database.db` file in your directory).*

4.  **Run the application:**
    ```bash
    python api.py
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
| `<column>` | `string` | - | Filter by any column (e.g., `country=Peru`, `sector=Agriculture`). |

#### Filter Examples

**Filter by specific column (e.g., Country):**
> `GET /data?country=Peru`

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

#### Example
**Get details for loan ID 350525:**
> `GET /data/350525`

---

### 3. Add a New User
Add a new user to the persistent database.

* **Endpoint:** `/users`
* **Method:** `POST`
* **Headers:** `Content-Type: application/json`

#### Request Body (JSON)
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `username` | `string` | Yes | The chosen username. |
| `age` | `int` | Yes | The user's age. |
| `country` | `string` | Yes | The user's country of residence. |

#### Example cURL Request:
```bash
curl -X POST [http://127.0.0.1:5000/users](http://127.0.0.1:5000/users) \
-H "Content-Type: application/json" \
-d '{"username":"alex", "age":25, "country":"USA"}'