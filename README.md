# AWS Sales Data Engineering Pipeline

## Project Overview
An automated sales data pipeline built using Python and AWS services.

## Technologies Used
- Python
- Pandas
- Amazon S3
- AWS Lambda
- Amazon Athena
- SQL
- Git and GitHub

## Pipeline Workflow
1. Upload raw sales CSV files to Amazon S3.
2. S3 triggers AWS Lambda when a CSV is uploaded to raw/.
3. Lambda calculates total_amount and saves the processed CSV to processed/.
4. Athena queries the processed sales data.
5. SQL analyzes sales by city, product, and date.

## Key Features
- Automated CSV processing
- Raw and processed data storage
- Event-driven serverless processing
- SQL-based sales analysis

## Project Structure
- scripts/transform.py
- .gitignore
- README.md

## Note
This is a learning project using sample sales data.
