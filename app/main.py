from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
import shortuuid
from contextlib import asynccontextmanager

from . import models, schemas, crud
from .database import engine, get_db


# models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/api/v1/shorten", response_model=schemas.LinkResponse)
async def create_short_link(link: schemas.LinkCreate, request: Request, db: AsyncSession = Depends(get_db)):
    shortcode = shortuuid.uuid()[:7]

    db_link = await crud.createLink(db=db, shortCode=shortcode, longUrl=str(link.longUrl))

    base_url = str(request.base_url)

    return {
        "longUrl": db_link.longUrl,
        "shortLink": f"{base_url}{db_link.shortCode}"
    }

@app.get("/{short_code}")
async def redirect_to_long_url(shortcode: str, db: AsyncSession = Depends(get_db)):
    db_link = await crud.getLinkByShortCode(db, shortcode=shortcode)
    if db_link is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return RedirectResponse(url=db_link.longUrl)