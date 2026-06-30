8d6259bvariable "aws_region" {
  description = "AWS region for resources"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "flask_secret_key" {
  type      = string
  sensitive = true
}

variable "image_tag" {
  default = "8d6259b"
}
