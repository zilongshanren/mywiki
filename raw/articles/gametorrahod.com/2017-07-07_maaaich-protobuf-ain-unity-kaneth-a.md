---
title: มาใช้ Protobuf ใน Unity กันเถอะ
url: https://gametorrahod.com/protobuf-in-unity/
author: Sirawat Pitaksarit
published: '2017-07-07'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/74b896a65525a22b.png)

Protocol Buffer หรือ protobuf เป็นเครื่องมือกำหนดโครงของ serialized data จาก Google ที่สามารถสร้างโค้ดตัวอ่านข้อมูลส่วนตัวของเราได้ในภาษาเป้าหมาย (ไม่ต้องเขียน parser) ได้ข้อมูลเล็กกว่า XML เหมาะจะส่งไปมาเพราะตัวอ่านอ่าน binary เข้าใจอยู่แล้ว แล้วก็มีกลไก versioning ไม่ให้ field ใหม่ทำเวอร์ชั่นเก่าพัง ไปอ่านรายละเอียดกันเองในนี้

**Protocol Buffers | Google Developers***Protocol buffers are a language-neutral, platform-neutral extensible mechanism for serializing structured data.*[developers.google.com](https://developers.google.com/protocol-buffers/)

เกมผมเวลาจะเซฟข้อมูลเกมเป็น binary พึ่งพาตัว serialize คลาสของ C# มาตลอด ( [System.Serializable] แปะที่หัวคลาสแล้วก็ยัดลง binary ได้เลย) แต่ข้อเสียคือขนาดออกมาค่อนข้างใหญ่ แตะนิดเพิ่ม field หน่อยมีโอกาสพัง จริงๆเพิ่มไม่ค่อยพังหรอกแต่ลดกับเปลี่ยนชื่ออะพัง (จริงๆ .NET ก็มี attribute สำหรับ mark ได้ว่า field ไหนของเวอร์ชั่นไหนนะ แต่ไม่สู้ protobuf…)

ที่สำคัญ! ไฟล์ binary ที่ได้ต้องอ่านโดย C# เท่านั้นเพราะมีแค่ .NET ที่เข้าใจก้อน class ที่ว่านี้ (แถมต้องมี definition ของ class ที่ถูกต้องไว้รอ) อันนี้ พอดีผมอยากจะทำระบบ scoreboard บนเว็บซักวัน โดยอ่านข้อมูลจากไฟล์เซฟของผู้เล่นได้โดยตรงเลย (จะได้ backup เซฟผู้เล่นได้ในตัวด้วย) จะให้ JS อ่านคลาส .NET ได้มันคงยาก

Solution แรกที่คงคิดคือทำเป็น JSON หรือ XML มั้ย แต่ดูยังไง protobuf ก็ดีกว่าถ้าจะเชื่อม JS กับ C# เข้าด้วยกันแน่นๆ เพราะคลาสอ่านเขียนที่ปลายทาง generate ขึ้นมาจาก definition .proto เดียวกัน (แถมขนาดยังเล็กกว่ามาก)

## แจกเครื่องมือ

การเสกโค้ด C# จาก protobuf ที่ว่าต้องใช้เครื่องมือ protoc จาก Google (จาก command line) แต่เพียงแค่เราใช้ plugin นี้ที่ผมเขียนขึ้นมา (โฆษณาหน่อย) ทุก .proto ในโปรเจคก็จะโดน generate เป็น C# อัตโนมัติเลยครับ (ทุกครั้งที่แก้ไขมันด้วย)

![](../../assets/10422a2a38492956.png)

**5argon/protobuf-unity***protobuf-unity - Automatic .proto files compilation in Unity project to C# as you edit them.*[github.com](https://github.com/5argon/protobuf-unity)

## ต้องแก้โปรเจคเยอะมั้ยแบบนี้

คลาสที่ออกมาจะเป็น sealed partial ดังนั้นเราสามารถใช้สมบัตินี้ในการเสกคลาสชื่อเดียวกันกับของในเกมเราให้มัน partial มาทับกันได้ครับ ดังนั้นลบออกแค่ส่วนตัวแปรที่จะเก็บข้อมูลก็พอ พวก logic สามารถเก็บไว้ได้ แล้วก็แก้ชื่อตัวแปรมาเป็นของที่เสกมาจาก protobuf แค่นั้น

![](../../assets/d39ba7942cdfdb4c.png)

![](../../assets/7aeee15d190247cd.png)

comment โค้ดตัวแปรเก่าแล้ว เพราะอันใหม่จะมาจากไฟล์ .proto (ชื่อเหมือนๆกันพอดี แก้ไม่มาก) ชื่อ message ตั้งชื่อให้ตรงกับชื่อคลาสที่อยากเสก คือ message NoteJudgeRecord

เรื่องการเล็งชื่อตัวแปรหรือไฟล์เพื่อให้โป๊ะเชะกับโปรเจค ลองอ่านนี่ดูเขียนไว้ใน repo เป็นภาษาอังกฤษ

- Use CamelCase (with an initial capital) for message names — for example, SongServerRequest. Use underscore_separated_names for field names — for example, song_name.
- By default of C# protoc, the underscore_names will become PascalCase and camelCase in the generated code.
- .proto file name matters and Google suggests you use underscore_names.proto. It will become the output file name in PascalCase. (Does not related to the file's content or the message definition inside at all.)
- Field index 1 to 15 has the lowest storage overhead so put fields that likely to occur often in this range.
- The generated C# class will has sealed partial.
- You cannot use enum as map's key.
- It’s not int but int32. And this data type is not efficient for negative number. (In that case use sint32)

ตัวอย่างการแปลง

![](../../assets/c43fcfa5384d8a16.png)

เสก partial ออกมาเสร็จแล้ว แก้ชื่อตัวแปรใหม่ให้ตรงกับที่เสกก็เป็นอันเสร็จ ถ้าใช้ accessor ชื่อแบบ PascalCase อยู่แล้วยิ่งไม่ต้องทำอะไรเลย

![](../../assets/1170f324acb98765.png)

![](../../assets/1ae3cdab9c6b5fa0.png)

![](../../assets/05a9e15e9d62ed34.png)

ส่วน repeated จะออกมาเป็นคล้ายๆ List<> และ map จะออกมาเป็นคล้ายๆ Dictionary<,> ตรงนี้อาจจะต้องแก้เยอะนิดนึงถ้าไม่ตรงกับข้อมูลเก่า

ต่อไปก็ไปแก้ในส่วนการ serialize ข้อมูลในเกมเรา โดย Google ได้เตรียมของดีไว้ให้ ไปดูได้ใน [https://developers.google.com/protocol-buffers/docs/csharptutorial#parsing-and-serialization](https://developers.google.com/protocol-buffers/docs/csharptutorial#parsing-and-serialization) เลยครับ

ในคลาสเสก ดูดีๆมีของเล่นแถมมาด้วยอย่าง MergeFrom Clone WriteTo ToString GetHashCode Equals เอามาใช้ได้ตามสบายครับ

## Enums

ใน message ของ protobuf นี่เราสามารถใช้ enum ได้ด้วย แต่แน่นอนว่าต้องมี enum definition อยู่ในไฟล์ proto หรือไฟล์ proto อื่นที่ import เข้ามา ดังนั้นเรามาย้าย enum ทุกตัวในเกมที่กะว่าจะให้ protobuf อ่านด้วยเกมก็อยากอ่านด้วย มาไว้ใน .proto ใหม่กันดีกว่า

![](../../assets/7fbd3affc6939a56.png)

เดิมทีในเกมมี enum ที่ไม่อยู่ใน scope class ใดๆเพื่อให้ใช้ด้วยกันได้ แต่กลายเป็น protobuf ใช้ด้วยกันไม่ได้

ใน protobuf ก็ทำแบบเดียวกันได้ด้วยการประกาศ enum ไว้นอก message (ขวา) แล้วมันจะออกมาเป็น enum นอก class ใน C# ครับ (กลาง) ดังนั้นออกมาแล้วก็ลบ enum เดิมในโปรเจคออกได้ (ซ้าย) ดีด้วยจะได้มีไฟล์ไว้เก็บรวบรวม enum ที่ใช้ประจำในรูปแบบ .proto ไฟล์ .proto อื่นอยากจะใช้ด้วยก็ใช้ import "enums.proto"; อะไรงี้

## Protobuf ไม่ปลอดภัย

ถึงจะบอกว่าเป็น binary ก็ตามแต่ก็แค่ byte เรียงกันโง่ๆ (index กับข้อมูลสลับกัน) ดังนั้นถึงไม่มีไฟล์ .proto ในครอบครองก็แฮคค่าดูไม่ยากโดยการทดลองเปลี่ยนข้อมูลแล้วดูว่าตรงไหนเปลี่ยน แล้วพยายามตีความดูเองก็ยังได้

ตัวอย่างเช่น ดูภาพบนสุดของหน้านี้ อันนั้นที่จริงเป็นไฟล์คะแนนของเกมผม สมมติถ้าไปอ่านหน้า [https://developers.google.com/protocol-buffers/docs/encoding](https://developers.google.com/protocol-buffers/docs/encoding) มาแล้ว เล็งดูแปปเดียวก็รู้ว่า field ชื่ออะไรมันอยู่ byte แถวๆไหน

ดังนั้นใช้ encryption ด้วย ตามสะดวก อันนี้ตัวอย่างท่า Save

![](../../assets/4926d84d2abe6a47.png)

อันนี้ตอน Load

![](../../assets/33a8a45acddd868b.png)

ปล. ถ้าไม่ using Google.Protobuf; จะไม่สามารถแปลง stream เป็น Input/OutputCodedStream แบบ implicit ได้ มันจะเออเร่อตรง WriteTo กับ ParseFrom

## ขนาดเล็กลงแค่ไหน

ไฟล์เล็กๆที่เก็บอะไรไม่มาก จากเดิม 1KB (1416 bytes) เล็กลงเหลือแค่ 208 bytes

![](../../assets/a95579ce9d6697a5.png)

เข้าใจว่าถ้าเก็บข้อมูลเพิ่มทางฝั่ง Protobuf ความห่างอาจจะลดลงรึเปล่า เพราะทาง C# Serialize อาจจะจองที่ไว้ตั้งแต่แรก แต่ยังไงก็ตามที่ไฟล์พอๆกันเล็กลง 6.8 เท่าแน่ะ! ลองเอาผลต่างไปคิดค่าขนส่งข้อมูลกับค่าเก็บข้อมูลของ AWS, Firebase ดูว่าผ่านไป 70 ปีมันจะทำลายแผนเกษียณของเราได้มั้ย