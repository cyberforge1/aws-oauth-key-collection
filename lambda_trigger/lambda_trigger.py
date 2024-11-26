# /lambda_trigger/lambda_trigger.py

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

        return secret_data  # Return the entire secret data
    except Exception as e:
        print(f"Error: Failed to fetch secrets. Exception: {e}")
        return None

def update_secret(secret_data):
    # Retrieve the region and secret name from environment variables
    aws_region = os.getenv('CUSTOM_AWS_REGION', 'ap-southeast-2')
    secret_name = os.getenv('SECRET_NAME')
    ACCESS_TOKEN_value = 'pVqXLoW3T$!jRV'

    secrets_client = boto3.client('secretsmanager', region_name=aws_region)

    if 'ACCESS_TOKEN' in secret_data:
        print("ACCESS_TOKEN already exists in the secret.")
        return {
            'statusCode': 200,
            'body': 'ACCESS_TOKEN already exists in the secret.'
        }
    else:
        # Add 'ACCESS_TOKEN' to the secret
        secret_data['ACCESS_TOKEN'] = ACCESS_TOKEN_value

        try:
            # Update the secret in Secrets Manager
            secrets_client.put_secret_value(
                SecretId=secret_name,
                SecretString=json.dumps(secret_data)
            )
            print("ACCESS_TOKEN added to the secret successfully.")
            return {
                'statusCode': 200,
                'body': 'ACCESS_TOKEN added to the secret successfully.'
            }
        except Exception as e:
            print(f"Error updating secret: {e}")
            return {
                'statusCode': 500,
                'body': f"Error updating secret: {e}"
            }

def lambda_handler(event, context):
    print("Lambda function started.")
    print(f"Debug: Event received: {event}")
    
    # Fetch secrets
    secret_data = get_secrets()
    if secret_data:
        print("Debug: Successfully retrieved secrets.")
        # Extract API_KEY and API_SECRET
        api_key = secret_data.get("API_KEY")
        api_secret = secret_data.get("API_SECRET")
        print(f"Debug: Extracted API_KEY: {api_key}, API_SECRET: {api_secret}")
        print("API_KEY:", api_key)
        print("API_SECRET:", api_secret)

        # Update the secret with 'ACCESS_TOKEN' if needed
        result = update_secret(secret_data)
        return result
    else:
        print("Error: Failed to fetch secrets.")
        return {
            'statusCode': 500,
            'body': 'Failed to fetch secrets.'
        }
