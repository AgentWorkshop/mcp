from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "MCP is super cool"}
