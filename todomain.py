from fastapi import FastAPI
from todomodels import Base
from tododatabase import engine
from routers import todoauth, todo


app = FastAPI()
app.include_router(todoauth.router) # Farklı dosyalarda (modüllerde) tanımladığımız endpoint gruplarını (Router)
                                    # ana uygulamaya dahil ediyoruz. Bu sayede kodun okunabilirliğini artırıyor
                                    # ve projeyi mantıksal parçalara (Auth, Todo vb.) bölüyoruz.
app.include_router(todo.router)

Base.metadata.create_all(bind=engine) #Bu satır veritabanımızı oluşturacak. Database içerisinde söylenen URL'de veritabanımız yoksa eğer bu veritabanını oluşturacak varsa hiçbir şey yapmayacak.
