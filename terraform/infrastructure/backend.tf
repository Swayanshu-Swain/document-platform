terraform {
  backend "s3" {
    bucket         = "terraform-state-006870473063"
    key            = "document-platform/dev/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraform-locks"
  }
}
