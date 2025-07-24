

### New
https://github.com/invariantlabs-ai/mcp-streamable-http/blob/main/python-example/server/weather.py

- example folder

- example question: 
Tell me the forecast for Boston tomorrow.

```
{
    "Latitude": "42.3601",
    "Longitude": "-71.0589
}
```

### 
```bash
pyenv virtualenv 3.12 lab_mcp
pyenv activate lab_mcp
pip install -r requirements.txt
or 
yes | pip install -r requirements.txt
```

```
uvicorn main:app --reload
```

### Test
```bash
curl http://127.0.0.1:8000/mcp
```

Output
```bash
event: endpoint
data: /mcp/messages/?session_id=f58ebf791ad445319884ae5bc336ba4c
```


## main_auth
```
uvicorn main:app --reload

```

### Test client
```bash
curl http://127.0.0.1:8000/mcp
```

Output
```bash
{"detail":"Not authenticated"}
```

Server
```
 "GET /mcp HTTP/1.1" 403 Forbidden
```

### Test client2
```bash
curl -H "Authorization: Bearer <your-actual-jwt-token>" http://localhost:8000/mcp
```

```
event: endpoint
data: /mcp/messages/?session_id=668b4e749e0a4313bacc24f26f11c4f1

: ping - 2025-07-24 15:26:34.732362+00:00
```

## Use Python

### Server
```bash
python main_remote.py
```


### Test client - Python
```bash
export MCP_CLIENT_TOKEN="TEST_CLIENT_TOKEN"
python client_remote.py
```



## References

- https://medium.com/@miki_45906/how-to-build-mcp-server-with-authentication-in-python-using-fastapi-8777f1556f75



