# scripts/lambda_trigger.py

from dotenv import load_dotenv
import boto3
import json
import os
import base64
import requests

# Load environment variables from the .env file at the project root
load_dotenv()

# Retrieve AWS region from environment variables, defaulting to ap-southeast-2
AWS_REGION = os.getenv('AWS_REGION', 'ap-southeast-2')

def get_secrets():
    # Initialize the Secrets Manager client with the specified region
    secrets_client = boto3.client('secretsmanager', region_name=AWS_REGION)
    secret_name = "api_secrets"  # Replace with the actual secret name in Secrets Manager

    try:
        # Retrieve the secret
        response = secrets_client.get_secret_value(SecretId=secret_name)
        secret_data = json.loads(response['SecretString'])
        
        # Extract API_KEY and API_SECRET
        api_key = secret_data.get("API_KEY")
        api_secret = secret_data.get("API_SECRET")
        
        return api_key, api_secret, secret_name
    except Exception as e:
        print("Error fetching secrets:", e)
        return None, None, None

def get_access_token(api_key, api_secret):
    url = "https://api.onegov.nsw.gov.au/oauth/client_credential/accesstoken"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{api_key}:{api_secret}".encode("utf-8")).decode("utf-8"),
    }
    params = {
        "grant_type": "client_credentials"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()
        if response.status_code == 200:
            access_token = response_data.get("access_token")
            print("Access Token:", access_token)
            return access_token
        else:
            print("Failed to retrieve access token:", response_data)
            return None
    except Exception as e:
        print("Error in API call:", e)
        return None

def update_secret_with_access_token(secret_name, api_key, api_secret, access_token):
    secrets_client = boto3.client('secretsmanager', region_name=AWS_REGION)
    try:
        # Prepare updated secret data
        updated_secret = {
            "API_KEY": api_key,
            "API_SECRET": api_secret,
            "ACCESS_TOKEN": access_token
        }
        
        # Update the secret in Secrets Manager
        secrets_client.put_secret_value(
            SecretId=secret_name,
            SecretString=json.dumps(updated_secret)
        )
        print("Secret updated with access token.")
    except Exception as e:
        print("Error updating secret:", e)

def lambda_handler(event, context):
    # Fetch the secrets (API_KEY and API_SECRET)
    api_key, api_secret, secret_name = get_secrets()
    if not api_key or not api_secret:
        return {
            'statusCode': 500,
            'body': 'Failed to retrieve API credentials'
        }

    # Fetch the access token
    access_token = get_access_token(api_key, api_secret)
    if not access_token:
        return {
            'statusCode': 500,
            'body': 'Failed to retrieve access token'
        }

    # Update the secret with the access token
    update_secret_with_access_token(secret_name, api_key, api_secret, access_token)

    return {
        'statusCode': 200,
        'body': 'Lambda executed and access token retrieved and stored successfully'
    }
