output "vpc_id" {
  description = "ID of the CloudOps VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value = [
    aws_subnet.public.id,
    aws_subnet.public_2.id
  ]
}

output "ecr_repository_url" {
  description = "URL of the backend ECR repository"
  value       = aws_ecr_repository.backend.repository_url
}