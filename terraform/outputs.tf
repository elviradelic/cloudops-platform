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