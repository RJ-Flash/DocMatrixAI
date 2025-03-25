provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "./modules/vpc"
  # VPC configuration
}

module "eks" {
  source = "./modules/eks"
  # EKS configuration
}

module "rds" {
  source = "./modules/rds"
  # RDS configuration
}
