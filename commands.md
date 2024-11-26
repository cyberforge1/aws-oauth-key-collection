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

zip -j zipped_lambda_functions/lambda_trigger.zip lambda_trigger/lambda_trigger.py

zip -r zipped_lambda_functions/lambda_api_test_call.zip lambda_api_test_call/



## Trigger

python scripts/invoke_lambda_trigger.py




# Dependency Installation

pip install requests -t lambda_test_api_call/
