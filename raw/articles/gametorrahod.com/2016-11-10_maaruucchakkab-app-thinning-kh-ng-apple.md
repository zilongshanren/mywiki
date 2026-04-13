---
title: มารู้จักกับ App Thinning (ของ Apple)
url: https://gametorrahod.com/app-thinning/
author: Sirawat Pitaksarit
published: '2016-11-10'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/21cc779cf707f135.png)

จาก[โพสต์ที่แล้วอันแสนยาวนาน](https://medium.com/%405argon/%E0%B8%8A%E0%B9%88%E0%B8%A7%E0%B8%A2%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2%E0%B8%AD%E0%B8%A2%E0%B8%B9%E0%B9%88%E0%B9%86%E0%B9%80%E0%B8%81%E0%B8%A1%E0%B8%97%E0%B8%B3%E0%B8%88%E0%B8%B2%E0%B8%81-unity-%E0%B8%81%E0%B9%87%E0%B8%AA%E0%B9%88%E0%B8%87%E0%B8%82%E0%B8%B6%E0%B9%89%E0%B8%99-app-store-%E0%B9%84%E0%B8%A1%E0%B9%88%E0%B9%84%E0%B8%94%E0%B9%89-c3fcce4b8ef1#.ktds0cyws)นี้

วันนี้พวกเราชาว Unity มีหนทางต่อสู้กับขนาดมหึมาที่เพิ่มขึ้นมาแล้วล่ะ มันเรียกว่า App Thinning ..ซึ่งก็คือสิ่งที่ Apple เพิ่มเข้าไปใน **iOS 9 (.0.2) **ตั้งแต่เดือนตุลาแล้ว

แต่วันนี้สดๆ [ Unity 5.3](http://blogs.unity3d.com/2015/12/08/unity-5-3-all-new-features-and-more-platforms/) ได้เพิ่ม

![](../../assets/247bf732cfbe557f.png)

![](../../assets/73ec079b79bf30e5.png)

Wow! เข้าใจว่ามันทำให้อัตโนมัติเลยมั้งเนี่ย ถึงเวลาแล้วที่เราจะมารู้กันว่าไอ้พวกนี้ทำไรได้

## App Slicing

ตั้งแต่ยุคที่ Apple บังคับให้ซัพพอร์ต 64-bit แอพก็ขนาดใหญ่มหึมาเพราะมันเรียกว่า Universal App ชื่อเหมือนจะดีแต่จริงๆแปลว่าในนั้นมีทั้ง 32 และ 64 ยัดอยู่ข้างใน (แล้วคนโหลดก็ต้องโหลดทั้งยวงนั่นแหละ)

ใหม่! App Slicing! ตอนเราส่งขึ้นไปก็ใหญ่เหมือนเดิมนั่นแหละแต่ตอนโหลดลงมามันจะเอามาแค่ที่จะใช้จริง (กี่ bit หรือ texture ขนาดเท่าไหร่) แปลว่าเกมที่ยัดภาพระดับ iPad แล้วคนใช้ iPhone โหลดไปนี่ คราวนี้ก็จะได้ภาพที่เล็กลงอัตโนมัติเลย

![](../../assets/2dd700330309f9b1.png)

แต่ถ้าผู้ใช้คนไหนไม่ยอมอัพ 9.0.2+ ก็ต้องทนได้อันมหึมาต่อไป

## Bitcode

ถ้าเรา build ด้วย Bitcode แล้วขนาดเกมเราจะใหญ่ขึ้นกว่า **100 MB!!! **แต่ไม่ต้องตกใจไปเพราะมันคือ Bitcode ที่เปรียบเสมือนโค้ดที่เกือบๆจะเป็นเกมแล้วแต่ยังไม่เป็น เรายกหน้าที่ compile ขั้นต่อไปให้ Apple นั่นเอง

ข้อดีคือทีนี้ถ้า Apple ออกฟังก์ชั่นใหม่ๆที่ทำให้แอพเร็วขึ้นเมื่อไหร่ แทนที่เราจะต้อง compile ใหม่แล้ว submit ใหม่ (และรอเวลาตรวจสอบนานเหี้ยๆใหม่) ทาง server เทพของ Apple ก็จะ compile ใหม่ให้เรา มีฟังก์ชั่นใหม่ทันใจ ดังนั้นถ้าใครที่เตรียมจะลอยแพเกมตัวเองแล้วกำลังจะอัพเดทเกมเวอร์ชั่นต่อไป อัพ Bitcode ขึ้นไปด้วยจะได้ทนทานต่ออนาคตมากขึ้น

## On Demand Resources

เทคนิคฮอตฮิตสำหรับยุคเกม energy+lives ที่ บ ทุนหนาใช้กัน เคยเล่นเกมแบบว่าโหลดมาเร็วมาก ดีใจจะได้เล่นแล้วพอกดเริ่มเกมเสือกได้รออีก 1 ชม. ไรแบบนี้มั้ยครับ คือเขาทำเพื่อ UX ที่ดีเพราะแทนที่จะยอมแพ้เลิกเล่นตั้งแต่โหลดมาจาก Store อย่างน้อยก็มีแอพอยู่ในเครื่องแล้ว (หรือโหลดภาพ asset ที่ localize เป็นเฉพาะภาษาของผู้ใช้ได้ด้วยครับ) คราวนี้ทาง Apple มีพื้นที่โฮสต์ของพวกนั้นให้เราเลย (แต่ถ้าทำเกมลง Google Play ด้วยสงสัยก็คงต้อง AWS กันต่อไป) อันนี้ไม่แน่ใจว่าใช้จาก Unity ยังไง

## App Thinning

App Slicing + Bitcode + On Demand Resources แปลตรงตัวก็คือทำให้แอพเล็กลง

อยากอ่านของจริงก็ไปนี่ได้ [https://developer.apple.com/library/tvos/documentation/IDEs/Conceptual/AppDistributionGuide/AppThinning/AppThinning.html](https://developer.apple.com/library/tvos/documentation/IDEs/Conceptual/AppDistributionGuide/AppThinning/AppThinning.html)