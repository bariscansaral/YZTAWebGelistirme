from fastapi import FastAPI, Depends, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from todomodels import Base, Todo
from tododatabase import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session


app = FastAPI()

Base.metadata.create_all(bind=engine) #Bu satır veritabanımızı oluşturacak. Database içerisinde söylenen URL'de veritabanımız yoksa eğer bu veritabanını oluşturacak varsa hiçbir şey yapmayacak.

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


# Verilerin hepsini görme
@app.get("/get_all")
async def get_all(db: db_dependency):
    # db.query(Todo).all() -> SQL'deki 'SELECT * FROM todos' komutunun ORM karşılığıdır.
    return db.query(Todo).all()


# Verileri filtreyle görme
@app.get("/get_by_id/{todo_id}", status_code=status.HTTP_200_OK)
async def get_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    # .filter() SQL'deki 'WHERE' şartıdır. .first() ise dönen listeden sadece ilk kaydı çeker.
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not Found")


# Veri ekleme:
@app.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    # **todo_request.model_dump() -> Pydantic modelindeki verileri sözlüğe çevirip Todo modeline dağıtır.
    todo = Todo(**todo_request.model_dump())
    db.add(todo)  # Veriyi işlem sırasına (stage) ekler.
    db.commit()  # SQL'e kalıcı olarak yazar.


# Verilerin update edilmesi:
@app.put("/update_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not Found")

    # Kullanıcıdan gelen güncel bilgileri mevcut veritabanı objesinin üzerine yazıyoruz.
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.completed = todo_request.completed

    db.add(todo)  # Güncellenen objeyi sıraya alıyoruz.
    db.commit()  # Veritabanında kalıcı hale getiriyoruz.


# Veri silme:
@app.delete("/delete_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        # Küçük bir detay: Buraya 'raise' eklemeyi unutursan hata fırlatmaz, koda devam eder.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not Found!")

    db.delete(todo)  # Objeyi veritabanından silinmek üzere işaretler.
    db.commit()  # Silme işlemini onaylar.
