output "users_table_name" {

  description = "Users table name"

  value = aws_dynamodb_table.users.name

}

output "files_table_name" {

  description = "Files table name"

  value = aws_dynamodb_table.files.name

}

output "audit_logs_table_name" {

  description = "Audit logs table name"

  value = aws_dynamodb_table.audit_logs.name

}

output "document_bucket_name" {

  description = "Document storage bucket"

  value = aws_s3_bucket.document_platform_dev.bucket

}

output "instance_id" {
  value = aws_instance.document_platform.id
}

output "public_ip" {
  value = aws_instance.document_platform.public_ip
}

output "ssm_connect_command" {
  value = "aws ssm start-session --target ${aws_instance.document_platform.id}"
}
