-- 1. Take data from CSV and write it to a persistent database table
CREATE TABLE IF NOT EXISTS loan_data AS 
SELECT * FROM read_csv('data.csv', nullstr=['', '..']);

-- 2. Add a table named "users" to the database
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR,
    age INTEGER,
    country VARCHAR
);