from fastapi import APIRouter, Depends, Path, HTTPException, Request
from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import RedirectResponse

from todomodels import Base, Todo
from tododatabase import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from routers.todoauth import get_current_user
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv #API keyi bu dosya kullanmak için kullanacağız. API key sayesinde gemini desteği ile description yazılacak.
import google.generativeai as genai
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

router = APIRouter(
    prefix="/todo", # Tüm todo işlemlerini '/todos' ana yolu altında toplar.
    tags=["Todo"]    # Dökümantasyonda kullanıcı işlemleriyle karışmaması için ayrı bir kategori açar.
)

templates=Jinja2Templates(directory="templates") #Frontend için klasör yolu belirttik.

class TodoRequest(BaseModel): #Veritabanına veri eklemek için sınıf oluşturuyoruz.
    title: str=Field(min_length=3)
    description: str = Field(min_length=3, max_length=1500)
    priority: int = Field(gt=0, lt=6)
    completed: bool = Field(default=False)

def get_db(): #Database ile bağlantı sağlamak için kullanacağımız fonksiyon. Veritabanından veri çekmek gibi tüm endpointler artık bu fonksiyona depend edecek.
    db=SessionLocal()
    try:
        yield db #yield return gibidir. return'den farkı return tek bir değer döndürürken yield birden fazla değer döndürebilir. Genel olarak SessionLocal ile çalışılırken yield kullanılması öneriliyor FastAPI dökümantasyonunda.
    finally:
        db.close() #Sessionu kapatan kod

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict, Depends(get_current_user)]

def redirect_to_login():
    redirect_response=RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie("access_token") #Tokenin geçerliliği bitmiş olabilir, hack saldırısı olabilir o yüzden cookie siliniyor.
    return redirect_response

@router.get("/todo-page") #Anasayfamız. Burada kullanıcı kayıt yapmadıysa bu sayfaya girememeli o yüzden get current user fonksiyonunu kullanıcaz Jinja html ile kendi kodumuz arasında bağlantı sağlıyor.
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user= await get_current_user(request.cookies.get("access_token")) #Kullanıcının cookiesinin içerisinden tokeni istiyoruz. get current user async fonksiyon olduğu için await yazısını ekledik başa.
        if user is None:
            return redirect_to_login()
        todos=db.query(Todo).filter(Todo.owner_id==user.get("id")).all()
        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos,"user": user})
    except:
        return redirect_to_login()



@router.get("/add-todo-page") #Yeni todo eklemek için frontend bağlantısı
async def render_add_todo_page(request: Request, db: db_dependency):
    try:
        user= await get_current_user(request.cookies.get("access_token")) #Kullanıcının cookiesinin içerisinden tokeni istiyoruz. get current user async fonksiyon olduğu için await yazısını ekledik başa.
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html", {"request": request,"user": user})
    except:
        return redirect_to_login()


@router.get("/edit-todo-page/{todo_id}") #todo değiştirileceği için todo'nun id'si path parametresi olarak istenmeli
async def render_edit_todo_page(request: Request,todo_id: int, db: db_dependency):
    try:
        user= await get_current_user(request.cookies.get("access_token")) #Kullanıcının cookiesinin içerisinden tokeni istiyoruz. get current user async fonksiyon olduğu için await yazısını ekledik başa.
        if user is None:
            return redirect_to_login()

        todo=db.query(Todo).filter(Todo.id==todo_id).first()
        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo,"user": user})
    except:
        return redirect_to_login()


# Verilerin hepsini görme
@router.get("/get_all")
async def get_all(user: user_dependency, db: db_dependency):
    # Bu fonksiyonu çalıştırmak için hem user (giriş yapmış kullanıcı) hem de db (veritabanı) bağlantısı zorunlu.
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # db.query(Todo).all() -> SQL'deki 'SELECT * FROM todos' komutunun ORM karşılığıdır.
    # Sadece giriş yapan kullanıcının id'sine ait olan tüm todoları filtreleyip getiren kod:
    return db.query(Todo).filter(Todo.owner_id == user.get("id")).all()


# Verileri filtreyle görme
@router.get("/get_by_id/{todo_id}", status_code=status.HTTP_200_OK)
async def get_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # .filter() SQL'deki 'WHERE' şartıdır. .first() ise dönen listeden sadece ilk bulduğunu çeker.
    # Burada diyoruz ki: Bize bir todo_id veriliyor, o todoyu bul;
    # ama o todo gerçekten bu kullanıcının (owner_id) mi diye de bak, başkasının verisi gelmesin.
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get("id")).first()

    if todo is not None:
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not Found")


# Veri ekleme:
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # **todo_request.model_dump() -> Pydantic modelindeki verileri sözlüğe çevirip Todo modeline dağıtır.
    # owner_id'yi ekleyerek, giriş yapan kullanıcının id verisini de yeni todoya ekliyoruz.
    # Böylece herkes sadece kendi hesabına özel todo'ları görecek şekilde atanmış oluyor.
    todo = Todo(**todo_request.model_dump(), owner_id=user.get("id"))
    todo.description=create_todo_with_gemini(todo.description) #Yapay zeka entegrasyonu sağlanırsa bu kod aktifleştirilerek canlıya alınacak.
    db.add(todo)  # Veriyi işlem sırasına (stage) ekler.
    db.commit()  # İşlemin yapılması için add dedikten sonra SQL'e kalıcı olarak yazılması (commit) şart.


# Verilerin update edilmesi:
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # Yine sadece bu kullanıcıya ait olan doğru todo'yu buluyoruz.
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get("id")).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not Found")

    # Kullanıcıdan gelen güncel bilgileri mevcut veritabanı objesinin üzerine yazıyoruz.
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.completed = todo_request.completed

    db.add(todo)  # Güncellenen objeyi tekrar sıraya alıyoruz.
    db.commit()  # Değişiklikleri veritabanında kalıcı hale getiriyoruz.


# Veri silme:
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # Silinecek todo'yu bulurken yine sahibinin (owner_id) bu kullanıcı olduğundan emin oluyoruz.
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get("id")).first()
    if todo is None:
        # Küçük bir detay: Buraya 'raise' eklemeyi unutursan hata fırlatmaz, kod çalışmaya devam eder.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not Found!")

    db.delete(todo)  # Objeyi veritabanından silinmek üzere işaretler.
    db.commit()  # Silme işlemini onaylar.

def create_todo_with_gemini(todo_string: str):
    load_dotenv()
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")
    response = llm.invoke(
        [
            HumanMessage(content="I will provide you a todo item to add my to do list. What i want you to do is create longer and more comprehensive description. My next message will be my todo:"),
            HumanMessage(content=todo_string)
        ]
    )
    return response.content

