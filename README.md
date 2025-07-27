
# MCP (Model Context Protocol) Python Examples

This repository contains examples demonstrating how to build and interact with MCP servers and clients in Python. It covers basic integration, authentication, and an advanced example of a GenAI-powered agent that uses MCP tools.

## Features

*   **Authenticated FastAPI Server**: An example of integrating an MCP server into a FastAPI application with bearer token authentication.
*   **Standalone Tool Server**: A standalone MCP server providing weather tools using the National Weather Service (NWS) API.
*   **Simple Python Client**: A basic client for calling a specific tool on the authenticated server.
*   **GenAI Agent Client**: An advanced client that uses Google's Gemini Pro to understand natural language queries and decide which tool to call on the weather server.

## Prerequisites

*   Python 3.10+
*   `pip` and `virtualenv` (or `pyenv`)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AgentWorkshop/mcp.git
    cd mcp
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Using pyenv (recommended)
    pyenv virtualenv 3.12 mcp_env
    pyenv activate mcp_env

    # Or using venv
    # python3 -m venv venv
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    The GenAI agent client requires an API key from Google.

    Create a `.env` file in the root of the project:
    ```bash
    touch .env
    ```

    Add your Google AI API key to the `.env` file:
    ```
    GENAI_API_KEY="your_google_ai_api_key"
    ```

---

## Example 1: Authenticated FastAPI Server (`greet` tool)

This example demonstrates an MCP server integrated with FastAPI that requires bearer token authentication.

### 1. Run the Server

The server will start on `http://localhost:8000`.

```bash
python main_remote.py
```

### 2. Run the Client

In a new terminal, first set the required environment variable for the authentication token. For this example, any string will work.

```bash
export MCP_CLIENT_TOKEN="my-secret-token"
python client_remote.py
```

#### Expected Output

```
Connected to MCP server at: http://localhost:8000/mcp
Available tools: ['greet']
Response from 'greet' tool: Hello, Remote User!
```

### (Optional) Testing with `curl`

You can also test the server endpoints directly with `curl`.

*   **Unauthenticated request (will fail):**
    ```bash
    curl http://localhost:8000/mcp
    ```
    *Output:* `{"detail":"Not authenticated"}`

*   **Authenticated request (will succeed):**
    ```bash
    curl -H "Authorization: Bearer my-secret-token" http://localhost:8000/mcp
    ```
    *Output:*
    ```
    event: endpoint
    data: /mcp/messages/?session_id=...
    ```

---

## Example 2: GenAI-Powered Weather Agent

This example showcases a more advanced use case: a standalone MCP server providing weather tools and a client that uses a Large Language Model (Gemini) to answer natural language questions by calling those tools.

### 1. Run the Weather Tool Server

This server provides `get_forecast` and `get_alerts` tools. It will run on `http://localhost:8123`.

```bash
python example/server/weather.py
```

### 2. Run the Agent Client

In a new terminal, run the agent client. Make sure you have set your `GENAI_API_KEY` in the `.env` file as described in the Setup section.

The client will start an interactive chat loop.

```bash
python example/client/client.py
```

#### Usage

Once the client is running, you can ask it questions about the weather.

**Example Query:**

```
Query: Tell me the forecast for Boston tomorrow.
```

**Expected Output:**

The client will show the internal reasoning of the model, including the tool call it decides to make. Note that for "Boston", the client code specifically uses hardcoded coordinates.

```
Query: Tell me the forecast for Boston tomorrow.

[Calling tool get_forecast with args {'latitude': 42.3601, 'longitude': -71.0589}]
[Overriding get_forecast with hardcoded Boston coordinates: Lat 42.3601, Long -71.0589]
This Afternoon:
Temperature: 75°F
Wind: 10 to 15 mph W
Forecast: A chance of showers and thunderstorms. Some of the storms could produce gusty winds. Mostly sunny, with a high near 75. West wind 10 to 15 mph, with gusts as high as 25 mph. Chance of precipitation is 30%.

Tonight:
Temperature: 55°F
Wind: 10 to 15 mph W
Forecast: A slight chance of showers and thunderstorms before 8pm. Mostly clear, with a low around 55. West wind 10 to 15 mph, with gusts as high as 25 mph. Chance of precipitation is 20%.

... (and so on)
```

You can ask for other locations as well, but the model will need to infer the latitude and longitude.

---

## References

- https://medium.com/@miki_45906/how-to-build-mcp-server-with-authentication-in-python-using-fastapi-8777f1556f75
