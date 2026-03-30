from tododatabase import Base
from sqlalchemy import Column, Integer, String, Boolean


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