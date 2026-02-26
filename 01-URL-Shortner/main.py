from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import uvicorn
from database import engine, SessionLocal
import models, schemas, utils
from fastapi.responses import RedirectResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLCreate, request: Request, db: Session = Depends(get_db)):
    existing_url = db.query(models.URLItem).filter(models.URLItem.original_url == url.target_url).first()
    if existing_url:
        return {
            "target_url" : existing_url.original_url,
            "short_url" : str(request.base_url) + existing_url.short_code,
            "admin_url" : str(request.base_url) + "admin/" + existing_url.short_code
        }
    db_url = models.URLItem(original_url=url.target_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    db_url.short_code = utils.encode(db_url.id)
    db.commit()

    return {
        "target_url": db_url.original_url,
        "short_url": str(request.base_url) + db_url.short_code,
        "admin_url": str(request.base_url) + "admin/" + db_url.short_code
    }

@app.get("/{short_code}")
def forward_to_target(short_code:str, db: Session = Depends(get_db)):
    db_url = db.query(models.URLItem).filter(models.URLItem.short_code == short_code).first()

    if db_url:
        db_url.click_count += 1
        db.commit()

        return RedirectResponse(db_url.original_url, status_code=307)
    
    raise HTTPException(status_code=404, detail="URL not found")

@app.get("/admin/{short_code}")
def get_url_info(short_code: str, request: Request, db: Session = Depends(get_db)):
    # 1. Find the URL by short_code
    db_url = db.query(models.URLItem).filter(models.URLItem.short_code == short_code).first()
    
    if db_url:
        # 2. Return all the stats!
        return {
            "target_url": db_url.original_url,
            "short_url": str(request.base_url) + db_url.short_code,
            "admin_url": str(request.base_url) + "admin/" + db_url.short_code,
            "click_count": db_url.click_count,
            "created_at": db_url.created_at
        }
    
    raise HTTPException(status_code=404, detail="URL not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)