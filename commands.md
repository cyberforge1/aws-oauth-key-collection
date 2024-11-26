# COMMANDS

## VENV

source venv/bin/activate

pip freeze > requirements.txt

pip install -r requirements.txt


## Terraform

terraform -chdir=terraform plan

terraform -chdir=terraform apply

terraform -chdir=terraform destroy

## Zip Lambda functions

zip -r zipped_lambda_functions/lambda_trigger.zip lambda_trigger/

zip -r zipped_lambda_functions/lambda_api_test_call.zip lambda_test_api_call/


## Trigger

python scripts/invoke_lambda.py



# Dependency Installation

pip install requests -t lambda_test_api_call/
