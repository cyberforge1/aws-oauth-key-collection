# terraform/lambda.tf

resource "aws_lambda_function" "lambda_trigger" {
  function_name    = "lambda_trigger"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "lambda_trigger.lambda_handler"
  runtime          = "python3.8"
  filename         = "../zipped_lambda_functions/lambda_trigger.zip"
  source_code_hash = filebase64sha256("../zipped_lambda_functions/lambda_trigger.zip")

  environment {
    variables = {
      # Add any necessary environment variables here
    }
  }

  tags = {
    Environment = "production"
  }
}
