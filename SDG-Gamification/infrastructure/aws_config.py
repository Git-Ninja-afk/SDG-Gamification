import json

# AWS RDS Configuration
RDS_CONFIG = {
    "DBInstanceIdentifier": "gamify-sdg-db",
    "Engine": "postgres",
    "EngineVersion": "15.3",
    "DBInstanceClass": "db.t3.micro",
    "AllocatedStorage": 20,
    "StorageType": "gp3",
    "MasterUsername": "admin",
    "DBName": "gamify_sdg",
    "VpcSecurityGroupIds": ["sg-xxxxx"],
    "BackupRetentionPeriod": 30,
    "MultiAZ": True,
    "EnableCloudwatchLogsExports": ["postgresql"],
}

# AWS S3 Configuration
S3_CONFIG = {
    "Bucket": "gamify-sdg-bucket",
    "Region": "ap-south-1",
    "PublicAccessBlockConfiguration": {
        "BlockPublicAcls": True,
        "IgnorePublicAcls": True,
        "BlockPublicPolicy": True,
        "RestrictPublicBuckets": True,
    },
    "VersioningConfiguration": {
        "Status": "Enabled"
    },
}

# AWS ElastiCache (Redis) Configuration
ELASTICACHE_CONFIG = {
    "CacheClusterId": "gamify-sdg-redis",
    "Engine": "redis",
    "EngineVersion": "7.0",
    "CacheNodeType": "cache.t3.micro",
    "NumCacheNodes": 1,
    "AutomaticFailoverEnabled": False,
}

# AWS Lambda Configuration for task verification
LAMBDA_CONFIG = {
    "FunctionName": "gamify-sdg-task-verification",
    "Runtime": "python3.11",
    "Timeout": 60,
    "MemorySize": 512,
    "Environment": {
        "Variables": {
            "DATABASE_URL": "${RDS_ENDPOINT}",
            "BUCKET_NAME": "gamify-sdg-bucket",
        }
    },
}

# AWS CloudFront Configuration
CLOUDFRONT_CONFIG = {
    "OriginDomainName": "gamify-sdg-bucket.s3.ap-south-1.amazonaws.com",
    "DefaultCacheBehavior": {
        "TargetOriginId": "S3Origin",
        "ViewerProtocolPolicy": "redirect-to-https",
        "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",
    },
    "PriceClass": "PriceClass_100",
}

# AWS Application Load Balancer Configuration
ALB_CONFIG = {
    "Name": "gamify-sdg-alb",
    "Subnets": ["subnet-xxxxx", "subnet-yyyyy"],
    "SecurityGroups": ["sg-xxxxx"],
    "Scheme": "internet-facing",
    "Type": "application",
}

# Deployment configuration
DEPLOYMENT_SETTINGS = {
    "region": "ap-south-1",
    "environment": "production",
    "min_instances": 2,
    "max_instances": 10,
    "cpu_threshold": 70,
    "memory_threshold": 80,
}

print("AWS Infrastructure Configuration")
print(json.dumps(RDS_CONFIG, indent=2))
