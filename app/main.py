import os
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
import shortuuid
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from . import models, schemas, crud
from .database import engine, get_db
import redis.asyncio as redis
from redis.exceptions import ConnectionError as RedisConnectionError

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

REDIS_URL = os.getenv("REDIS_URL")

# Global variable for the Redis client
redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup...")
    async with engine.begin() as conn:
        # await conn.run_sync(models.Base.metadata.create_all)
        pass
    
    global redis_client
    if REDIS_URL:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        try:
            await redis_client.ping()
            print("Connected to Redis successfully")
        except RedisConnectionError as e:
            print(f"Could not connect to Redis: {e}")
            redis_client = None
    else:
        print("REDIS_URL not set. Redis client not created.")
        
    yield

    print("Application Shutdown...")
    if redis_client:
        await redis_client.close()
        print("Redis connection closed.")

app = FastAPI(lifespan=lifespan)

@app.post("/api/v1/shorten", response_model=schemas.LinkResponse)
async def create_short_link(link: schemas.LinkCreate, request: Request, db: AsyncSession = Depends(get_db)):
    cacheKey = str(link.longUrl)
    base_url = str(request.base_url)

    if redis_client:
        cachedShortLink = await redis_client.get(cacheKey)
        if cachedShortLink:
            print("Cache hit!")
            return {
                "longUrl": str(cacheKey),
                "shortLink": f"{base_url}{cachedShortLink}"
            }
        print("Cache Miss")

    existingLink = await crud.checkDbForLink(db=db, long_Url = str(link.longUrl))

    if(existingLink != None):
        print('longURL was already parsed from DB, setting cache.')
        if redis_client:
            await redis_client.set(cacheKey, existingLink.shortCode)
        return {
            "longUrl": str(existingLink.longUrl),
            "shortLink": f"{base_url}{existingLink.shortCode}"
        }
    
    shortcode = shortuuid.uuid()[:7]
    db_link = await crud.createLink(db=db, shortCode=shortcode, longUrl=str(link.longUrl))

    print("New link created, setting cache.")
    if redis_client:
        await redis_client.set(db_link.longUrl, db_link.shortCode)

    return {
        "longUrl": db_link.longUrl,
        "shortLink": f"{base_url}{db_link.shortCode}"
    }

@app.get("/{short_code}")
async def redirect_to_long_url(short_code: str, db: AsyncSession = Depends(get_db)):
    cacheKey = short_code
    print("Dummy Commit")
    if redis_client:
        cachedLink = await redis_client.get(cacheKey)
        if cachedLink:
            print("Cache Hit!")
            return RedirectResponse(url=cachedLink)
    print("Cache Miss!")

    db_link = await crud.getLinkByShortCode(db, shortCode=short_code)
    if db_link is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    print("DB hit, setting cache.")
    if redis_client:
        await redis_client.set(cacheKey, db_link.longUrl)
        
    return RedirectResponse(url=db_link.longUrl)
