import os
from fastapi import FastAPI
from routers import events
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(events.router)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://event-search-fd9fe.web.app",    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


a = "2021-08-02（月）08:45-2021-10-29（金）18:00"
#from pytz import timezone
from datetime import datetime, timedelta, timezone
JST = timezone(timedelta(hours=+9), 'JST')
# utc_now = datetime.now(timezone('UTC'))
tzutc = "2021-08-01T23:45:00.000Z"
# dt_now = datetime.datetime.now()
# print(dt_now)
# dt_now_utc = datetime.datetime.now(datetime.timezone.utc)

# print(dt_now_utc)

"https://connpass.com/search/?q=python&start_from=2021/01/04&start_to=2021/07/04&prefectures=osaka&prefectures=online&selectItem=osaka&selectItem=online"

"prefectures = tokyo"
"https://connpass.com/api/v1/event/?keyword=python&prefectures=tokyo&order=1&count=10"
