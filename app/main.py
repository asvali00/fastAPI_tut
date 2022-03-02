from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote


# SQLALCHEMY code that creates table
# models.Base.metadata.create_all(bind=engine) # ovo više i netreba - imamo alembic, ali možeš i ostaviti, to samo znači da će se tablice kreirati pri pocetku svake aplikacije ako ih nema... a alembic ce rijesiti tragove koje nisi definira bude li trebalo

app = FastAPI()

# here we will provide a list a public domains that can talk to out API - and here we can allow specific request (Only GET, or only POST, etc)
origins = ["*"] # origins = ["*"] --> all servers can access our API

# middleware is function that runs before any request, middleware is often used in webframeworks
# in this case with CORSmiddleware will specify what domains can talk to our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Path/route operation - OVO TI JE VIŠE MANJE NEPOTREBNO
@app.get("/")  # Decorator - sa ovime donju funkciju definiramo kao fastAPI funkciju - tome služe dekoratori - ovdje specificiramo GET http request metodu i unutar toga PATH prema root funkciji koji kreće iza tvoje domene -  ovdje / predstavlja to da smo na istom mjestu na kojem je domena - znači root je tvoja home domena npr www.home.com
def root():  # Function - async keyword doing sth asyncronosly (you can remove that and everythin we'll be pretty much the same) - root - arbitrary name
    # here we're returning python dictionary and fastAPI just change it to JSON ehich is universal data language in web
    return {"message to world": "Welcome to my API!!!!"}
