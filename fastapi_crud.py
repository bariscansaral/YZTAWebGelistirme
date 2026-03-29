from fastapi import FastAPI, Body
#uvicorn fastapi_crud:app --reload şu komut ile terminalden bu dosyayı çalıştırabilirsin
app=FastAPI()

#Her endpoint oluşturulmasında fonksiyon tanımlanması ve çeşidinin belirtilmesi gereklidir.


# #Göstermek için değişken şeklinde veritabanı oluşturuyoruz
courses_db=[
    {"id": 1, "instructor": "Bariscan", "title": "Python", "category": "Development"},
    {"id": 2, "instructor": "Atil", "title": "Java", "category": "Development"},
    {"id": 3, "instructor": "Ahmet", "title": "Jenkins", "category": "Devops"},
    {"id": 4, "instructor": "Zeynep", "title": "Deep Learning", "category": "AI"},
    {"id": 5, "instructor": "Mehmet", "title": "Machine Learning", "category": "AI"},
    {"id": 6, "instructor": "Selman", "title": "Kubernets", "category": "Devops"}
]

@app.get("/")
async def hello_world():
    return {"Message":"Hello World"}

@app.get("/courses") #/courses eklediğimizde web sitesine tüm kursları getirecek bunu istiyoruz.
async def get_all_courses():
    return courses_db       #http://127.0.0.1:8000/courses adresine gidersen courses dbde yazdıklarını ekrana yazdırır.


#Path ile Filtreleme:

@app.get("/courses/{course_title}") #Süslü parantez bu pathin ne yazılırsa onu getirmesini sağlar
async def get_course_by_title(course_title:str):
    for course in courses_db:
        if course.get("title").casefold() == course_title.casefold():
            return course

@app.get("/courses/{course_id}") #Bu kod çalışmıyor aynı üstteki ile aynı path'de olduğu için bunu göstermek için buraya yazıldı, path çakışmasını göstermek için.
async def get_course_by_id(course_id:int):
    for course in courses_db:
        if course.get("id").casefold() == course_id.casefold():
            return course


@app.get("/courses/byid/{course_id}")
async def get_course_by_id(course_id:int):
    for course in courses_db:
        if course.get("id") == course_id:
            return course

#Query ile Filtreleme:

@app.get("/courses/") # query için patika yanına slash koymak yeterli
async def get_category_by_query(category:str):
    courses_to_return = []
    for course in courses_db:
        if course.get("category").casefold() == category.casefold():
            courses_to_return.append(course)
    return courses_to_return

# Query ve Path aynı anda hem instructor hem categorye göre filtreleme felan:

@app.get("/courses/{course_instructor}/") #sonuna bir slash daha koyup hem path hem queryi aynı anda kullanmış oluyoruz.
async def get_course_instructor_category_by_query(course_instructor:str,category:str):
    courses_to_return = []
    for course in courses_db:
        if course.get("instructor").casefold() == course_instructor.casefold() and course.get("category").casefold() == category.casefold():
            courses_to_return.append(course)
    return courses_to_return


#POST İŞLEMİ

@app.post("/courses/create_course")
async def create_course(new_course=Body()):
    courses_db.append(new_course)


#UPDATE İŞLEMİ
@app.put("/courses/update_course")
async def updated_course(updated_course=Body()):
    for index in range(len(courses_db)):
        if courses_db[index].get("id")==updated_course.get("id"):
            courses_db[index]=updated_course


#DELETE İŞLEMİ

@app.delete("/courses/delete_course/{course_id}")
async def delete_course(course_id:int):
    for i in range(len(courses_db)):
        if courses_db[i].get("id")==course_id:
            courses_db.pop(i)
            break