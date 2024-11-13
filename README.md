# AWS OAuth Key Collection

## Project Overview
A scheduled Airflow DAG automates a data pipeline on AWS. It retrieves an access token using AWS Lambda and Secrets Manager, then makes API calls to fetch data. The data is processed, stored securely in S3, and notifications are sent via SNS for monitoring.

## Screenshot
![Project Diagram](diagrams/aws-oauth-key-collection-diagram-dark.png "AWS OAuth Key Collection Architecture")