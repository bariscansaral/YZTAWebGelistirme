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