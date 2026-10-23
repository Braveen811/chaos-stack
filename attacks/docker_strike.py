import docker
import random
from rich.console import Console

console = Console()

def execute_docker_strike(severity):
    try:
        client = docker.from_env()
        containers = client.containers.list()
        
        if not containers:
            console.print("[bold yellow][!] No running Docker containers found to attack.[/bold yellow]")
            return

        # Select a random victim container
        victim = random.choice(containers)
        console.print(f"[bold red][☠️] Target acquired: {victim.name} (ID: {victim.short_id})[/bold red]")

        if severity == "low":
            console.print(f"[yellow][*] Action (LOW): Pausing container {victim.name}...[/yellow]")
            victim.pause()
        elif severity == "medium":
            console.print(f"[yellow][*] Action (MEDIUM): Restarting container {victim.name}...[/yellow]")
            victim.restart()
        elif severity == "high":
            console.print(f"[bold red][*] Action (HIGH): Sending SIGKILL to {victim.name}...[/bold red]")
            victim.kill()
            
        console.print(f"[bold green][✔] Chaos successfully injected into {victim.name}.[/bold green]")
        
    except docker.errors.DockerException as e:
        console.print("[bold red][X] Error: Could not connect to Docker. Is the Docker daemon running?[/bold red]")
        console.print(f"Details: {e}")
