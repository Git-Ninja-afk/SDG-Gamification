"""
AWS CDK Infrastructure as Code for Gamify SDG Platform
"""
from aws_cdk import (
    core,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_elasticache as elasticache,
    aws_iam as iam,
)

class GameifySdgStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # VPC
        vpc = ec2.Vpc(
            self,
            "GameifyVPC",
            cidr="10.0.0.0/16",
            max_azs=2,
            nat_gateways=1,
        )

        # RDS PostgreSQL Database
        db_instance = rds.DatabaseInstance(
            self,
            "GameifyDB",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15_3
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            database_name="gamify_sdg",
            allocated_storage=20,
            multi_az=True,
            deletion_protection=True,
            backup_retention=core.Duration.days(30),
            publicly_accessible=False,
        )

        # S3 Bucket for user uploads
        s3_bucket = s3.Bucket(
            self,
            "GameifyBucket",
            bucket_name="gamify-sdg-bucket",
            versioned=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True,
            ),
            encryption=s3.BucketEncryption.KMS,
        )

        # Security Group for backend
        backend_sg = ec2.SecurityGroup(
            self,
            "BackendSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
        )
        backend_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(8000),
            description="Allow HTTP traffic to backend",
        )
        backend_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443),
            description="Allow HTTPS traffic",
        )

        # Output database endpoint
        core.CfnOutput(
            self,
            "DatabaseEndpoint",
            value=db_instance.db_instance_endpoint_address,
            description="RDS database endpoint",
        )

        # Output S3 bucket name
        core.CfnOutput(
            self,
            "S3BucketName",
            value=s3_bucket.bucket_name,
            description="S3 bucket for user uploads",
        )


class GameifySdgApp(core.App):
    def __init__(self):
        super().__init__()
        GameifySdgStack(self, "GameifySdg", env=core.Environment(
            account="123456789012",
            region="ap-south-1"
        ))


app = GameifySdgApp()
app.synth()
