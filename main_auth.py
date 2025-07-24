from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi_mcp import FastApiMCP, AuthConfig

token_auth_scheme = HTTPBearer()

# Your FastAPI app
app = FastAPI()

mcp = FastApiMCP(
    app,
    name="Protected MCP",
    auth_config=AuthConfig(
        dependencies=[Depends(token_auth_scheme)],
    ),
)
mcp.mount()
