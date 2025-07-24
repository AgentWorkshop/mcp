from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi_mcp import FastApiMCP, AuthConfig

token_auth_scheme = HTTPBearer()

app = FastAPI()

mcp = FastApiMCP(
    app,
    name="Protected MCP",
    auth_config=AuthConfig(
        dependencies=[Depends(token_auth_scheme)],        
    ),
    # IMPORTANT: Set a base_url if your app is hosted at a subpath or behind a proxy
    # For example, if your server is accessible at https://your-domain.com/api/mcp
    # you might set base_url="/api" or the full URL.
    # If the /mcp endpoint is directly at the root, you might not need to set this.
    # base_url="https://your-domain.com"
)
mcp.mount()

# Example endpoint that will be exposed as an MCP tool
@mcp.tool
@app.get("/greet/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}

# Run your FastAPI app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
