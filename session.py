import os
import json
from datetime import timedelta
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

SESSION_EXPIRE_MINUTES = 60

async def create_session(session_id: str, user_id: str) -> None:
    session_data = {"user_id": str(user_id)}
    await redis_client.setex(
        f"session:{session_id}",
        timedelta(minutes=SESSION_EXPIRE_MINUTES),
        json.dumps(session_data)
    )

async def get_session(session_id: str) -> dict | None:
    data = await redis_client.get(f"session:{session_id}")
    if data:
        return json.loads(data)
    return None

async def delete_session(session_id: str) -> None:
    await redis_client.delete(f"session:{session_id}")