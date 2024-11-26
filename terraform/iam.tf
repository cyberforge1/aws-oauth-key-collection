# terraform/iam.tf

resource "aws_iam_role" "lambda_execution_role" {
  name = "LambdaExecutionRole"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_execution_policy" {
  name        = "LambdaExecutionPolicy"
  description = "Policy to allow Lambda to write to CloudWatch logs and access Secrets Manager"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        # Permissions for CloudWatch Logs
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*"
      },
      {
        # Permissions to get and put the secret value
        "Effect": "Allow",
        "Action": [
          "secretsmanager:GetSecretValue",
          "secretsmanager:PutSecretValue"
        ],
        "Resource": "arn:aws:secretsmanager:${var.CUSTOM_AWS_REGION}:${var.AWS_ACCOUNT_ID}:secret:${var.SECRET_NAME}*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_execution_policy.arn
}
