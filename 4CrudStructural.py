from fastapi import FastAPI, Body, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Course:   #db için sınıf oluşturuyoruz.
    id: int
    title: str
    instructor: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, instructor: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.instructor = instructor
        self.rating = rating
        self.published_date = published_date


class  CourseRequest(BaseModel): #post ile veri eklemek için bu sınıfı kullanacağız. id'yi kullanıcı vermez o yüzden özel opsiyonel ayarladık ilerde otomatik de hesaplatıcaz şimdilik böyle
    id: Optional[int] = Field(description="The id of the course is optional", default=None) #Field verinin içeriğine sınır koymanı sağlar.
    title: str = Field(min_length=3, max_length=100)
    instructor: str = Field(min_length=3)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gte=2005, lte=2050) #lte = less then or equal to yani <=

    model_config={      #BaseModel içerisinde yer alan model_config değişkenini burada override (üzerine yazma) ediyoruz. Bu yapı, özellikle /docs (Swagger) sayfasında kullanıcının karşısına çıkacak olan örnek JSON formatını
                         # belirlememizi sağlar. Yani kullanıcıya veriyi hangi yapıda göndermesi gerektiğini gösteren bir 'kullanım kılavuzu örneği' sunmuş oluyoruz.
        "json_schema_extra":{
            "example":{
                "title":"Course Title",
                "instructor":"Cevdet",
                "rating":3,
                "published_date":2026
            }
        }

    }

courses_db=[
    Course(id=1,title="Python",instructor="Bariscan",rating=5,published_date=2029),
    Course(id=2,title="Kotlin",instructor="Atil",rating=5,published_date=2026),
    Course(id=3,title="Jenkins",instructor="Ahmet",rating=5,published_date=2023),
    Course(id=4,title="Kubernetes",instructor="Suna",rating=2,published_date=2020),
    Course(id=5,title="Machine Learning",instructor="Cevdet",rating=3,published_date=2026),
    Course(id=6,title="Deep Learning",instructor="Kerim",rating=1,published_date=2025)
]



@app.get("/courses", status_code=status.HTTP_200_OK) #Virgülden sonra kendi status codemizi belirtebiliriz.
async def get_all_courses():
    return courses_db

#Path sınıfı

@app.get("/courses/{course_id}", status_code=status.HTTP_200_OK)
async def get_course(course_id: int = Path(gt=0)): #gt=Greater Than lt=Less Than yani course id 0'dan büyük 3'ten küçük olacak demek
    for course in courses_db:
        if course.id == course_id:
            return course
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found!") #id yi olmayan bir değer girdiğinde bunu dönsün diye hata mesajını belirliyoruz.

#Query sınıfı

@app.get("/courses/", status_code=status.HTTP_200_OK)
async def get_courses_by_rating(course_rating:int = Query(gt=0, lt=6)): #0'dan büyük 6'dan küçük değerler kullanılmalı diyoruz yani
    courses_to_return=[]
    for course in courses_db:
        if course.rating==course_rating:
            courses_to_return.append(course)
    return courses_to_return

@app.get("/courses/publish/",status_code=status.HTTP_200_OK) #pathler aynı olmamalı queryde yoksa çalışmaz o yüzden özel path belirleyip öyle query atadık.
async def get_courses_by_published_date(published_date: int = Query(gt=2005, lt=2050)):
    courses_to_return=[]
    for course in courses_db:
        if course.published_date==published_date:
            courses_to_return.append(course)
    return courses_to_return

#CREATE İŞLEMLERİ

@app.post("/courses/create_course",status_code=status.HTTP_201_CREATED)
async def create_course(course_request: CourseRequest):
    new_course=Course(**course_request.model_dump())    # model_dump() fonksiyonu, Pydantic sınıfından gelen doğrulanmış veriyi
                                                        # standart bir Python sözlüğüne (dictionary) dönüştürür.
                                                        # Başına koyduğumuz ** (unpacking) işareti ise bu sözlükteki her bir anahtar-değer
                                                        # çiftini (key-value) sanki tek tek elle yazıyormuşuz gibi Course sınıfının
                                                        # içine 'id=1, title="Python"...' şeklinde dağıtarak yeni bir nesne üretmemizi sağlar. Ancak böyle yaparsak id'yi opsiyonel yaptık istekte id gelmezse bu patlar bi işe yaramaz.

    courses_db.append(find_course_id(new_course))

def find_course_id(course:Course): #ID'yi güncelleyip otomatik atamamızı sağlayacak olan fonksiyon bu.
    course.id=1 if len(courses_db)==0 else courses_db[-1].id+1
    return course

#UPDATE İŞLEMİ

@app.put("/courses/update_course",status_code=status.HTTP_204_NO_CONTENT) #Put işlemi için de ayrı bir courserequest sınıfı oluşturup düzenlemek çok daha iyi olur ama hızlı ilerlemek için şimdilik uğraşmadık.
async def update_course(course_request:CourseRequest):
    course_updated=False
    for i in range(len(courses_db)):
        if courses_db[i].id==course_request.id:
            courses_db[i]=course_request
            course_updated=True
        if not course_updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found!")


#DELETE İŞLEMİ

@app.delete("/courses/delete/{course_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int = Path(gt=0)):
    courses_deleted=False
    for i in range(len(courses_db)):
        if courses_db[i].id==course_id:
            courses_db.pop(i)
            courses_deleted=True
            break
    if not courses_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found!")