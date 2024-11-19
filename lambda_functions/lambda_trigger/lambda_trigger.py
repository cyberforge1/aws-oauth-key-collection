# lambda_functions/lambda_trigger/lambda_trigger.py

import boto3
import json
import os

def get_secrets():
    # Retrieve the region from the custom environment variable
    aws_region = os.getenv('CUSTOM_AWS_REGION', 'ap-southeast-2')  # Default to ap-southeast-2
    secret_name = os.getenv('SECRET_NAME')  # Fetch the secret name from environment variable
    print(f"Debug: AWS_REGION resolved to {aws_region}")
    print(f"Debug: SECRET_NAME resolved to {secret_name}")
    
    secrets_client = boto3.client('secretsmanager', region_name=aws_region)

    try:
        # Retrieve the secret
        response = secrets_client.get_secret_value(SecretId=secret_name)
        print(f"Debug: Secrets Manager response: {response}")
        
        secret_data = json.loads(response['SecretString'])
        print("Debug: Parsed secret data successfully.")
        
        # Extract API_KEY and API_SECRET
        api_key = secret_data.get("API_KEY")
        api_secret = secret_data.get("API_SECRET")
        print(f"Debug: Extracted API_KEY: {api_key}, API_SECRET: {api_secret}")

        return api_key, api_secret
    except Exception as e:
        print(f"Error: Failed to fetch secrets. Exception: {e}")
        return None, None

def lambda_handler(event, context):
    print("Lambda function started.")
    print(f"Debug: Event received: {event}")
    
    # Fetch and print secrets
    api_key, api_secret = get_secrets()
    if api_key and api_secret:
        print("Debug: Successfully retrieved and printed secrets.")
        print("API_KEY:", api_key)
        print("API_SECRET:", api_secret)
    else:
        print("Error: Failed to fetch secrets.")
    
    return {
        'statusCode': 200,
        'body': 'Lambda executed and secrets accessed successfully'
    }
