import docker
import random
from rich.console import Console

console = Console()

def execute_network_strike(severity):
    try:
        client = docker.from_env()
        containers = client.containers.list()
        
        if not containers:
            console.print("[bold yellow][!] No running Docker containers found for network strike.[/bold yellow]")
            return

        victim = random.choice(containers)
        console.print(f"[bold red][☠️] Target acquired for Network Chaos: {victim.name}[/bold red]")

        latency = "1000ms" if severity == "high" else "200ms"
        console.print(f"[yellow][*] Action: Injecting {latency} network latency into {victim.name}...[/yellow]")
        
        exit_code, output = victim.exec_run(f"tc qdisc add dev eth0 root netem delay {latency}", user="root")
        
        if exit_code == 0 or b"File exists" in output:
            console.print(f"[bold green][✔] Severe network latency successfully injected into {victim.name}.[/bold green]")
        else:
            console.print("[bold yellow][!] Target container lacks 'tc' (iproute2) tools to inject latency.[/bold yellow]")
            
    except docker.errors.DockerException as e:
        console.print(f"[bold red][X] Docker Error: {e}[/bold red]")
