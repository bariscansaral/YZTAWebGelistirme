###SENKRON ÇALIŞMA
import time

def my_func1():
    start1 = time.time()
    print("1. Fonksiyon çalıştırılıyor...")
    time.sleep(5)
    print("1. Fonksiyon bitti.")
    end1=time.time()
    print(f"Birinci fonksiyonun çalışma süresi = {round(end1-start1,4)}")
    return 5

def my_func2():
    start2=time.time()
    print("2. Fonksiyon Çalıştırılıyor...")
    time.sleep(5)
    print("2. Fonksiyon bitti.")
    end2=time.time()
    print(f"İkinci fonksiyonun çalışma süresi = {round(end2-start2,3)} ")
    return 10

if __name__ == "__main__":
    print("\nSenkron Çalışma:")
    start3=time.time()

    x = my_func1()
    y = my_func2()

    print(f"my_func1 çalışması sonucunda x'in değeri = {x}")
    print(f"my_func2 çalışması sonucunda y'nin değeri = {y}")
    end3=time.time()
    print(f"Toplam geçen süre = {round(end3-start3,4)}\n\n")



###ASENKRON ÇALIŞMA

import asyncio

async def my_func3():
    start4 = time.time()
    print("3. Fonksiyon çalıştırılıyor...")
    await asyncio.sleep(5) #non blocking delay simülasyonu
    print("3. Fonksiyon bitti.")
    end4=time.time()
    print(f"Üçüncü fonksiyonun çalışma süresi = {round(end4-start4,4)}")
    return 5

async def my_func4():
    start5=time.time()
    print("4. Fonksiyon Çalıştırılıyor...")
    await asyncio.sleep(5)
    print("4. Fonksiyon bitti.")
    end5=time.time()
    print(f"Dördüncü fonksiyonun çalışma süresi = {round(end5-start5,3)} ")
    return 10

async def main():
    print("\nAsenkron Çalışma:")
    start6=time.time()

    task1=asyncio.create_task(my_func3())
    task2=asyncio.create_task(my_func4())
    x=await task1
    y=await task2

    print(f"my_func3 çalışması sonucunda x'in değeri = {x}")
    print(f"my_func4 çalışması sonucunda y'nin değeri = {y}")
    end6=time.time()
    print(f"Toplam geçen süre = {round(end6-start6,4)}\n\n")

if __name__ == "__main__":
    asyncio.run(main())