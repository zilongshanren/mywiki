---
title: ทำไม virtual method ถึงใช้คีย์เวิร์ด virtual
url: https://gametorrahod.com/why-virtual-called-virtual/
author: Sirawat Pitaksarit
published: '2018-04-19'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/be2b1fa1bbefaa93.jpeg)

ใน C# เราสามารถสร้างเมธอดที่สามารถ override ได้ใน inheritance โดยการใส่ virtual modifier

ทางด้านชื่อ override ในฝั่ง subclass ยังพอเข้าใจง่าย แต่ทำไมจะ override ได้ ต้อง “จำลอง (virtual)” ใน superclass?

อันที่จริงแล้วมันมีสิ่งที่เรียกว่า Virtual Method Table หรือ vtable เป็นสิ่งที่เตรียมไว้ตอน compile time เต็มไปด้วย pointer ชี้ไปที่เมธอดต่างๆที่คลาสนั้นมีอยู่ เพื่อให้ตอน runtime สามารถมา lookup ดูได้ว่าควรจะเลือกใช้เมธอดไหน ที่ต้องเลือกเพราะเช่นกรณี runtime polymorphism

**Virtual method table - Wikipedia***Whenever a class defines a virtual function (or method), most compilers add a hidden member variable to the class which…*[en.wikipedia.org](https://en.wikipedia.org/wiki/Virtual_method_table)

ก็คือ ที่ call site มีการเรียกเมธอดนึงจากตัวแปรตัวนึงแล้วจะต้องวิ่งไปหาให้ถูกอัน เวลาคลาส A ทำ virtual ไว้แล้ว B ทำ override ไว้ แต่ละตัวแปรจะมี pointer 1 ตัวที่ชี้ไปที่ vtable ที่ตัวเองควรจะได้ ทำให้เรียกถูกอัน

เช่น A a = new A(); กับ A a2 = new B(); แบบนี้สองตัวนี้เรียกฟังก์ชั่นไปลงอันต่างกัน ใช้ตาดูเหมือนจะ solve at compile time ได้ แต่กรณีที่ไม่ได้ก็มี

**Why can't run-time polymorphism be solved at compile time?***Because in the general case, it's impossible at compile time to determine what type it will be at run time. Your…*[stackoverflow.com](https://stackoverflow.com/questions/34354516/why-cant-run-time-polymorphism-be-solved-at-compile-time?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)

ใน C# นี้ทุกๆตัวแปรมี vtable แน่นอนเพราะทุก object สืบทอดมาจาก System.Object ที่มี virtual เช่น .ToString() virtual method ก็คือ method ที่ไม่รู้ขณะอยู่ใน compile time ว่าจะเรียกอันไหนดี ต้องปรึกษา vtable ตอน runtime นั่นเอง ใน intermediate languate ของ C# นี่มีคำสั่งเฉพาะชื่อ callvirt แยกออกมาจาก call ด้วย

**List of CIL instructions - Wikipedia***This is a list of the instructions in the instruction set of the Common Intermediate Language bytecode.*[en.wikipedia.org](https://en.wikipedia.org/wiki/List_of_CIL_instructions)

แต่มี lookup ก็ใช่ว่าจะช้า อย่าง IL2CPP ของ Unity ก็สามารถทำ “devirtualization” ได้ถ้ามันคิดว่าชัวร์ๆว่าจะลงเมธอดไหนแน่ๆ

**IL2CPP Optimizations: Devirtualization - Unity Blog***Modern compilers are excellent at performing many optimizations to improve run time code performance. As developers, we…*[blogs.unity3d.com](https://blogs.unity3d.com/2016/07/26/il2cpp-optimizations-devirtualization/)

ถ้าอ่าน จะรู้ว่าหนึ่งในสิ่งที่ทำให้ IL2CPP มั่นใจได้คือคีย์เวิร์ด sealed แล้วมันจะเอา virtual call ออกไปแทนที่ด้วยฟังก์ชั่นปกติเลย ดังนั้น sealed ก็เป็น optimization ลับนึงของการทำ Unity นะครับ ไม่เคยใช้เลยล่ะสิ (*ผ่าง*) (ผมก็ไม่เคย)