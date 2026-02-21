##PYDANTIC NE İŞE YARAR NEDİR

#PYDANTICSIZ VERİ TİPLERİNİ KARARLAŞTIRIP FARKLI VERİ TİPİ VERME:
print("--------Pydantic Öncesi--------\n")
class ProductWithoutPydantic:
    def __init__(self, name: str, price: float, in_stock: bool):
        self.name = name
        self.price = price
        self.in_stock = in_stock
if __name__ == "__main__":
    external_data={
        "name":"Laptop",
        "price":"5999.99",
        "in_stock":"True"
    }
    product=ProductWithoutPydantic(
        name=external_data.get("name"),
        price=external_data.get("price"),
        in_stock=external_data.get("in_stock")
    )
    print(product.name,type(product.name))
    print(product.price, type(product.price))
    print(product.in_stock, type(product.in_stock))
    """Yukarıda asıl sınıfta price name ve in_stock verilerinin tiplerini belirtmemize rağmen hepsini zorla str şeklinde atayabildik ve hata almadık.
    Biz aslında name için str price için float in stock için boolean tiplerini kullanmak istemiştik ve buna zorlamaya çalıştık ancak
    python esnek olduğu için sıkıntısız bu kodları çalıştırdı."""

#PYDANTIC İLE AYNI İŞLEMLER:

from pydantic import BaseModel

class ProductWithPydantic(BaseModel):
    name:str
    price:float
    in_stock:bool
    #Base Model kullandığımız için __init__ kullanmamıza gerek yok!
print("\n--------Pydantic Sonrası--------\n")
if __name__ == "__main__":
    external_data={
        "name":"Laptop",
        "price":"5999.99",
        "in_stock":"True"
    }
    product_pydantic=ProductWithPydantic(
        name=external_data.get("name"),
        price=external_data.get("price"),
        in_stock=external_data.get("in_stock")
    )
    print(product_pydantic.name,type(product_pydantic.name))
    print(product_pydantic.price, type(product_pydantic.price))
    print(product_pydantic.in_stock, type(product_pydantic.in_stock))

    """Çıktıya baktığında eğer verileri düzgün girersen gerekli dönüşümleri yaptığını görebilirsin. Boolean kısmına "True" yerine "asdasd"
    felan yazsaydık hata verirdi, düzgün yazmış olmak önemli"""