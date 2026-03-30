from fastapi import FastAPI
from todomodels import Base
from tododatabase import engine

app = FastAPI()

Base.metadata.create_all(bind=engine) #Bu satır veritabanımızı oluşturacak. Database içerisinde söylenen URL'de veritabanımız yoksa eğer bu veritabanını oluşturacak varsa hiçbir şey yapmayacak.