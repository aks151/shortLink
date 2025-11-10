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
    # with every post call we are doing the creation process, we should not create new short code if it is present already in the db
    
    base_url = str(request.base_url)

    existingLink = await crud.checkDbForLink(db=db, long_Url = str(link.longUrl))

    if(existingLink != None):
        print('longURL was already parsed')
        return {
            "longUrl": str(existingLink.longUrl),
            "shortLink": f"{base_url}{existingLink.shortCode}"
        }
    
    shortcode = shortuuid.uuid()[:7]
    db_link = await crud.createLink(db=db, shortCode=shortcode, longUrl=str(link.longUrl))

    return {
        "longUrl": db_link.longUrl,
        "shortLink": f"{base_url}{db_link.shortCode}"
    }

@app.get("/{short_code}")
async def redirect_to_long_url(short_code: str, db: AsyncSession = Depends(get_db)):
    print("saturday debug greatness")
    db_link = await crud.getLinkByShortCode(db, shortCode=short_code)
    if db_link is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return RedirectResponse(url=db_link.longUrl)