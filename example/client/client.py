import argparse
import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

import os
from google import genai
from google.genai import types

from dotenv import load_dotenv

load_dotenv()


class MCPClient:
    """MCP Client for interacting with an MCP Streamable HTTP server"""

    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.genai = genai.Client(api_key=os.getenv("GENAI_API_KEY"))


    async def connect_to_streamable_http_server(
        self, server_url: str, headers: Optional[dict] = None
    ):
        """Connect to an MCP server running with HTTP Streamable transport"""
        self._streams_context = streamablehttp_client(  # pylint: disable=W0201
            url=server_url,
            headers=headers or {},
        )
        read_stream, write_stream, _ = await self._streams_context.__aenter__()  # pylint: disable=E1101

        self._session_context = ClientSession(read_stream, write_stream)  # pylint: disable=W0201
        self.session: ClientSession = await self._session_context.__aenter__()  # pylint: disable=C2801

        await self.session.initialize()

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        # The messages list here is for your internal tracking, not directly passed to send_message
        messages = [{"role": "user", "content": query}]

        response = await self.session.list_tools()

        # Correctly format tools for the Gemini API
        available_tools = []
        for tool in response.tools:
            tool_declaration = types.FunctionDeclaration(
                name=tool.name,
                description=tool.description,
                parameters=tool.inputSchema,
            )
            available_tools.append(types.Tool(function_declarations=[tool_declaration]))

        chat = self.genai.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(tools=available_tools),
        )

        final_text_parts = []
        # Initial call: send the user's query directly as the message
        response_from_gemini = chat.send_message(
            query, # Pass the query directly
            # max_output_tokens=1000,
        )

        # Process response and handle tool calls
        final_text = []

        # Loop to handle multi-turn interactions (tool calls and subsequent responses)
        while True:
            had_tool_call_in_turn = False
            # Check if there's a candidate and content, avoiding potential errors
            if response_from_gemini.candidates:
                candidate = response_from_gemini.candidates[0] # Usually one candidate
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.text:
                            final_text_parts.append(part.text)
                        elif part.function_call:
                            had_tool_call_in_turn = True
                            tool_name = part.function_call.name
                            tool_args = part.function_call.args

                            final_text_parts.append(f"[Calling tool {tool_name} with args {tool_args.to_dict()}]")

                            # --- Specific Logic for Boston Coordinates ---
                            if tool_name == "get_forecast" and "Boston" in query:
                                tool_args['latitude'] = 42.3601
                                tool_args['longitude'] = -71.0589
                            final_text_parts.append(f"[Overriding get_forecast with hardcoded Boston coordinates: Lat {tool_args['latitude']}, Long {tool_args['longitude']}]")

                            # --- End Specific Logic ---

                            # Execute tool call
                            tool_result = await self.session.call_tool(tool_name, tool_args.to_dict())

                            # Send the tool result back to Gemini
                            # Gemini will process this and likely generate a new response
                            response_from_gemini = await chat.send_message(
                                types.Part(function_response=types.FunctionResponse(name=tool_name, response=tool_result.content)),
                                max_output_tokens=1000,
                            )
                            # Break inner loop to process the *new* response from Gemini
                            break
                    
            if not had_tool_call_in_turn:
                # If no tool call was made in this turn, it means Gemini either
                # responded with text or completed its thought process.
                break # Exit the while loop

            # If a tool call was made, the loop will continue with the new response_from_gemini

        return "\n".join(final_text_parts)
    

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Properly clean up the session and streams"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)


async def main():
    """Main function to run the MCP client"""
    parser = argparse.ArgumentParser(description="Run MCP Streamable http based Client")
    parser.add_argument(
        "--mcp-localhost-port", type=int, default=8123, help="Localhost port to bind to"
    )
    args = parser.parse_args()

    client = MCPClient()

    try:
        await client.connect_to_streamable_http_server(
            f"http://localhost:{args.mcp_localhost_port}/mcp"
        )
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())