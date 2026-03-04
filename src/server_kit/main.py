from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def liveness():
    return {"message": "ok", "data": {"service": "api", "status": "alive"}}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
