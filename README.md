# 🏒 Toronto Maple Leafs Data Ingestion and Database Pipeline

This Python project fetches and stores up-to-date data on the **Toronto Maple Leafs** using a sports information API. This project was built to understand elements of Flask and implement in a fun and data-friendly way to stay up to date on my personal favourite hockey team!

## 📌 Features

- Ingests data from data_ingestion.py using the Sports Information API on RapidAPI
- Cleans the data in data_processing.py, allowing for database handling to take place
- Full database functionality implemented in database.py using SQLAlchemy and Flask
- These 3 steps break down the pipeline into modular portions for debugging and maintainability purposes

## 🚀 Getting Started

Install any necessary dependencies with requirements.txt:

pip install -r requirements.txt

Use the CRUD operations built into database.py to update the PlayerModel database attribute as needed.

For general database population, use main.py to ingest and clean data and then populate the database.

**PLEASE NOTE**
RapidAPI can be used for free with a limited amount of API calls per month. Do not ingest more data than allowed in your month please!