from fastapi import FastAPI, Request, HTTPException, Depends
from models import URL, Click
from database import SessionLocal
import string, random
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class URLRequest(BaseModel):
    long_url: str
    
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

RATE_LIMIT = 10  # max requests
RATE_LIMIT_WINDOW = 60  # seconds

@app.post("/shorten")
async def shorten_url(request: URLRequest, db: Session = Depends(get_db), client_ip: str = Depends(lambda request: request.client.host)):
    # Rate limit key for this IP
    key = f"rate_limit:{client_ip}"

    current = r.get(key)
    if current and int(current) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests, please try again later.")
    
    # Increment count or set with expiry if new
    pipe = r.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, RATE_LIMIT_WINDOW)
    pipe.execute()

    # Link shortening code
    short_code = generate_short_code()
    db_url = URL(long_url=request.long_url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return {"short_url": f"http://localhost:8000/{short_code}"}


# Serve index.html manually at "/"
@app.get("/")
def serve_home():
    return FileResponse("static/index.html")
    
# GET /{short_code}: Redirect & log click
@app.get("/stats/{short_code}")
def get_stats(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    clicks = db.query(Click).filter(Click.short_code == short_code).all()
    total_clicks = len(clicks)

    click_logs = [
        {"timestamp": str(click.timestamp), "ip": click.ip_address}
        for click in clicks
    ]

    return {
        "short_code": short_code,
        "long_url": url.long_url,
        "total_clicks": total_clicks,
        "click_logs": click_logs
    }


@app.get("/{short_code}")
async def redirect_to_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    # Checking Redis first
    long_url = r.get(short_code)
    if not long_url:
        url = db.query(URL).filter(URL.short_code == short_code).first()
        if not url:
            raise HTTPException(status_code=404, detail="Short URL not found")
        long_url = url.long_url
        r.set(short_code, long_url, ex=3600)  # cache for 1 hour

    # Log click
    click = Click(short_code=short_code, ip_address=request.client.host)
    db.add(click)
    db.commit()

    return RedirectResponse(long_url)