# terraform/lambda.tf

resource "aws_lambda_function" "lambda_trigger" {
  function_name    = "lambda_trigger"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "lambda_trigger.lambda_handler"  # Remains the same since the file name didn't change
  runtime          = "python3.8"
  filename         = "${path.module}/../zipped_lambda_functions/lambda_trigger.zip"
  source_code_hash = filebase64sha256("${path.module}/../zipped_lambda_functions/lambda_trigger.zip")

  environment {
    variables = {
      CUSTOM_AWS_REGION = var.CUSTOM_AWS_REGION
      SECRET_NAME       = "api_secrets"
    }
  }

  tags = {
    Environment = "production"
  }
}
