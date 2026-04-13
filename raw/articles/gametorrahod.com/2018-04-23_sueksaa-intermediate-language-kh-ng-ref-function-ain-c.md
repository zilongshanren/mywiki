---
title: ศึกษา intermediate language ของ ref function ใน C#
url: https://gametorrahod.com/ref-intermediate-language-csharp/
author: Sirawat Pitaksarit
published: '2018-04-23'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/b96d5eb2901100a1.jpeg)

เรียนจบมาซะนานแล้ว มา throwback สู่วิชา compiler กันบ้าง… ผมสงสัยว่าการส่งของ value type เข้าไปใน ref นี่มันประหยัดกว่าก๊อปเข้าไปตรงๆในทาง IL อย่างไร มาลองศึกษากันดีกว่าครับ

## Ref vs NoRef

```
using System;
public class Program
{
public static void Main()
{
int z = 999;
int x = 555;
int c = 333;
Ref(ref z);
Ref(ref c);
NoRef(x);
}
private static void Ref(ref int a)
{
a += 1;
}
private static void NoRef(int a)
{
a += 1;
}
}
```


IL :

```
// =============== CLASS MEMBERS DECLARATION ===================
.class public auto ansi beforefieldinit Program
extends [mscorlib]System.Object
{
.method public hidebysig static void Main() cil managed
{
//
.maxstack 1
.locals init (int32 V_0,
int32 V_1,
int32 V_2)
IL_0000: nop
IL_0001: ldc.i4 0x3e7
IL_0006: stloc.0
IL_0007: ldc.i4 0x22b
IL_000c: stloc.1
IL_000d: ldc.i4 0x14d
IL_0012: stloc.2
IL_0013: ldloca.s V_0
IL_0015: call void Program::Ref(int32&)
IL_001a: nop
IL_001b: ldloca.s V_2
IL_001d: call void Program::Ref(int32&)
IL_0022: nop
IL_0023: ldloc.1
IL_0024: call void Program::NoRef(int32)
IL_0029: nop
IL_002a: ret
} // end of method Program::Main
.method private hidebysig static void Ref(int32& a) cil managed
{
//
.maxstack 8
IL_0000: nop
IL_0001: ldarg.0
IL_0002: dup
IL_0003: ldind.i4
IL_0004: ldc.i4.1
IL_0005: add
IL_0006: stind.i4
IL_0007: ret
} // end of method Program::Ref
.method private hidebysig static void NoRef(int32 a) cil managed
{
//
.maxstack 8
IL_0000: nop
IL_0001: ldarg.0
IL_0002: ldc.i4.1
IL_0003: add
IL_0004: starg.s a
IL_0006: ret
} // end of method Program::NoRef
```


มาเริ่มกันที่ main

```
.locals init (int32 V_0,
int32 V_1,
int32 V_2)
```


ตัวแปร local ทั้ง 3 ตัวได้ address เป็นของตัวเอง

```
IL_0000: nop
IL_0001: ldc.i4 0x3e7
IL_0006: stloc.0
IL_0007: ldc.i4 0x22b
IL_000c: stloc.1
IL_000d: ldc.i4 0x14d
IL_0012: stloc.2
```


ค่า 999 555 333 เข้าไปอยู่ในตัวแปรด้วย load constant ขึ้น stack แล้ว store local เพื่อเอาค่าบน stack ตะกี้ไปใส่ local variable

nop เอาไว้วาง breakpoint เพราะโค้ด build ในโหมด debug

```
IL_0013: ldloca.s V_0
IL_0015: call void Program::Ref(int32&)
IL_001a: nop
IL_001b: ldloca.s V_2
IL_001d: call void Program::Ref(int32&)
IL_0022: nop
IL_0023: ldloc.1
IL_0024: call void Program::NoRef(int32)
```


load **address** of local (short form) เอาที่อยู่ตัวแปรซึ่งก็คือ V_0 ที่กำหนดไว้ตอนแรก ขึ้น stack ก็คือ เตรียม argument แล้วกระโดดเข้าฟังก์ชั่น Ref จะเห็นว่าอันสุดท้ายเป็น load local เฉยๆ จาก stloc ที่เพิ่งเรียก อันนี้ได้ค่าตัวแปร ซึ่งการ copy ค่าที่ costly เกิดขึ้นตรง ldloc นี้ครับ ถ้าเป็น ldloc**a **ล่ะก็จะเสียแค่ 4 bytes

ข้างใน Ref

```
IL_0000: nop
IL_0001: ldarg.0
IL_0002: dup
IL_0003: ldind.i4
IL_0004: ldc.i4.1
IL_0005: add
IL_0006: stind.i4
IL_0007: ret
```


ก็คือเอาที่อยู่ที่อยู่บน stack ก่อนหน้านี้มาคัดลอกด้วย load argument #0 ขึ้น stack ก่อนแล้ว dup ให้เพิ่มเป็นสองอัน จากนั้น load indirectly (ต้องใช้ address) เพื่อเอาค่าออกมา เมื่อใช้แล้ว address นั้นจะ pop ออกมาแล้ว push ค่าใหม่ไปแทนเลยดังนั้นการ dup ตอนแรกก็จำเป็นต้องทำเผื่อไว้ก่อนถ้าไม่อยากให้มันหายไปเลย อยากทำอะไรต่ออีกอยู่

ต่อมา load constant int 1 แล้วก็เอาสองอันบนสุดบน stack มาบวกกันด้วย add และสุดท้าย store indirectly ใช้เก็บผลบวกลงบน address (ตัวที่ถูกคัดลอกตอนแรก) ได้พอดี เพราะว่าเก็บใส่ address มันก็เลยมีผลออกไปข้างนอกได้

แถมให้ว่าคำสั่ง load constant นี่มีตั้งแต่ 0 1 2 3 4 5 6 7 8 -1

ส่วนข้างใน NoRef

```
IL_0000: nop
IL_0001: ldarg.0
IL_0002: ldc.i4.1
IL_0003: add
IL_0004: starg.s a
IL_0006: ret
```


ที่ต่างออกไปคือไม่ต้อง dup แล้วก็บวกเสร็จ มันเก็บใส่ argument memory เลย ก็คือมีค่าแค่ใน method นี้เท่านั้นครับไม่ได้ออกไปข้างนอก

เมธอด Ref ถ้าสมมติมี ref parameter 2 ตัวมันจะออกมาเป็นแบบนี้ครับ

```
IL_0000: nop
IL_0001: ldarg.0
IL_0002: dup
IL_0003: ldind.i4
IL_0004: ldc.i4.1
IL_0005: add
IL_0006: stind.i4
IL_0007: ldarg.1
IL_0008: dup
IL_0009: ldind.i4
IL_000a: ldc.i4.1
IL_000b: add
IL_000c: stind.i4
IL_000d: ret
```


ใช้ stack model ก็เลยโค้ดเหมือนๆกัน ซ้ำกันได้เลย แต่ละชุดมันทำให้ top stack สะอาดพร้อมจะทำอะไรต่อไปได้ทันที

## struct

ถ้าโปรแกรมเป็นแบบนี้ล่ะ

```
using System;
public class Program
{
public struct Big
{
public int a,b,c,d;
}
public static void Main()
{
Big big = new Big();
UseBig(big);
big.a += 7;
}
private static void UseBig(Big big)
{
big.a += 1;
big.b += 1;
}
}
```


IL :

```
.method public hidebysig static void Main() cil managed
{
//
.maxstack 3
.locals init (valuetype Program/Big V_0)
IL_0000: nop
IL_0001: ldloca.s V_0
IL_0003: initobj Program/Big
IL_0009: ldloc.0
IL_000a: call void Program::UseBig(valuetype Program/Big)
IL_000f: nop
IL_0010: ldloca.s V_0
IL_0012: dup
IL_0013: ldfld int32 Program/Big::a
IL_0018: ldc.i4.7
IL_0019: add
IL_001a: stfld int32 Program/Big::a
IL_001f: ret
} // end of method Program::Main
.method private hidebysig static void UseBig(valuetype Program/Big big) cil managed
{
//
.maxstack 8
IL_0000: nop
IL_0001: ldarga.s big
IL_0003: dup
IL_0004: ldfld int32 Program/Big::a
IL_0009: ldc.i4.1
IL_000a: add
IL_000b: stfld int32 Program/Big::a
IL_0010: ldarga.s big
IL_0012: dup
IL_0013: ldfld int32 Program/Big::b
IL_0018: ldc.i4.1
IL_0019: add
IL_001a: stfld int32 Program/Big::b
IL_001f: ret
} // end of method Program::UseBig
```


เริ่มมาตั้งต้นด้วย address บน stack และใช้ initobj เพื่อ initialize ข้อมูลไว้ที่ address นั้น ตอนนี้ address ที่ทำไว้จะหายไปกับคำสั่ง init แล้ว

ต่อมา จะเห็นว่า stack เป็น value type การใช้ ldloc ก็จะต้องเสียเวลาก๊อปทุกๆค่าใน struct มากองไว้บน stack ค่าที่เพิ่ง init ไว้ที่ตำแหน่ง V_0 ตอนนี้มาอยู่บน stack หมดแล้ว

เข้ามาข้างใน การเอาค่า argument ออกมาบน stack เปลี่ยนเป็น ldarga ซึ่งไม่ได้เอาค่าแต่เอา address แทน ตรงนี้ไม่เหมือนกรณีทั้ง ref และไม่ ref ของตัวแปรปกติที่ใช้ ldarg เฉยๆ

จากนั้นใช้ท่า dup เหมือนเดิม แต่ทีนี้มี load field ใช้เปลี่ยน address เป็นค่า field ของ struct นั่นเองแล้วทับลงไปที่เดิม (รู้ยังว่าทำไมตอนแรกใช้ ldarga) ที่เหลือก็เหมือนเดิม ยกเว้น store field ที่ใช้ address ที่โดน dup เก็บไว้ในตอนแรก

เนื่องจาก address นี้เป็น address ของ argument variable ดังนั้นผลจะไม่ส่งออกไปข้างนอกครับ

```
IL_0000: nop
IL_0001: ldloca.s V_0
IL_0003: initobj Program/Big
IL_0009: ldloc.0
IL_000a: call void Program::UseBig(valuetype Program/Big)
IL_000f: nop
IL_0010: ldloca.s V_0
IL_0012: dup
IL_0013: ldfld int32 Program/Big::a
IL_0018: ldc.i4.7
IL_0019: add
IL_001a: stfld int32 Program/Big::a
IL_001f: ret
```


หลังกลับมาแล้ว เราทำ address ขึ้นมาใหม่เหมือนตอนแรกพร้อมกับ dup เพิ่มอีกอัน เพราะต่อไปจะใช้ add แล้วก็ stfld ก็ใช้ 2 address พอดี ตรงนี้ผมใช้ +7 เพื่อให้เห็นว่า +constant มีคำสั่งเฉพาะทางตั้งแต่เลข 0 ถึง 8 แล้วก็ -1

## ref struct

ทีนี้ก็เลยสงสัยว่าถ้าเข้ามาเป็น ref struct ล่ะ (เปลี่ยนค่าเห็นผลจริงข้างนอก)

```
using System;
public class Program
{
public struct Big
{
public int a,b,c,d;
}
public static void Main()
{
Big big = new Big();
UseBig(ref big);
big.a += 7;
}
private static void UseBig(ref Big big)
{
big.a += 1;
big.b += 1;
}
}
```


IL :

```
.method public hidebysig static void Main() cil managed
{
//
.maxstack 3
.locals init (valuetype Program/Big V_0)
IL_0000: nop
IL_0001: ldloca.s V_0
IL_0003: initobj Program/Big
IL_0009: ldloca.s V_0
IL_000b: call void Program::UseBig(valuetype Program/Big&)
IL_0010: nop
IL_0011: ldloca.s V_0
IL_0013: dup
IL_0014: ldfld int32 Program/Big::a
IL_0019: ldc.i4.7
IL_001a: add
IL_001b: stfld int32 Program/Big::a
IL_0020: ret
} // end of method Program::Main
.method private hidebysig static void UseBig(valuetype Program/Big& big) cil managed
{
//
.maxstack 8
IL_0000: nop
IL_0001: ldarg.0
IL_0002: dup
IL_0003: ldfld int32 Program/Big::a
IL_0008: ldc.i4.1
IL_0009: add
IL_000a: stfld int32 Program/Big::a
IL_000f: ldarg.0
IL_0010: dup
IL_0011: ldfld int32 Program/Big::b
IL_0016: ldc.i4.1
IL_0017: add
IL_0018: stfld int32 Program/Big::b
IL_001d: ret
} // end of method Program::UseBig
```


สังเกตุว่า

- ที่ Main มีเปลี่ยนจาก load local เฉยๆเป็น load local address
- ใน UseBig เมื่อได้มาเป็น address แล้ว ตรงแรกสุดเป็น load argument เฉยๆไม่ใช้ load argument address (ใช้เวอร์ชั่นโหลดค่า แต่ได้ address เพราะส่งเข้ามาเป็น address)

ที่มันกลับกัน จะส่งผลให้ข้างในเริ่มด้วย top stack ที่เป็น address ของตัวนอกแทน (ตัวอย่างที่แล้ว top stack เป็น address ของ argument variable ที่โปรแกรมเตรียมไว้ให้ใหม่) ทำให้ที่เหลือที่เหมือนเดิม ไปกระทบข้างนอก แทนที่จะกระทบ argument space ที่โปรแกรมเตรียมไว้ให้เหมือนกรณีไม่ ref

## out

```
using System;
public class Program
{
public struct Big
{
public int a, b, c, d;
}
public static void Main()
{
Big bigOut;
BigOut(out bigOut);
bigOut.a += 7;
}
private static void BigOut(out Big bigOut)
{
bigOut = new Big();
bigOut.a = 3;
}
}
```


IL :

```
.method public hidebysig static void Main() cil managed
{
//
.maxstack 3
.locals init (valuetype Program/Big V_0)
IL_0000: nop
IL_0001: ldloca.s V_0
IL_0003: call void Program::BigOut(valuetype Program/Big&)
IL_0008: nop
IL_0009: ldloca.s V_0
IL_000b: dup
IL_000c: ldfld int32 Program/Big::a
IL_0011: ldc.i4.7
IL_0012: add
IL_0013: stfld int32 Program/Big::a
IL_0018: ret
} // end of method Program::Main
.method private hidebysig static void BigOut([out] valuetype Program/Big& bigOut) cil managed
{
//
.maxstack 8
IL_0000: nop
IL_0001: ldarg.0
IL_0002: initobj Program/Big
IL_0008: ldarg.0
IL_0009: ldc.i4.3
IL_000a: stfld int32 Program/Big::a
IL_000f: ret
} // end of method Program::BigOut
```


จริงๆก็เป็นแค่ variation ของท่า ref คือโหลด address เตรียมไว้แล้วเข้าข้างใน แค่ว่า initobj อยู่ข้างในแทนและเก็บของใส่ address นั้น ทำให้ผลกระทบออกมาข้างนอก ( out ออกมา)

## ถ้าเป็น in ของ C#7.2 ล่ะ

ตัวดู IL ที่ใช้อยู่มันใช้ syntax 7.2 ไม่ได้เลยยังไม่แน่ใจ แต่เดาว่ามันน่าจะออกมาเหมือน ref ที่ฝั่ง caller (ใช้ ldloca เอาแค่ address มาวางเตรียมไว้) แล้วในฝั่งฟังก์ชั่นก็ใช้ ldfld เอาค่าจาก address นั้นมาใช้ ซึ่งจุดนี้ถ้า stfld ก็จะกระทบข้างนอกเลยแหละ แต่เป็นหน้าที่ที่ทาง compiler ต้องเช็คได้ว่าข้างในห้ามแก้ค่า และจะไม่มี stfld เกิดขึ้น

## ประโยชน์ใน Unity

ทั้งหมดนี้รู้ไว้เพื่อเตรียมตัวสำหรับ in ของ C# 7.2 ที่ Unity สัญญาว่าจะเอามาให้เล่นเร็วๆนี้ครับ แล้วเกมจะได้เร็วขึ้น โปรแกรมบัคน้อยลง (เห็นทวีตว่ากำลัง merge ความสามารถใช้ Roslyn แล้วใน 2018.2 แสดงว่าน่าจะทำเสร็จแล้ว)

ตัวแปรสำคัญที่จะเป็นเป้าหมายของ ref กับ in ใน Unity คือ Vector3 (3x float) กับ Touch (~14x 4bytes !) ถ้าส่งเข้าแบบก๊อปค่าใน main loop แน่นๆนี่ บานแน่นอนครับ ใครอยาก optimize โดยใช้ ref แต่กลัวข้างในแก้ค่า in นี่ godsend มากเลยครับ

## ส่งท้าย

ยังไงเราก็ไม่รู้ performance ชัดๆของแต่ละ opcode รวมทั้ง optimization ที่ทำได้ต่อจาก IL นี้ด้วย (ยังไม่ถึงขั้น machine code) เช่นอาจมีการ inlining เกิดขึ้นก็ได้ ดังนั้นรู้ไว้เฉยๆแต่อย่าไปกังวลมากครับ

แล้วก็ รายการคำสั่ง CIL เผื่อใครอยากรู้อยากเห็น

**List of CIL instructions - Wikipedia***This is a list of the instructions in the instruction set of the Common Intermediate Language bytecode.*[en.wikipedia.org](https://en.wikipedia.org/wiki/List_of_CIL_instructions)