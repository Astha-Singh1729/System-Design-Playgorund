from pydantic import BaseModel

class URLCreate(BaseModel):
    target_url: str

class URLInfo(URLCreate):
    short_url: str
    admin_url: str