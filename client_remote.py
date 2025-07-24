import asyncio
from fastmcp import Client
from fastmcp.client.transports import SSETransport
import os


async def main():
    # --- 1. Define and get the Bearer token (from environment variable) ---
    token = os.getenv("MCP_CLIENT_TOKEN")
    if not token:
        raise ValueError("MCP_CLIENT_TOKEN environment variable not set. "
                         "Please set it, e.g., export MCP_CLIENT_TOKEN='your_secret_token'")

    # --- 2. Define the MCP server URL ---
    mcp_server_url = "http://localhost:8000/mcp"

    # --- 3. Create a custom SSE transport with the Authorization header ---
    # This directly injects the header into the transport layer.
    transport = SSETransport(
        url=mcp_server_url,
        headers={"Authorization": f"Bearer {token}"}
    )

    # --- 4. Initialize the MCP client with the custom transport ---
    async with Client(transport=transport) as client:
        print(f"Connected to MCP server at: {mcp_server_url}")

        # --- 5. List available tools (optional, but good for verification) ---
        try:
            tools = await client.list_tools()
            print("Available tools:", [tool.name for tool in tools])
        except Exception as e:
            print(f"Error listing tools: {e}")
            # If authentication fails, listing tools might also fail or return empty

        # --- 6. Call the 'greet' tool (as defined in your server) ---
        try:
            # The 'greet' tool expects a 'name' argument
            resp = await client.call_tool("greet", {"name": "Remote User"})

            # The response 'resp' from client.call_tool is typically a ToolCallResponse object.
            # The actual result from your FastAPI endpoint is in resp.result.
            # Your FastAPI endpoint returns {"message": "Hello, {name}!"}
            if resp and hasattr(resp, 'result') and isinstance(resp.result, dict):
                print(f"Response from 'greet' tool: {resp.result.get('message', 'No message found')}")
            else:
                print(f"Received unexpected response from 'greet' tool: {resp}")

        except Exception as e:
            print(f"Error calling 'greet' tool: {e}")

# Run the main coroutine
if __name__ == "__main__":
    asyncio.run(main())
