data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "document_platform_dev" {

  bucket = "document-platform-${var.environment}-${data.aws_caller_identity.current.account_id}"

}

data "aws_ami" "ubuntu" {
  most_recent = true

  owners = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_dynamodb_table" "users" {

  name         = "users-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "username"

  attribute {
    name = "username"
    type = "S"
  }

}

resource "aws_dynamodb_table" "files" {

  name         = "files-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "file_id"

  attribute {
    name = "file_id"
    type = "S"
  }

  attribute {
    name = "department"
    type = "S"
  }

  attribute {
    name = "uploaded_at"
    type = "S"
  }

  global_secondary_index {

    name            = "department-index"
    hash_key        = "department"
    range_key       = "uploaded_at"
    projection_type = "ALL"

  }

}

resource "aws_dynamodb_table" "audit_logs" {

  name         = "audit_logs-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "username"
  range_key = "timestamp"

  attribute {
    name = "username"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  attribute {
    name = "department"
    type = "S"
  }

  global_secondary_index {

    name            = "department-index"
    hash_key        = "department"
    range_key       = "timestamp"
    projection_type = "ALL"

  }

}

resource "aws_iam_role" "document_platform_role" {

  name = "document-platform-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

}
resource "aws_iam_policy" "document_platform_policy" {

  name = "document-platform-policy-${var.environment}"

  policy = jsonencode({

    Version = "2012-10-17"

    Statement = [

      {
        Effect = "Allow"

        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]

        Resource = [
          "${aws_s3_bucket.document_platform_dev.arn}/*"
        ]
      },

      {
        Effect = "Allow"

        Action = [
          "s3:ListBucket"
        ]

        Resource = [
          aws_s3_bucket.document_platform_dev.arn
        ]
      },

      {
        Effect = "Allow"

        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]

        Resource = [
          aws_dynamodb_table.users.arn,
          aws_dynamodb_table.files.arn,
          aws_dynamodb_table.audit_logs.arn,

          "${aws_dynamodb_table.files.arn}/index/*",
          "${aws_dynamodb_table.audit_logs.arn}/index/*"
        ]
      }

    ]
  })
}

resource "aws_iam_role_policy_attachment" "document_platform_attachment" {

  role = aws_iam_role.document_platform_role.name

  policy_arn = aws_iam_policy.document_platform_policy.arn

}

resource "aws_iam_instance_profile" "document_platform_profile" {
  name = "document-platform-profile-dev"
  role = aws_iam_role.document_platform_role.name
}

resource "aws_iam_role_policy_attachment" "ssm_core" {
  role       = aws_iam_role.document_platform_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_security_group" "document_platform_sg" {
  name        = "document-platform-sg-dev"
  description = "SSM only access"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "document_platform" {

  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.small"

  iam_instance_profile = aws_iam_instance_profile.document_platform_profile.name

  vpc_security_group_ids = [
    aws_security_group.document_platform_sg.id
  ]
  
  user_data = templatefile(
    "${path.module}/userdata.sh.tpl",
    {
      flask_secret_key = var.flask_secret_key
    }
  ) 

  tags = {
    Name = "document-platform-dev"
  }
}
