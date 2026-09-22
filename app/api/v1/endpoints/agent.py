from fastapi import APIRouter, Depends
from app.services.agent.sentinel import SentinelAgent
from app.services.agent.tools import SecurityAuditorTool
from app.api.deps import RoleChecker
from app.core.responses import api_response

router = APIRouter()
agent = SentinelAgent(name="Sentinel")
agent.add_tool(SecurityAuditorTool())

@router.post("/execute")
async def execute_agent_command(command: str, current_user=Depends(RoleChecker(["admin"]))):
    result = await agent.run_command(command)
    return api_response(status="success", data={"result": result})
