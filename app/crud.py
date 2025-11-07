from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models

async def getLinkByShortCode(db: AsyncSession, shortCode: str):
    print("getLinkByShortCode at crud.py")

    result = await db.execute(select(models.Link).filter(models.Link.shortCode == shortCode))
    return result.scalars().first()


async def createLink(db: AsyncSession, shortCode: str, longUrl: str):
    # here we are directly creating a new model and then just straight forward adding it to the db
    # what should be done is to first check if the long link has been processed already right
    new_link = models.Link(shortCode=shortCode, longUrl = longUrl)
    
    db.add(new_link)
    await db.commit()
    await db.refresh(new_link)
    return new_link
