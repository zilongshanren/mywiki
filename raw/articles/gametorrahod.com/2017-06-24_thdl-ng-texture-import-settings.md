---
title: ทดลอง Texture Import Settings
url: https://gametorrahod.com/texture-import-settings/
author: Sirawat Pitaksarit
published: '2017-06-24'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

## Pack vs. Single POT

ภาพ 512x256 จำนวน 64 ภาพเหมือนกัน แต่ชุดแรกเป็นแบบเดี่ยวๆให้ compress ด้วยพลัง power of two แต่ละภาพ (กติกาของ Android ไม่ต้องจตุรัสก็ได้) อีกชุดให้ pack ลง 2048x2048 สองแผ่นพอดี ซึ่งขนาดภาพแต่ละภาพเล็กลงนิดหน่อยเพราะ Unity มันมี padding power อยู่ 2 pixel

โค้ดโปรเจคทดสอบนี้ออกแบบไว้ให้ใช้ภาพทั้งหมดในโปรเจคแล้ว ตามภาพ ดังนั้นทุกภาพต้องถูกใส่ลงไปใน build

![](../../assets/e2b892093e4bbef7.png)

![](../../assets/0802a26ec6116739.png)

ใน Import Settings บอกว่าภาพขนาด 64 KB

![](../../assets/20f9c7661dfbb0c7.png)

ใน Import Settings บอกว่าภาพขนาด 378 KB แต่ขนาดจริงน่าจะต้องรอ Atlas

![](../../assets/8467ce2420002bde.png)

ภาพหลัง pack แล้ว

![](../../assets/0cfc89b3f06b2c92.png)

![](../../assets/00ff79c985283a7c.png)

ผลหลังจาก build ออกมา (ทำไม inf% nan%) พบว่า

- ในรายการ build มีบรรทัด atlas อันเดียว ถึงจริงๆแล้วจะมี 2 แผ่น atlas ก็เถอะ
- เหมือนนอกจากจะมีแผ่นใหญ่ข้างบนสุดแล้วยังมีวิญญาณอยู่ข้างล่างอีก แต่ขนาดเล็กกว่า

ผลสรุปคือ

**แบบ atlas**

`4000 KB + (0.4 KB * 12) + (0.3 KB * 52) = 4020.4 KB`


**แบบ compress power of two เดี่ยวๆ**

`(64.5 KB * 12) + (64.4 KB * 52) = 4122.8 KB`


แบบ atlas ขนาดชนะนิดนึง แถมตอน draw น่าจะดีต่อ draw call มากกว่า ถ้าบังเอิญภาพอยู่ใน atlas แผ่นเดียวกัน เพราะงั้นเราควรใช้แบบ atlas ที่ภาพเล็กลงมากว่า power of two นิดนึงให้ pack ได้

(แล้วตกลง 378 KB ที่โชว์มันคืออะไร)

## Compression Quality

ทีนี้เราจะมาทดลองแบบเดิมแต่เปลี่ยน Compression Quality กันดูครับ

![](../../assets/f3deeb3033ab2526.png)

ซึ่ง High แปลว่าเสียเวลา compress นาน แล้วตอนใช้กิน memory มากกว่า แต่น่าจะเล็กกว่า เขาว่างั้น

![](../../assets/291098e416376966.png)

Low Quality

![](../../assets/2f84c59bfa1af717.png)

ผลคือเหมือนเดิม

High Quality

![](../../assets/3d0707664dc6e51f.png)

ผลก็ยังเหมือนเดิม (อ้าว!)

### Compression Quality อีกอัน

แต่เดี๋ยวก่อน! ยังมี option ลับอีกอย่างที่ต้องตั้งจากโค้ดซึ่งมีค่าตั้งแต่ 0 ถึง 100 (ปกติคือ 50)

![](../../assets/be08d18ef7ff4086.png)

**Quality : 100 + HQ Compression**

เอาแบบสุดติ่งไปเลยทีนี้

![](../../assets/18f78ad4977d5959.png)

Reimport นานมาก ประมาณภาพละ 6–10 วิ แสดงว่าต้องรอ 1280 วินาทีถ้าเราไปแตะต้องอะไรก็ตามที่ทำให้ต้อง import ใหม่ (21 นาที!!)

จริงๆไม่ถึง ประมาณ 10 นาทีก็เสร็จ ผลลัพธ์คือ

![](../../assets/d39abcdd829013a4.png)

เหมือนเดิม (อ้าว!)

สำหรับคนสงสัยว่าขนาด APK อาจจะต่างกันมากก็ได้

![](../../assets/b4f9a679f351f517.png)

## Crunch Texture

ยังมีอีก! เทคโนโลยี Crunch นี้ค่อนข้างใหม่ ([https://github.com/BinomialLLC/crunch](https://github.com/BinomialLLC/crunch)) เสียเวลา crunch นิดๆแต่ขนาดเล็กลงมาก เครื่องที่รับ DXT Texture ได้จะสามรถใช้ Crunch Texture ได้เลย แต่เครื่องที่ว่ามีน้อย (พวก Tegra) ถ้าเครื่องไหนรับไม่ได้ขึ้นมามันจะ**บานเป็น RGBA 32 bit** ทันที แต่ก็ดีที่เซฟขนาด APK ได้ (ถ้ายอมโดนบานไหว RAM เยอะจัด หรือเป็นภาพ key จริงๆที่อยากจะให้ดูแปปเดียวแต่ภาพใหญ่)

![](../../assets/8b2f6663b81ffb6b.png)

![](../../assets/c5fc74c5c7f36dc8.png)

อันนี้ไม่รู้เหมือนกันว่าทำไม Fast แล้วขนาดยิ่งเล็กลงอีกได้ ขนาดที่เห็นคือขนาดเมื่ออยู่ใน memory นะครับ

แล้วก็ Crunch ที่ให้ติ้กหน้าแรกลองติ๊กแล้วไม่มีผล ต้องมาหน้า Android

![](../../assets/b32d18170242e058.png)

เมื่อลอง reimport และ build ดู

![](../../assets/2aeb7c63db521ef6.png)

![](../../assets/a938d22b86211722.png)

![](../../assets/b32aef121be6e714.png)

![](../../assets/3d0eeec11fd02f21.png)

![](../../assets/59ec04b0413969b6.png)

จะเห็นว่าผลคือขนาดเล็กลงแล้วครับ

![](../../assets/158d67ffe2f1e6f0.png)