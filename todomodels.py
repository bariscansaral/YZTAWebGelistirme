from tododatabase import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Todo(Base):
    __tablename__ = "todos"  # Veritabanındaki fiziksel tablonun adı.

    # 1. Primary Key: Her parçanın eşsiz bir seri numarası (ID) olması gerekir.
    # 'index=True' diyerek bu numaraya göre arama yapılmasını hızlandırıyoruz (hızlı katalog tarama gibi).
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    description = Column(String)

    # 2. Priority: İş emrinin öncelik sırasını belirleyen tam sayı değeri.
    priority = Column(Integer)

    # 3. Boolean & Default: İşlem tamamlandı mı?
    # Yeni bir iş emri açıldığında varsayılan olarak 'tamamlanmadı' (False) kabul ediyoruz.
    completed = Column(Boolean, default=False)
    owner_id=Column(Integer, ForeignKey("users.id")) #Todo listlerle kullanıcılar arasında bağ kuruyoruz her kullanıcı herkesin listini göremesin kendininkini görsün diye.


class User(Base):
    # Veritabanında bu tabloya verilecek isim:
    __tablename__ = "users"

    # Her kullanıcının kendine has, benzersiz kimlik numarası (Otomatik artar)
    id = Column(Integer, primary_key=True, index=True)

    # Kullanıcı adı ve E-posta; 'unique=True' sayesinde aynı isimle/maille iki kişi kayıt olamaz.
    username = Column(String, unique=True)
    email = Column(String, unique=True)

    # Kullanıcının temel bilgileri:
    first_name = Column(String)
    last_name = Column(String)

    # Şifre güvenliği: Parolayı açık halde değil, şifrelenmiş (hashed) bir metin olarak saklıyoruz.
    hashed_password = Column(String)

    # Kullanıcının durumu: Hesabı aktif mi değil mi? (Varsayılan olarak True)
    is_active = Column(Boolean, default=True)

    # Yetkilendirme: Kullanıcının rolu (Örn: 'admin' veya 'user').
    # Kimin hangi yetkiye sahip olacağını bu sütun sayesinde belirliyoruz.
    role = Column(String)
