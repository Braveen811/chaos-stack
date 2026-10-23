import argparse
import boto3
from rich.console import Console
from rich.panel import Panel
from attacks.docker_strike import execute_docker_strike
from attacks.aws_strike import execute_aws_strike
from attacks.network_strike import execute_network_strike
from analytics.logger import log_strike, show_report

console = Console()

def print_banner():
    banner = """
[bold red]⚠️  CHAOS-STACK[/bold red]
[yellow]LocalStack AWS & Docker Chaos Engineering CLI[/yellow]
    """
    console.print(Panel(banner, border_style="red", expand=False))

def heal_aws():
    try:
        s3 = boto3.client('s3', endpoint_url='http://localhost:5000', aws_access_key_id='test', aws_secret_access_key='test', region_name='us-east-1')
        buckets = s3.list_buckets().get('Buckets', [])
        for bucket in buckets:
            bucket_name = bucket['Name']
            s3.delete_bucket_policy(Bucket=bucket_name)
            console.print(f"[bold green][✔] Removed DenyAll policy from S3 bucket: {bucket_name}[/bold green]")
    except Exception as e:
        console.print(f"[bold yellow][!] Could not heal AWS: {e}[/bold yellow]")

def main():
    parser = argparse.ArgumentParser(description="Inject chaos into LocalStack and Docker.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    strike_parser = subparsers.add_parser("strike", help="Inject a fault into the architecture")
    strike_parser.add_argument("--target", choices=["docker", "aws", "network"], required=True, help="Target layer")
    strike_parser.add_argument("--severity", choices=["low", "medium", "high"], default="low", help="Blast radius")

    subparsers.add_parser("heal", help="Remove all injected faults and restore state")
    subparsers.add_parser("report", help="Show DuckDB resilience analytics")

    args = parser.parse_args()

    if getattr(args, 'command', None) is None:
        print_banner()
        parser.print_help()
        return

    print_banner()

    if args.command == "strike":
        console.print(f"[bold red][*] Initiating {args.severity.upper()} severity strike on {args.target.upper()}...[/bold red]")
        
        if args.target == "docker":
            execute_docker_strike(args.severity)
        elif args.target == "aws":
            execute_aws_strike(args.severity)
        elif args.target == "network":
            execute_network_strike(args.severity)
            
        log_strike(args.target, args.severity)
            
    elif args.command == "heal":
        console.print("[bold green][*] Reversing all chaos injections. System healing...[/bold green]")
        heal_aws()
        
    elif args.command == "report":
        show_report()

if __name__ == "__main__":
    main()
