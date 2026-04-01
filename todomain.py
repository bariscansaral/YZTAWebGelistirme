from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles #Frontend için kullanacağız.
from starlette.responses import RedirectResponse
from starlette import status

from todomodels import Base
from tododatabase import engine
from routers import todoauth, todo


app = FastAPI()

app.include_router(todoauth.router) # Farklı dosyalarda (modüllerde) tanımladığımız endpoint gruplarını (Router)
                                    # ana uygulamaya dahil ediyoruz. Bu sayede kodun okunabilirliğini artırıyor
                                    # ve projeyi mantıksal parçalara (Auth, Todo vb.) bölüyoruz.
app.include_router(todo.router)

Base.metadata.create_all(bind=engine) #Bu satır veritabanımızı oluşturacak. Database içerisinde söylenen URL'de veritabanımız yoksa eğer bu veritabanını oluşturacak varsa hiçbir şey yapmayacak.

app.mount("/static", StaticFiles(directory="static"), name="static") #Front end için bağlantı sağladık.

@app.get("/")
async def read_root(request: Request):
    return RedirectResponse(url="/todo/todo-page", status_code=status.HTTP_302_FOUND)