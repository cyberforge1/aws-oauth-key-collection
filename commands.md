# COMMANDS

## VENV

source venv/bin/activate

pip freeze > requirements.txt

pip install -r requirements.txt


## Terraform

cd terraform

terraform plan

export $(cat .env | xargs)
terraform apply

terraform destroy

## Zip Lambda functions

zip -r zipped_lambda_functions/lambda_trigger.zip lambda_functions/lambda_trigger


## Basic Checks



## Trigger
python scripts/invoke.lambda.py
