import boto3
import json
from rich.console import Console

console = Console()

def execute_aws_strike(severity):
    config = boto3.session.Config(connect_timeout=2, read_timeout=2, retries={'max_attempts': 0})
    # Swapped to Moto on port 5000
    s3 = boto3.client('s3', endpoint_url='http://localhost:5000', aws_access_key_id='test', aws_secret_access_key='test', region_name='us-east-1', config=config)
    
    try:
        buckets = s3.list_buckets().get('Buckets', [])
        if not buckets:
            console.print("[bold yellow][!] No S3 buckets found. Create one first to attack it.[/bold yellow]")
            return
        
        target_bucket = buckets[0]['Name']
        console.print(f"[bold red][☠️] Target acquired: Cloud S3 Bucket '{target_bucket}'[/bold red]")
        
        if severity == "high":
            console.print(f"[bold red][*] Action (HIGH): Injecting DenyAll IAM Policy to '{target_bucket}'...[/bold red]")
            deny_policy = {
                "Version": "2012-10-17",
                "Statement": [{
                    "Sid": "ChaosStrikeDeny",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:*",
                    "Resource": [f"arn:aws:s3:::{target_bucket}", f"arn:aws:s3:::{target_bucket}/*"]
                }]
            }
            s3.put_bucket_policy(Bucket=target_bucket, Policy=json.dumps(deny_policy))
            console.print(f"[bold green][✔] S3 Bucket '{target_bucket}' is now locked down (Access Denied).[/bold green]")
        else:
            console.print(f"[yellow][*] Action ({severity.upper()}): Only HIGH severity implemented for AWS in this demo.[/yellow]")
            
    except Exception as e:
        console.print("[bold red][X] Cloud Emulation Offline: Could not connect to Moto on port 5000.[/bold red]")
        console.print(f"[italic yellow]Error details: {e}[/italic yellow]")
