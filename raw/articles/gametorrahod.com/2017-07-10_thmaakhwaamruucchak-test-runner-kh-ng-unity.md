---
title: ทำความรู้จัก Test Runner ของ Unity
url: https://gametorrahod.com/unity-test-runner-thai/
author: Sirawat Pitaksarit
published: '2017-07-10'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

รู้หรือไม่ว่า Test Runner (ร่างสุดยอด) เป็นฟีเจอร์**ใหม่**ของ Unity 5.6? หลายๆคนอาจจะคุ้นๆว่ามันมีมานานแล้วไม่ใช่เหรอ คือก่อนหน้านี้มันเคยมั่วมานานมาก

## พาเริ่มต้นเขียน test ใน Unity 5.6+ ตั้งแต่ต้น พร้อมพูดไปด้วย

กำลังอัดวิดิโออยู่ ถ้าไม่ขี้เกียจเดี๋ยวคงมา

## ประวัติศาสตร์

ตอนแรก ต้องโหลด Unity Test Tools จาก Asset Store แล้วทำ Unit Test ได้ (รันจาก editor แล้วผลออกมาเลย) แล้วก็ทำ integration test ได้ โดยต้องสร้าง scene พิเศษขึ้นมาเอง แล้วเอาสคริปต์กำกับไปแปะ แล้วพอรัน มันจะค่อยๆทำตามโดยที่ห้ามทำอะไรกับ GameObject ที่มันกำกับเทสอยู่ไม่งั้นเทสจะหยุด 555

**Unity-Technologies / UnityTestTools***This is the repository for the Unity Test Tools project.*[bitbucket.org](https://bitbucket.org/Unity-Technologies/unitytesttools/)

**Unity-Technologies / UnityTestTools / wiki / IntegrationTestsRunner - Bitbucket***A Test Object is a GameObject on the scene that has TestComponent attached to it. Everything under the Test Object in…*[bitbucket.org](https://bitbucket.org/Unity-Technologies/unitytesttools/wiki/IntegrationTestsRunner)

หน้าตา integration test ของเดิมประมาณนี้

![](../../assets/f28e0730d5c2fd5d.png)

ปัญหาที่ตามมาก็คือถ้าเขียน load scene ไว้ในเทสโดยใช้ฟังก์ชั่นเดียวกับในเกมอาจจะทำให้ของหายหมดเพราะดันใช้ LoadSceneMode.Single ต้องมานั่งแยกเวอร์ชั่นเทสให้มันเป็น additive ด้วยเหตุผลที่อยากจะรักษาของเทสไว้ ยากกว่าตอนที่จะเดินทางจาก scene ที่ว่าไป scene ถัดไป ในเกมปกติกะว่าจะให้ .Single ให้มันล้างบางให้สะอาดไง ทีนี้ใช้ .Single ก็เทสหาย จะใช้ .Additive ก็เหลือ scene เก่า ทำให้ต้องมานั่ง .Unload ทุก scene ยกเว้น integration scene เอาเองถึงจะได้ฟังก์ชั่นเหมือน .Single (ผมมีเมธอด .UnloadExcept เขียนไว้เพื่อทำ integration test โดยเฉพาะ)

ต่อจากนั้นไม่นานใน Unity 5. เท่าไหร่ไม่รู้ มันก็มีเมนู Test Runner ขึ้นมาตรงนี้

![](../../assets/3cf7c7e3c07b12d3.png)

แล้ว unit test ก็โดนเอาออกจาก Unity Test Tools แต่ถ้าอยากเทส Integration ก็ยังต้องเก็บ Unity Test Tools ไว้อยู่ กลายเป็นเกมมีระบบเทส 2 อันแยกกัน

## ร่างสุดยอด

ใน Unity 5.6 ในที่สุด integration test ก็ไปอยู่ใน Test Runner ในชื่อ Play mode test ในที่สุดก็เอา Unity Test Tools ออกจากโปรเจคได้ แต่การเขียนเทสก็เปลี่ยนไปด้วย ไปอ่านเอาเองที่

**Unity - Manual: Unity Test Runner***The Unity Manual helps you learn and use the Unity engine. With the Unity engine you can create 2D and 3D games, apps…*[docs.unity3d.com](https://docs.unity3d.com/Manual/testing-editortestsrunner.html)

หลักๆก็คือไม่ต้องมี scene เฉพาะเวลาจะทำ play mode test แล้ว มันเสกให้เราเอง เมธอดไหนอยากให้เป็นเทสก็แค่ใส่ [Test] (แบบเดิม ใช้ได้กับ unit/edit mode test) กับ [UnityTest] (แบบใหม่ ใช้ yield ได้ ใช้กับ integration/play mode test)

ใครยังไม่เข้าใจเรื่อง yield กับ IEnumerator ลองดูตัวอย่างนี้ได้ครับ (รันเทสแล้วจะ log 1 2 3 4 เรียงกันทั้งคู่ แล้วเทสถึง pass)

![](../../assets/c38db0e46abf231f.png)

![](../../assets/d9be76c4683a093f.png)

## ทดสอบ Attribute เดิมของ NUnit

![](../../assets/27fad8ebc06d9a68.png)

ผลก็คือยังใช้ได้เหมือนเดิม

![](../../assets/2fb92b847345f50e.png)

## ทดสอบ Attribute ใหม่

เห็นในนี้ [https://docs.unity3d.com/Manual/testing-editortestsrunner.html](https://docs.unity3d.com/Manual/testing-editortestsrunner.html) มีแนะนำให้ implement interface IPrebuildSetup

![](../../assets/966ebaec5a20c710.png)

![](../../assets/eb335db71480eed7.png)

ผลคือ ทำไมมันไม่เห็นรันเลย

![](../../assets/9ca72eec784148da.png)

ลองแปะ attribute เพิ่มที่เขาบอกว่าไม่ต้องแปะก็ได้

![](../../assets/7d50271abc43e9fc.png)

มันก็ยังไม่รันอยู่ดี

![](../../assets/06452b5d951a1b53.png)

สรุปคือใช้อันเดิมไปนั่นแหละ

## Integration Test ต้องแก้อะไรมั่ง

ตอนแรกมันทำสไตล์เอา MonoBehaviour ไปแปะ game object ใน integration scene แล้วเทสก็จะเริ่มจาก Start ตามปกติ

คราวนี้มันไม่มี scene ให้แปะแล้ว และเทสจะเริ่มจากเมธอดที่ใส่ [UnityTest] ไว้แทน ก็แค่ลบ : MonoBehaviour inheritance ออกไปแล้วก็เอา [UnityTest] ไปแปะไว้ที่ชอบๆ ออ แล้วก็ไฟล์นี้ห้ามเอาไว้ในโฟลเดอร์ Editor ไม่งั้นมันจะไปโผล่ใน edit mode test

จริงๆถ้าไม่ลืมเอาออกจะเจอแบบนี้ เพราะตัวเทสจะพยายาม new คลาสเทสของเรา

![](../../assets/2cb69f65b685cfe0.png)

เวลาเริ่มเทส Scene เราจะกลายเป็นแบบนี้ครับ

![](../../assets/eae15802ca516836.png)

อันนั้นคือ Scene ใหม่ที่ Unity เสกมาให้ พร้อม game object ปริศนา 1 อัน ซึ่งเป็นตัวที่รัน coroutine เมธอดที่เราแปะ [UnityTest] ไว้ ดังนั้นระวังด้วยถ้าเทสเรามี LoadScene แบบล้างบางเมื่อไหร่ อันนี้หายไป ก็จะกลายเป็น coroutine หยุด 55555

![](../../assets/dc4e982bfef3ddae.png)

แบบภาพนี้ Debug.Log("2") จะไม่รันเพราะตัวรัน coroutine ระเบิดเละไปแล้ว และ Assert ก็ไปไม่ถึงด้วย กลายเป็น load scene เสร็จก็ค้างอยู่แค่นั้น จบ (แถมถ้ากดออก play mode ตอนนี้ scene ขยะจะคาอยู่ใน project เราให้เราต้องเก็บกวาดเอง)

ดังนั้นเรามีวิธีโกงความตายโดยการคุ้ยหาอีตัว Test Runner นั่นมาเข้า DontDestroyOnLoad ซึ่งใช้ได้แม้จะไม่อยู่ใน MonoBehaviour ก็ตาม ท่าก็ประมาณนี้

![](../../assets/bfc33d9f7b0a7d99.png)

เพียงเท่านี้ไอ้ตัวนั้นมันก็จะถึก ไม่โดนล้างบาง

## ท่า NUnit ที่ใช้ได้

[SetUp] กับ [TearDown] ใช้ได้เหมือนเดิม อ้อ แล้วก็ ใช้หลายอันก็ได้ครับโดยลำดับคือ จากบนลงล่าง และจาก class แม่มาลูก (ดังนั้นทำ [Setup] ที่ใช้ด้วยกันหลายๆเทสไว้เป็นคลาสแม่ อะไรงี้ก็ได้)

![](../../assets/45f9cee3f67908fb.png)

![](../../assets/f4dbf6ee65aa4db7.png)

[TestCaseData] ใช้ได้กับ [Test](ใช้กำหนด parameterized test จากคลังข้อมูลแยก)

Assert สไตล์ NUnit 3.0 (Constraint model) ใช้ได้ ( Assert.That(____ , Is.GreaterOrEqual(____)); ) อันเก่าก็ยังใช้ได้ ( Assert.GreaterOrEqual(___, __); )

![](../../assets/4f71fd839780a8a3.png)

![](../../assets/dede35652cfe4115.png)

ถ้าลองใช้กับ [UnityTest] จะเกิดเออเร่อปริศนา

![](../../assets/2ade465666085ca9.png)

![](../../assets/52b6b61588d5be20.png)

ทาง Unity บอกว่าถ้าอยากทำ parameterize กับ [UnityTest] ตอนนี้ต้องใช้สไตล์ [ValueSource] อย่างเดียว ท่าในการทำคือแบบนี้

![](../../assets/aa263f15b87847dc.png)

เฮ่เฮ้

![](../../assets/cd03845da38283fc.png)

จำไว้ด้วยว่าถ้าใช้ ValueSource หลายๆ parameter แล้วมันจะไล่จับคู่ให้ทุกกรณีเลยน่ะครับ ออแล้วก็ source ข้อมูลต้องเป็น static variable/method/property น่ะ แต่จะ private ก็ได้ (แต่เมธอดเทสต้องไม่ private น่ะ)

[TestFixtureData] ใช้**ไม่ได้ **(ให้ NUnit เสก test instance เพิ่มอีกหลายชุดโดยให้แต่ละชุดมี constructor ต่างๆกันได้ แปะใส่คลาส ไม่ใช่ใส่เทส)

![](../../assets/003048bb1784a845.png)

![](../../assets/e450eae6a7874463.png)

## MonoBehaviourTest

เขามีคลาสวิเศษ MonoBehaviourTest<T> มาให้ ซึ่งเขาว่าถ้า new แล้ว yield return ใส่มัน มันจะ instantiate ตัวคลาส T ให้แล้วก็รัน Awake Start Update ประหนึ่งเป็นของชิ้นนึงจริงๆ แล้วจะ yield รอถึงเมื่อไหร่ คลาส T ของเราที่ว่าต้อง implement IMonoBehaviourTest ด้วย จากนั้นก็ implement property bool IsTestFinished เอาไว้บอกมัน ทีนี้ข้างใน mono ของเรานี้ก็สามารถ StartCoroutine อะไรงี้ได้ด้วย หรือเทสอะไรอื่นๆตามชอบได้ ปกติ MonoBehavior นี้ new ไม่ได้ คิดว่านี่คงมีประโยชน์พอควรสำหรับเทสแค่ MonoBehavior อันเดียวเดี่ยวๆว่าทำงานถูกมั้ย

```
yield return new MonoBehaviourTest<MyMonoBehaviourTest>();
public class MyMonoBehaviourTest : MonoBehaviour, IMonoBehaviourTest {
private int frameCount;
public bool IsTestFinished { get { return frameCount > 10; } }
void Update() { frameCount++; }
}
```


## ปรับแต่งรายการ Test Case

ถ้าเป็น [Test] เฉยๆ เท่าที่ลองสามารถใส่ Descriptionใน attribute ได้ มันจะไปขึ้นเล็กๆตรง console ของ Test Runner แล้วก็ถ้าใส่ TestName จะเปลี่ยนชื่อได้ จากที่แต่ก่อนอิงตามชื่อ method ส่วนอันอื่นๆอย่าง Author หรือ Category ไม่มีผลอะไรกับ Unity

![](../../assets/b9ac4e240aa5a7af.png)

![](../../assets/e176fe59b2f06193.png)

![](../../assets/d737f63d572bedda.png)

![](../../assets/a8c6a618fde6c658.png)

แต่ถ้าเป็น [UnityTest] อย่างว่า ใช้ได้แค่ [ValueSource] ก็เลยเปลี่ยนชื่อไม่ได้ ถ้า args เป็นอะไรที่ดูง่ายเช่น string หรือ int ก็โอเคอยู่ แต่ถ้าเป็น object อาจจะดูไม่ค่อยดี เพราะกลายเป็นเหมือนๆกันหมดเลย

แต่เราสามารถ override ToString ของ class เราเพื่อขุดเอาข้อมูลของคลาสมาแสดง ก็พอแก้ขัดได้ครับ

![](../../assets/7935cd1e9e9bf06c.png)

![](../../assets/80e92f00ae0df882.png)

![](../../assets/163fca7e18fbe107.png)

![](../../assets/92897c1ce24b776c.png)

## รันในเครื่องจริงได้ด้วยนะ!

จะเห็นว่ามีปุ่ม Run all in player ที่มุมขวาบน กดปุ้บเครื่องมือถือที่ต่อกับคอมอยู่ ก็จะโดน Unity โยน Scene เสกใหม่ให้ไปรันทันที เหมาะจะเทสอะไรที่มันเวิคบนเครื่องจริงเท่านั้น เช่น Firebase หรือ Ads อะไรงี้ครับ

## แต่มัน Run all บางอันเออเร่อบนเครื่องด้วย

ใช้ attribute UnityPlatform แบบนี้แล้วจะยกเว้นได้ครับ เช่น

![](../../assets/80b2011f23162e00.png)

![](../../assets/89382a2574422cce.png)

แบบนี้จะกลายเป็นรันบนเครื่องคอมไม่ได้ เทสกลายเป็น skip ถ้าจะให้มันไปรันบนมือถือแล้ว skip ก็เปลี่ยนเป็น exclude หรือว่าจะใส่ RuntimePlatform เป็นของคอมๆอย่างเดียวก็ได้ หรือถ้าใครขี้เกียจใส่ของใน attribute แบบนั้นก็ทำ subclass มาให้ความสะดวกตัวเองแบบนี้ก็ได้ครับ (เพราะ attribute เป็น compile time เราจะใช้ตัวแปรไม่ได้นะ)

![](../../assets/89ec9fb8f06da092.png)

แล้วก็แปะใส่ TestFixture (หัวคลาส) ได้เลยจะได้คลุมไปให้หมดทุกเทส

หรือถ้าอยากยกเลิกทุกที่ชั่วคราว ใช้ [Ignore("reason")] ได้ครับซึ่ง ignore แค่ TestCase หรือทั้ง Fixture เลยก็ได้เหมือนกัน

## สิ่งที่จะเพิ่มในอนาคต

มีลุงคนนึงจาก Unity มาบอกว่าเดี๋ยวคงจะเพิ่มระบบ integration test แบบตาม scene กลับมาทีหลัง ตอนนี้ก็เรียกคำสั่งโหลด scene เองไปก่อน [https://forum.unity3d.com/threads/integration-testing-support-in-5-6.460745/#post-2991665](https://forum.unity3d.com/threads/integration-testing-support-in-5-6.460745/#post-2991665)

## อยากเทพต้องไปเรียน NUnit

ที่นี่เลย

**nunit/docs***docs - Documentation for all active NUnit projects*[github.com](https://github.com/nunit/docs/wiki/NUnit-Documentation)