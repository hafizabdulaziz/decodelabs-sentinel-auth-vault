from app.services.agent.base import BaseSecurityAgent

class SentinelAgent(BaseSecurityAgent):
    async def run_command(self, command: str) -> str:
        # Simple command parsing
        if "audit" in command.lower():
            return "Running security audit..."
        elif "scan" in command.lower():
            return "Scanning for vulnerabilities..."
        return "Unknown command."
