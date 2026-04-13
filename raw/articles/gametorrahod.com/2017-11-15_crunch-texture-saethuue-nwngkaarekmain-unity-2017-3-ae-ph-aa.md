---
title: Crunch Texture สะเทือนวงการเกมใน Unity 2017.3 แอพอาจเล็กลงได้ 20% ฟรีๆ
url: https://gametorrahod.com/crunch-texture/
author: Sirawat Pitaksarit
published: '2017-11-15'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/6ab4fed067da9698.png)

ใครทำเกมจะรู้ว่าขนาดเกมเกินกว่าครึ่ง (น่าจะซัก 80%) เสียไปกับ Texture ครับ ถึงแม้ว่าจะพยายาม compress แล้วก็ตาม…

## รู้จักกับไฟล์ภาพบีบอัด

BMP นี่คือไฟล์เปลือยๆที่เก็บสีเป็นเม็ดๆเลยไม่มีเพี้ยน ส่วน JPEG ก็เล็กและเละ กับ PNG เล็กพอควร ไม่เละ แถมใสได้ด้วย ทางคอมรู้จักกันประมาณนี้ใช่มั้ยครับ

ทางมือถือจะมีบีบอัดอีก format ชุดนึงที่ออกแบบมาให้อยู่ใน GPU ได้ทั้งอย่างนั้นเลย (เอา PNG เข้า GPU มันไม่รู้เรื่องนะ ต้อง decompress ก่อน) คือ

- DXT — ใช้กับ GPU Tegra ของ Nvidia ได้ (หายาก เช่น Nvidia Shield) กับใช้กับเกมคอมได้
- PVRTC — ใช้ GPU Power VR ก็คือมือถือ Apple ได้ทุกรุ่นกับ Android หายากบางรุ่น อันนี้ภาพออกมาดูโง่ๆเพราะใช้อัลกอริทึมเก็บภาพหลายขนาดแล้วมา blend กัน เกลียดเป็นการส่วนตัว
- ASTC — อันนี้เทพ บ. ARM เป็นคนคิด แต่ใช้ได้กับหลายเครื่องที่ใหม่ๆหน่อย ถ้าของ Apple เครื่องที่ A8 ขึ้นไป (iPhone SE+) จะใช้ได้ Android ใหม่ๆก็ใช้ได้
- ATC — ใช้กับ GPU Adreano อันนี้หาได้ง่ายใน Android เพราะไส้ในส่วนมากมาจาก Qualcomm (Snapdragon)
- ETC — มาตรฐานโดย OpenGL ใช้ได้ทุกเครื่อง 100% แต่เวอร์ชั่นแรกดันทำใสไม่ได้ เวอร์ชั่น 2 ใสได้แต่ดันต้องมี OpenGL 3.0+ ทำให้เกิดความกังวลอีกว่าเครื่องไหนจะเละ (ตอนนี้น่าจะพ้น 2.0 เยอะแล้ว?)

ที่เขียนว่าใช้ได้ คือถ้าทำเป็นแบบนั้นไปแล้วใช้ไม่ได้ขึ้นมาจะเสียเวลา decompress แถมขนาดบานใน RAM อีก (แต่ขนาดเก็บในแอพก็เล็กตามที่ compress) ซึ่งเราไม่สามารถเลือกทำหลายๆ format ไปได้ (ใครจะยอมเสียที่เกม 2–4 เท่าต่อภาพทั้งๆที่ตั้งใจ compress ให้ที่เกมเล็กลง) ทาง Android เลยมีกลยุทธ์แยก APK ให้แต่ละเครื่องได้เกมที่บีบภาพคนละแบบไปได้

**Multiple APK Support | Android Developers***Multiple APK support is a feature on Google Play that allows you to publish different APKs for your application that…*[developer.android.com](https://developer.android.com/google/play/publishing/multiple-apks.html)

เนื่องจาก iPhone มี 2 ตัวเลือก (ไม่นับ ETC) การประชัน PVRTC กับ ASTC เคยพิมพ์ไว้แล้ว ไปอ่านเพิ่มเติมได้ครับ

**PVRTC vs ASTC texture compression on an iOS device***PVRTC is the default, but did you know from A8 onwards iOS now supports ASTC? (and perhaps you are not taking advantage…*[gametorrahod.com](https://gametorrahod.com/pvrtc-vs-astc-texture-compression-on-an-ios-device-38278a2345d)

## แล้ว Crunch คืออะไร!

**BinomialLLC/crunch***crunch - Advanced DXTc texture compression and transcoding library*[github.com](https://github.com/BinomialLLC/crunch)

เป็น format เทพที่เชื่อมกับ DXT แปลงไปแปลงมาได้อย่างรวดเร็ว มีจุดอ่อนแค่ว่าตอน compress เสียเวลาสุดๆ แต่ขนาดที่ได้มันทำให้ผมต้องอึ้ง (ไม่มีคลิป)

![](../../assets/6ab4fed067da9698.png)

โว้ว! จาก ETC โง่ๆขนาด 0.5 MB (500 KB) เล็กลงเหลือ 100 KB! เล็กลง 5 เท่า! (ขนาดเต็มๆ RGB16 ก็คือ 1024x1024x2 = 2MB)

แต่ข้อเสียคือมันแปลงเป็น DXT นั่นแหละครับพอการ์ดจอมาเห็นแล้วใช้ไม่ได้ก็จะเกิดการงอกเป็น RGB(A) เต็มๆ (แต่ภาพที่เห็นยังเป็นแบบ compress อยู่) เพื่อที่จะได้โยนเข้าการ์ดจอได้ ซึ่งก็จะทำให้ขนาดใน RAM เป็น 2MB แถมยังเสียเวลา uncompress ด้วย (นานพอควรนะผมเคยลอง) เรียกได้ว่าอยากดันทุรังให้เกมเล็กๆในมือถือก็ได้ แต่ต้องโดนทำโทษตอนใช้จริง

## Unity 2017.3

ทีนี้! ใน Unity เวอร์ชั่น 2017.3 ที่จะมาเขาบอกว่าทำให้ crunch ใส่ ETC ได้แล้ว (ทำอีท่าไหน)

**Updated Crunch texture compression library - Unity Blog***Crunch is a lossy texture compression format, which is normally used on top of DXT texture compression. Crunch…*[blogs.unity3d.com](https://blogs.unity3d.com/2017/11/15/updated-crunch-texture-compression-library/)

ก็แปลว่าเราสามารถได้ไฟล์ขนาดเล็กที่เล่นได้ทุกเครื่องแน่นอนครับ! ถ้าขนาด texture กิน 80% จริง ใช้ crunch หมดทั้งเกมนี้มีสิทธ์ลดขนาดเกมได้ฟรีๆตั้งเกือบ 20% แน่ะ! Wow! (แต่ตอนมัน crunch จะกินเวลานานมาก คงจะทรมานตอนที่จำเป็นต้อง reimport)