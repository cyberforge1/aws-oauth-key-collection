# lambda_functions/lambda_trigger.py

import boto3
import json
import os

def get_secrets():
    # Initialize the Secrets Manager client
    secrets_client = boto3.client('secretsmanager', region_name=os.getenv('AWS_REGION', 'us-west-2'))
    secret_name = "api_secrets"  # Replace with the actual secret name in Secrets Manager

    try:
        # Retrieve the secret
        response = secrets_client.get_secret_value(SecretId=secret_name)
        secret_data = json.loads(response['SecretString'])
        
        # Extract API_KEY and API_SECRET
        api_key = secret_data.get("API_KEY")
        api_secret = secret_data.get("API_SECRET")
        
        print("API_KEY:", api_key)
        print("API_SECRET:", api_secret)
    except Exception as e:
        print("Error fetching secrets:", e)

def lambda_handler(event, context):
    print("Lambda function started.")
    get_secrets()  # Fetch and print secrets
    return {
        'statusCode': 200,
        'body': 'Lambda executed and secrets accessed successfully'
    }
