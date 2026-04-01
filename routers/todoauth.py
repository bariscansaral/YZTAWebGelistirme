from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from todomodels import User
from passlib.context import CryptContext # Şifreleme yapmak için oluşturulmuş bir kütüphane; kullanıcı parolalarını güvenli bir şekilde şifrelemek (hash) için kullanacağız.
from tododatabase import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # Token işlemlerini kolayca FastAPI kütüphanesiyle gerçekleştirmek için kullanacağız.
from jose import jwt, JWTError # JWT Encode (oluşturma) ve Decode (çözme) işlemleri için kullanacağız. Algoritmayı, secret keyi ve payload içeriğini burada belirleyeceğiz.
from datetime import timedelta, datetime, timezone
from starlette import status

router = APIRouter(
    prefix="/auth",             # Rota Öneki: Bu dosyadaki tüm endpoint'lerin başına otomatik olarak '/auth' ekler.
    tags=["Authentication"]     # Swagger UI (/docs) sayfasında tüm işlemleri 'Authentication' başlığı altında toplar ve düzenli tutar.
)

# Şifreleme işlemi için bcrypt algoritmasını kullanan bir instance (örnek) oluşturduk.
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY: Bu keyi kendin oluşturmak istemezsen Google üzerinden "random 32 character string generator" ile unique bir key alabilirsin.
# ALGORITHM: Şifreleme sırasında hangi matematiksel algoritmanın (HS256) kullanılacağını seçiyoruz.
SECRET_KEY = "fhqyqkZN3HJfe8gWF5ySvFgN4lvIVmjB"
ALGORITHM = "HS256"

def get_db(): # Şifrelenen kullanıcı bilgilerini veritabanına aktarmak ve sorgulamak için kullanıyoruz.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
# OAuth2_bearer: Tokenın hangi URL'den alınacağını sisteme tanıtıyoruz.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

class CreateUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    role: str
    phone_number: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Token oluşturma fonksiyonu: expires_delta parametresi tokenın ne kadar süre sonra geçersiz olacağını belirler.
# JWT Encode (Şifreleme) işlemi burada yapılır.
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    payload = {"sub": username, "id": user_id, "role": role} # Payload: Token içerisinde gizli olarak tutulacak kullanıcı verileri.
    expires = datetime.now(timezone.utc) + expires_delta # Çalıştığı andan itibaren belirlenen süre kadar geçerli olmasını sağlayan zaman ayarı.
    payload.update({"exp": expires})
    # Hangi veriyi, hangi gizli anahtar ve algoritma ile şifreleyeceğimizi belirtip tokenı üretiyoruz.
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# get_current_user: Gelen tokenı decode edip (çözüp) içindeki kullanıcı bilgilerini kontrol eder.
# Bu fonksiyonu todo.py içinde 'dependency' olarak vererek, giriş yapmayanların işlem yapmasını engelleyeceğiz.
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or ID!")
        return {"username": username, "id": user_id, "role": user_role}
    except JWTError:
        # Token geçersizse veya süresi dolmuşsa bu hata fırlatılır.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid!")

# Kullanıcının bilgilerini (kullanıcı adı ve şifre) veritabanındakilerle doğrulayan fonksiyon.
def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    # bcrypt_context.verify: Girilen ham şifre ile veritabanındaki şifrelenmiş (hashed) hali karşılaştırır.
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUser):
    # Yeni kullanıcıyı oluştururken şifreyi açık halde değil, .hash() ile şifreleyerek kaydediyoruz.
    user = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        is_active=True,
        hashed_password=bcrypt_context.hash(create_user_request.hashed_password),
        phone_number=create_user_request.phone_number
        )
    db.add(user)
    db.commit()

# Token Alma (Giriş) İşlemi:
# Kullanıcı giriş yaptığında (Login), kimlik bilgileri doğrulanır ve sistem tarafından bir 'Erişim Token'ı (JWT) üretilir.
# Bu token, kullanıcının 'Dijital Kimlik Kartı' gibidir.
# Sonraki tüm isteklerde (to do ekleme, silme vb.) bu token sunucuya gönderilir.
# Sunucu, gelen her isteğin gerçekten yetkili ve doğrulanmış bir kullanıcıdan geldiğini bu token üzerinden teyit eder.

# OAuth2PasswordRequestForm: Kullanıcıdan kullanıcı adı ve şifreyi standart bir form yapısında alır.
# 'Depends()' ile bu formun doldurulmasını zorunlu kılıyoruz (Bağımlılık Enjeksiyonu).
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    # 1. Kimlik Doğrulama: Formdan gelen bilgileri veritabanındaki (db) kayıtlarla karşılaştırır.
    user = authenticate_user(form_data.username, form_data.password, db)

    # 2. Hata Yönetimi: Eğer kullanıcı bulunamazsa veya şifre yanlışsa '401 Unauthorized' hatası fırlatır.
    # Bu, "Yetkisiz Giriş Denemesi" olarak kayıtlara geçer.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # 3. Sertifikalandırma: Doğrulanan kullanıcı için geçici bir 'Access Token' üretilir.
    # Oluşturduğumuz token ve ne kadar süre sonra geçersiz olacağını (Örn: 20 dk) burada belirliyoruz.
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    # 4. Yanıt: Kullanıcıya dijital anahtarını ve anahtarın tipini (Bearer) sözlük yapısında döner.
    return {"access_token": token, "token_type": "bearer"}