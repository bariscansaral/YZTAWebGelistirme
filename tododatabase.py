from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Veritabanının Konumu: SQLite kullanarak 'todoai_app.db' adında yerel bir dosya oluşturuyoruz.
# Bu dosya, tüm verilerimizin kalıcı olarak saklanacağı 'hard disk' alanıdır.
SQLALCHEMY_DATABASE_URL = "sqlite:///./todoai_app.db"

# 2. Motor (Engine): Veritabanı ile Python arasındaki ana köprüdür.
# 'connect_args' içindeki ayar, SQLite'ın aynı anda tek bir işlem hattından güvenle çalışmasını sağlar.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 3. Oturum Fabrikası (Session): Veritabanına veri eklemek veya silmek için açılan geçici 'işlem pencereleridir'.
# Her kullanıcı işlemi için buradan bir 'oturum' (session) kopyası üretilir.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Ana Kalıp (Base): Bu en kritik kısımdır.
# Veritabanındaki tabloları oluştururken bu 'Base' sınıfından miras alacağız.
# Bu sayede SQLAlchemy, hangi sınıfın hangi tabloya karşılık geldiğini otomatik olarak anlar.
Base = declarative_base()