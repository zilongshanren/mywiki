---
title: ทดสอบขนาดไฟล์ binary serialize ภาค 2
url: https://gametorrahod.com/binary-zip/
author: Sirawat Pitaksarit
published: '2018-03-05'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

จากภาคแรก จะเห็นว่าจากไฟล์ C# Serialize ดิบๆถ้า zip แล้วสามารถลดขนาดได้ตั้งกว่า 70% แน่ะ แสดงว่าไฟล์ C# ที่ว่ามันมีข้อมูลที่ค่อนข้างเป็น pattern ตัว algorithm เลย zip ได้

ทีนี้มาค้นพบว่าใช้ C# Serializer นี่ไม่ฉลาดเลยก็เลยเปลี่ยนเป็น protobuf แล้ว มาดูกันว่าขนาดจะเปลี่ยนไปได้แค่ไหนถ้า zip แล้ว

ก่อนอื่นมี primer อยากให้รู้ว่า C# Serialize เอาข้อมูลคลาสยัดลงไปในไฟล์เยอะอยู่ ในขณะที่ protobuf ข้อมูลคลาสว่าอ่านยังไงไม่ได้รวมเข้าไปด้วยแต่ใช้คลาสอ่านที่ generate ขึ้นมา ข้อมูลก็แค่ข้อมูลจริงๆ (ก็คือ ถ้ารู้โครงสร้างเราจะอ่านให้มันไปเป็นตัวแปรคลาสอื่นก็ยังได้) เพราะแบบนี้ขนาดไฟล์ของ C# ก็เลยจะใหญ่กว่าอยู่

## หน้าตาของข้อมูล

เป็น Simfile 1 อัน มี Chart 4 อัน แต่ละ Chart มี Note ประมาณ 100–500 อัน

Note ตัวนึงมี field int string float อะไรงี้รวมกันประมาณ 15 อัน กับมี reference ไปหาอีกคลาสเก็บข้อมูลนึงอีก 5 อัน อันนึงมี bool string int อะไรงี้รวมกัน 3 อัน ก็รวมแล้วมี field ประมาณ 30 อัน

แถมยังมีขยะ serialize อยู่ด้วยเพราะตอนแรกไม่รู้ว่า C# มันแอบยัด backing field ของ auto property เข้าไปทั้งๆที่ไม่ได้อยากเก็บ ไอ้พวกนี้ถ้ารวมด้วยก็ Note ละอีกซัก 10 อัน

ถ้ารวมทั้งหมดก็มี field ประมาณ 40 fields * 300 notes *4 charts = 48,000 fields ใน 1 Simfile

เกมผมในเวอร์ชั่นแรกนี้ จะมีประมาณ 20 Simfile ที่ต้องติดไปกับเกม

## ผลการทดลอง

**C# Serializer : **909 KB <- ถ้าทำแบบนี้ที่เกมจะเพิ่มไป 20MB กับข้อมูลเหล่านี้

**C# Serializer -> DESCrypto -> BZip2 :** 178 KB (- 80.41%) <- ก่อนหน้านี้ใช้ท่านี้อยู่

**Protobuf -> DESCrypto :** 87KB (- 90.42%)

**Protobuf -> DESCrypto -> BZip2 :** **12 KB (- 98.67%)**

**Protobuf -> BZip2 -> DESCrypto : **88 KB (- 90.31%)

ถ้าเทียบเปลี่ยนจาก C# Serializer เปลี่ยนเป็น Protobuf แล้ว ขนาดก็เล็กลง **12/87 -> 86.2%** เลยครับ

## สรุปผลการทดลอง

- อย่าใช้ C# Serializer เลย หรือถ้าอยากใช้อย่างน้อยใช้ DataContract ไม่ใช่มา serialize ทั้งตัวแปรไปเลย
- compression algorithm ทำอะไร binary จาก protobuf ไม่ได้เลย แต่ใช้กับผลจาก DES encryption แล้วได้ผล ดังนั้นใส่ compression หลัง crypto จะดีที่สุด

## ประโยชน์ที่ได้รับจากการทดลอง

ขนาดเล็กลงจนแทบหายไปเลย กราบ protobuf

![](../../assets/d3ba172fe03bbf33.jpeg)