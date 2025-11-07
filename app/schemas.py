from pydantic import BaseModel, HttpUrl

class LinkBase(BaseModel):
    longUrl: HttpUrl

class LinkCreate(LinkBase):
    pass

class LinkResponse(LinkBase):
    shortLink: str

    class Config:
        from_attributes = True