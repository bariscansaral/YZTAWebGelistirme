# YZTA Web Geliştirme – FastAPI Öğrenme Projesi

Bu repository, **FastAPI merkezli web geliştirme sürecini** adım adım öğrenmek için oluşturulmuştur.  
Amaç; her konuyu **uygulayarak**, küçük commit’lerle ilerlemek ve süreci GitHub üzerinden belgelemektir.

Bu repo bir bitmiş ürün değil, **öğrenme sürecinin kendisidir**.

---

## 🎯 Amaç

- FastAPI ile backend geliştirmeyi öğrenmek
- Modern web geliştirme kavramlarını uygulamalı görmek
- Git & GitHub kullanımını gerçek bir proje üzerinden pekiştirmek
- Commit’leri öğrenme günlüğü gibi kullanmak

---

## 📚 Öğrenilecek Konu Başlıkları

Bu proje ilerledikçe aşağıdaki başlıklar ele alınacaktır:

- Python 201
- Pydantic & FastAPI Temelleri
- FastAPI Orta Seviye
- Veritabanı İşlemleri
- Dependency İşlemleri
- Yetkilendirme (Authentication / Authorization)
- Migration İşlemleri
- Frontend (Gemini ile)
- Docker
- FastAPI ile basit web geliştirme (Frontend Gemini üzerinden)

> Her başlık, öğrenildikçe commit’ler ve README güncellemeleri ile detaylandırılacaktır.

---

---

---

---

---


# Pydantic Nedir

Pydantic, Python’da veri doğrulama (validation) ve tip kontrolü yapmanı sağlayan bir kütüphanedir.
Özellikle API geliştirirken (örneğin FastAPI ile) gelen verilerin doğru tipte ve formatta olup olmadığını otomatik olarak kontrol etmek için kullanılır.

Python esnek (dinamik tipli) bir dil olduğu için sınıflarda değişkenlere belirtilen veri tipleri dışında farklı tiplerde değerler atanabilir ve bu durum her zaman hata oluşturmaz. İlk bakışta sorun gibi görünmese de, 
özellikle büyük projelerde ve API geliştirme süreçlerinde beklenmeyen hatalara yol açabilir. Bu tür veri tutarsızlıklarını önlemek ve daha güvenli bir yapı sağlamak amacıyla Pydantic ortaya çıkmıştır.

PydanticLearningMain.py dosyasında, sınıfların Pydantic kullanılmadan ve Pydantic ile birlikte oluşturulduğunda veri tiplerinde nasıl değişiklikler olabileceği detaylıca gösterilmiştir. Pydantic kullanılmadığı senaryoda, değişkenin tipini önceden belirlesen bile farklı tipte değerler atayabilirsin ve Python 
bunu hata olarak vermez. Oysa Pydantic sayesinde, doğru şekilde yazdığın sürece (örneğin bir Boolean değişkene "True" gibi string değer atamak) veri tipi otomatik olarak dönüştürülür. Ancak yanlış değer atarsan (örneğin "asdasd" gibi Boolean olmayan bir ifade) Pydantic hata verir. Yani Pydantic, veri tiplerini güvenli ve tutarlı bir şekilde yönetmeyi sağlar.

---

# Python Senkron ve Asenkron Çalışma Açıklaması

Bu proje, Python’da senkron (blocking) ve asenkron (non-blocking) fonksiyonların farkını öğretmek amacıyla hazırlanmıştır. Kodda iki fonksiyon üzerinden hem senkron hem de asenkron çalışmayı görebilirsiniz.

## Senkron Çalışma

Senkron çalışma, işlemlerin ardışık olarak yürütüldüğü klasik yöntemdir. Burada bir fonksiyon tamamlanmadan bir sonraki fonksiyon başlamaz. Örneğin, `my_func1()` tamamlanmadan `my_func2()` çalışmaz. Bu nedenle toplam süre, iki fonksiyonun sürelerinin toplamına eşittir. Senkron çalışma basittir ancak uzun süren görevlerde programın beklemesine sebep olur.

## Asenkron Çalışma

Asenkron çalışma, işlemlerin eş zamanlı (concurrent) yürütülmesini sağlar. Python’da bunu `asyncio` kütüphanesi ile gerçekleştirebiliriz. Asenkron programlamada fonksiyonlar `async def` ile tanımlanır ve çalıştırılırken `await` kullanılır.

- `async def`: Fonksiyonları asenkron olarak tanımlar. Bu fonksiyonlar `await` ile çalıştırılabilir.
- `await`: Asenkron işlemin tamamlanmasını bekler. `await` kullanılmazsa fonksiyon çalıştırılmaz ve hata alınır.
- `asyncio.create_task()`: Asenkron fonksiyonları task olarak başlatır, arka planda çalışmasını sağlar ve diğer görevlerle eş zamanlı yürütülmesine imkan tanır.
- `async def main()` ve `asyncio.run(main())`: Asenkron görevlerin yönetildiği ana fonksiyondur. Tüm task’lar burada başlatılır ve çalıştırılır.

Asenkron çalışmada fonksiyonlar eş zamanlı çalıştırıldığı için toplam süre, tek bir fonksiyonun süresine yakın olur. Bu yöntem özellikle I/O bekleyen işlemlerde veya uzun süren görevlerde programın daha verimli çalışmasını sağlar.

## Özet

- Senkron: Fonksiyonlar ardışık çalışır, toplam süre fonksiyon sürelerinin toplamına eşittir.
- Asenkron: Fonksiyonlar eş zamanlı çalışır, toplam süre genellikle en uzun fonksiyon süresine yakın olur.
- Asenkron programlama, modern Python’da performansı artırmak için kritik bir yöntemdir.

---

## 🚀 Uygulama: FastAPI ile İlk API Denemesi (CRUD İşlemleri)

Bu aşamada, bir kurs veritabanı simülasyonu üzerinden temel HTTP yöntemlerini (metotlarını) uyguladım.

### 🛠 Temel Terimler ve Mantık

- **Endpoint (Uç Nokta):** Web sitesindeki adres uzantılarıdır (Örn: `/courses`).
- **Path Parameter (Yol Parametresi):** Adres çubuğuna direkt yazdığımız özel bilgilerdir. "Sadece bu ID'ye sahip parçayı getir/sil" komutudur.
- **Body (Gövde):** Veriyi adres çubuğunda değil, bir paket içinde göndermektir. Yeni bir kayıt eklerken (POST) veya bir kaydı güncellerken (PUT) tüm veri setini bu paketle içeri alırız.
- **CRUD:** Bir veriyi Oluşturma (Create), Okuma (Read), Güncelleme (Update) ve Silme (Delete) işlemlerinin genel adıdır.

### 📝 Yapılan İşlemler (Fonksiyonlar)

- **GET (Okuma):** Sistemdeki mevcut verileri listeleriz. Tüm kursları görebilir veya belirli bir kurs ismine/kategorisine göre filtreleme yapabiliriz.
- **POST (Oluşturma):** `Body()` kullanarak dışarıdan yeni bir kurs verisini sisteme dahil ederiz.
- **PUT (Güncelleme):** Mevcut bir kaydın üzerine yeni bilgileri yazarız. "Şu ID'li kursun eğitmenini değiştir" komutu gibi çalışır.
- **DELETE (Silme):** Belirlediğimiz bir ID'yi sistemden tamamen çıkarırız. Burada adres çubuğuna ID yazmak (Path Parameter), tüm veritabanını silmek yerine sadece hedeflediğimiz kaydı silmemizi sağlar.

### ⚠️ Önemli Not: Path Çakışması (Conflict)
Eğer iki farklı fonksiyon aynı adres yapısını (Örn: `/courses/{değişken}`) kullanıyorsa, program hangisini çalıştıracağını karıştırabilir. Bu yüzden ID ile arama yaparken `/courses/byid/{id}` gibi daha spesifik bir path tanımlamak sistemin hata vermesini önler.

### 🔍 Otomatik Dökümantasyon (Swagger UI)
FastAPI'nin en büyük kolaylığı, yazdığımız tüm bu fonksiyonları görsel bir panelde test etmemize izin vermesidir. Uygulama çalışırken şu adresten tüm endpointleri deneyebilirsin:
`http://127.0.0.1:8000/docs`

---

## 🚀 Uygulama: Pydantic ile Veri Güvenliği ve Otomatik ID Yönetimi

Bu aşamada projemizi bir üst seviyeye taşıyarak verileri sadece işlemekle kalmadık, aynı zamanda bir "Kalite Kontrol" (Validation) mekanizması kurduk.

### 🛠 Neler Öğrendim ve Uyguladım?

- **Pydantic & BaseModel:** Veri girişlerini belirli bir kalıba soktuk. Artık sisteme rastgele veri giremiyoruz; her girişin tipi ve sınırları belli.
- **Field Sınıfı (Tolerans Yönetimi):** Verilerin içeriğine kısıtlamalar koyduk. Örneğin bir kursun puanı (`rating`) 0-6 arası olmalı veya yayınlanma tarihi (`published_date`) belirli bir yıl aralığında kalmalı.
- **HTTP Status Codes:** İşlemlerin sonucuna göre (Başarılı: 200, Oluşturuldu: 201, Veri Yok: 204 vb.) standart internet protokolü kodlarını kullanmaya başladık.
- **HTTPException (Hata Yakalama):** Aranan bir ID bulunamadığında sistemin "çökmesi" yerine kullanıcıya anlamlı bir hata mesajı (404 Not Found) dönmesini sağladık.

### 📝 Teknik Detaylar

- **Otomatik ID Atama:** Kullanıcının her seferinde benzersiz bir ID bulup girmesi zahmetinden kurtulduk. `find_course_id` fonksiyonu ile sistem, veritabanındaki son kaydı kontrol edip bir sonraki ID'yi otomatik atıyor.
- **model_config & JSON Schema:** API dokümantasyonunda (`/docs`) kullanıcının işini kolaylaştıracak "örnek veri formatı" (example) hazırladık.
- **model_dump() & Unpacking:** Pydantic nesnelerini standart Python sözlüklerine dönüştürüp `**` operatörü ile sınıflar arası hızlı veri transferi yapmayı öğrendik.
- **Gelişmiş CRUD:**
    - **POST:** Yeni kayıtları otomatik ID ile ekliyoruz.
    - **PUT:** Mevcut kayıtları Pydantic doğrulamasıyla güncelliyoruz.
    - **DELETE:** Belirli bir ID'yi güvenli bir şekilde (hata kontrolü yaparak) siliyoruz.

> **Mühendislik Notu:** `update` işlemi için aynı sınıfı kullanmak pratik olsa da, ileride sadece belirli alanların güncellenmesi gereken durumlar için "Update-Specific" sınıflar oluşturmanın daha temiz (clean code) bir yaklaşım olacağını not ettik.

 ---

> ## 🗄️ SQL Temelleri ve Veritabanı Mimarisi

Bu aşamada veritabanlarının çalışma mantığını, SQL dilini ve projemizi nasıl "kalıcı" (persistent) hale getireceğimizi öğrendik. Artık verilerimiz RAM'de değil, fiziksel bir `.db` dosyasında saklanıyor.

### 📊 SQL (Structured Query Language) Notları
Veritabanı üzerinde işlem yapmak için kullandığımız temel komutlar:

- **SELECT:** Verileri çağırmak için kullanılır. `SELECT *` tüm kolonları, `SELECT name, hint` ise sadece belirli kolonları getirir.
- **LIMIT:** Gelen veri miktarını sınırlandırır (Örn: `LIMIT 10`).
- **WHERE & LIKE:** Verileri filtrelemek için kullanılır. 
    - `WHERE id=4`: Tam eşleşme.
    - `LIKE 'A%'`: A ile başlayanlar.
    - `LIKE '%i'`: i ile bitenler.
    - `LIKE '%e%'`: İçinde e geçenler.
- **INSERT INTO:** Yeni veri eklemek için kullanılır. Kolon sırasına ve veri tipine dikkat edilmelidir.
- **UPDATE & SET:** Mevcut verileri güncellemek için kullanılır (`WHERE` ile hedef belirtmek kritiktir!).
- **DELETE:** Veri silmek için kullanılır.

### 🏗️ SQLAlchemy Proje Yapısı

1. **Database Konfigürasyonu:** SQLite bağlantı ayarları yapıldı ve `SessionLocal` ile veritabanı "oturumları" oluşturuldu.
2. **Model Tanımlama:** `Todo` sınıfı, `Base` kalıbından türetilerek veritabanında fiziksel bir tabloya (`todos`) dönüştürüldü.
    - `id`: Benzersiz seri numarası (Primary Key).
    - `completed`: İşlem durumunu tutan Boolean (Varsayılan: False).
3. **Tablo Oluşturma:** `Base.metadata.create_all(bind=engine)` komutu ile tanımladığımız modellerin fiziksel `.db` dosyasında otomatik olarak oluşturulması sağlandı.

---

>## 💉 Gelişmiş Dependency Injection (Bağımlılık Enjeksiyonu) ve `Annotated` Kullanımı

Veritabanı işlemlerinde verimliliği artırmak ve kod tekrarını önlemek amacıyla **Dependency Injection (Bağımlılık Enjeksiyonu)** yapısını kurduk. Bu yapıyı daha profesyonel hale getirmek için `typing.Annotated` kütüphanesini kullandık.

#### 1. Dependency Injection (DI) Nedir?
DI, bir fonksiyonun çalışması için gereken dış kaynağın (örneğin Veritabanı Oturumu), fonksiyonun içinde yaratılması yerine dışarıdan bir "yakıt hattı" gibi içeri aktarılmasıdır.

#### 2. `Annotated` ile Standart Bağlantı Aparatı Oluşturma
Normalde her API fonksiyonunun içine uzun uzun `db: Session = Depends(get_db)` yazmamız gerekir. `Annotated` kullanarak bu bağımlılığı bir tip tanımı olarak standartlaştırdık.

**Neden `Annotated` Kullanıyoruz?**
- **Kod Temizliği:** Fonksiyon parametrelerini kalabalıktan kurtarır.
- **Tek Merkezden Kontrol:** Veritabanı alma yöntemini değiştirmek istediğimizde 50 farklı yeri değil, sadece en baştaki `db_dependency` tanımını değiştirmemiz yeterli olur.
- **Tip Güvenliği:** Yazılım editörünün bize hangi verinin (Session) geleceğini tam olarak bilmesini sağlar.

**Kod Örneği:**
```python
# Standart bağlantı ucu (Dependency) tanımlama
db_dependency = Annotated[Session, Depends(get_db)]

# Kullanımı: Artık her fonksiyon sadece bu ucu takıyor
@app.get("/")
async def read_data(db: db_dependency):
    return db.query(Todo).all()