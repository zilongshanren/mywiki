---
title: ทดสอบสมรรถภาพ SharpZibLib กับไฟล์ที่ serialize คลาสเป็น binary
url: https://gametorrahod.com/sharp-zip-lib/
author: Sirawat Pitaksarit
published: '2017-06-12'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

## วัตถุประสงค์

ไฟล์เกมบางอันที่ serialize ทั้งคลาสเป็น binary ไว้ด้วยคอมโบ BinaryFormatter + CryptoStream (DES) เพื่อใส่พาสเวิร์ดมันก็ใช้ได้นะ แต่ออกมาใหญ่มาก

ก็เลยเปลี่ยนมาใช้การ compress ใส่พาสดีกว่า มาเจอ SharpZibLib ที่ดูดี สามารถทำ Zip, GZip, Tar ได้ แล้วก็อ่าน LZW ได้

## อุปกรณ์

**icsharpcode/SharpZipLib***SharpZipLib - #ziplib is a Zip, GZip, Tar and BZip2 library written entirely in C# for the .NET platform.*[github.com](https://github.com/icsharpcode/SharpZipLib)

## วิธีการทดลอง

หลังจากเรียนรู้วิธีใช้แล้วก็ได้เวลาทดสอบว่ามี compression เลเวลไหนให้ใช้บ้าง โค้ดที่ใช้ก็ประมาณนี้ครับ (Unity) เลเวลมีตั้งแต่ 0 ถึง 9 ลอง compress แล้วอ่านกลับมาด้วยว่าใช้เวลามากน้อยต่างกันแค่ไหน ไซส์ได้เท่าไหร่

## ผลการทดลอง

![](../../assets/83e4009d02a1ebe5.png)

**BZip2 (+DES CryptoStream)**

Compress Time Avg : 970 ms

Size : 690 KB → 137 KB

ไม่มี compression level ให้ใช้นะ แล้วก็ไม่มี password ด้วย เพราะงั้นเลยต้องยัดเข้า CryptoStream เองอีกรอบ

## อภิปรายผลการทดลอง

- จะเห็นว่าแค่ Zip Lv.1 ก็ช่วยได้มากแล้ว (ลดขนาดได้ตั้ง 72.75%) แต่ตั้งแต่ Lv.6 เป็นต้นไปเริ่มขาดทุนกับเวลาที่ใช้
- BZip2 ไม่มี Lv. ให้ตั้ง และได้ขนาดเล็กที่สุด เวลาที่ใช้ มากกว่า Lv.7 ของ Zip
- สำหรับ decompress time เท่าที่ลอง ไม่ว่าจะ compress ด้วย Lv. ไหนก็ใช้เวลาเท่าๆกัน
- เปลี่ยน ZipInputStream เป็น GZipInputStream แล้วผลออกมาเหมือนๆเดิมก็เลยไม่ได้ทดลองต่อ

## สรุปผลการทดลอง

ถ้าห่วงเรื่องเวลา compress ใช้ Zip compression Lv.5-6 ถ้าไม่ห่วงก็ใช้ BZip2 ครับ

## สิ่งที่ได้จากการทดลอง

- ได้รู้ว่าการ compress มีระดับต่างกันอย่างไร ใช้เวลาต่างกันอย่างไรบ้าง
- ได้รับความรู้ใหม่ๆในเรื่องโปรแกรมมิ่ง
- ได้ฝึกฝนทักษะการวิเคราะห์ของตนเองให้ดีขึ้น