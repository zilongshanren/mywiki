---
title: รีวิวปัญหา 1,000,000$ ที่ว่ากันว่าพิสูจน์ได้เมื่อวานนี้ “Riemann hypothesis”
url: https://gametorrahod.com/riemann-hypothesis/
author: Sirawat Pitaksarit
published: '2018-09-24'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/fa7e7c00618c59af.png)

เรื่องน่าตื่นเต้นที่เกิดขึ้นช่วงนี้ ไม่ใช่[ไอติมไผ่ทอง](https://www.khaosod.co.th/special-stories/news_1604026)หรือ[เจ้าหญิงคุปป้า](https://dic.pixiv.net/a/%E3%82%AF%E3%83%83%E3%83%91%E5%A7%AB)แต่ว่าในงาน [HLF18](https://www.heidelberg-laureate-forum.org/) มี speaker ท่านหนึ่ง Sir Michal Francis Atiyah ขึ้นมาพิสูจน์ปัญหา Riemann hypothesis แล้วครับ! ซึ่งเป็น 1 ใน 6 Millennium Prize Problems ที่เหลืออยู่ครับ

**Millennium Prize Problems - Wikipedia***The Millennium Prize Problems are seven problems in mathematics that were stated by the Clay Mathematics Institute on…*en.wikipedia.org

เป็นรายการปัญหาสำคัญทางคณิตศาสตร์ที่คนแก้ได้จะได้รางวัล 1 ล้าน $ เลยทีเดียว ปัญหาเดียวที่เคยแก้ได้นั้นตั้งแต่ปี 2013 ครับ ไหนๆก็มีเรื่องสำคัญขนาดนี้ในช่วงชีวิตเราก็เลยลองกูเกิลรัวๆดู รู้มาเท่านี้เลยมาสรุปให้ฟัง

## Euler zeta function

แนะนำ

**What is the Riemann Hypothesis? " Heidelberg Laureate Forum " SciLogs - Wissenschaftsblogs***This year at the HLF there are multiple sessions in the program concerning the Riemann Hypothesis, including a talk…*scilogs.spektrum.de

อ่านแล้วเลยจะเล่าให้ฟังลวกๆสรุปจากเว็บนั้น

![](../../assets/03474694d56c885d.png)

ตัวนั้นอ่านว่า zeta ถ้ามีฟังก์ชั่นนี้แบบเอา s อะไรก็ได้ แต่ sum ไปเรื่อยๆจน n = infinite นี่ ก็พอจะนึกภาพได้ว่ามันต้องน้อยลงเรื่อยๆจนแทบไม่ขยับเข้าซักจุดใช่มั้ยครับ แต่ว่าฟังก์ชั่นนี้ **define ไว้แค่ s > 1** แล้วก็ converge แน่ๆ (ไม่ infinite)

ถ้าดูเผินๆก็คงจะออกมาเป็นค่าๆนึงที่ 1 กว่าๆใช่มั้ยครับเพราะตัวแรกก็ 1 ละ แล้วก็ + น้อยลงเรื่อยๆ อันนี้จะเรียกว่า Euler zeta function เพราะ Euler ศึกษาส่วนที่ s เป็นจำนวนจริงก่อนที่ Riemann จะมาทำต่อ

### Highlight !

- s = 2 : ถ้ากดเครื่องคิดเลขรัวๆก็จะได้ 1.644934 แต่ก็แค่ค่าประมาณ ต่อมา Euler บอกว่าเลขนั่นคือ π²/6
[https://en.wikipedia.org/wiki/Basel_problem](https://en.wikipedia.org/wiki/Basel_problem)/[https://www.youtube.com/watch?v=d-o3eB9sfls](https://www.youtube.com/watch?v=d-o3eB9sfls) - s = 3 : ได้เป็นเลข Apéry’s constant ที่มีค่าอยู่จริงทางฟิสิกส์ และพิสูจน์ได้ว่าเป็น irrational
[https://en.wikipedia.org/wiki/Ap%C3%A9ry%27s_constant](https://en.wikipedia.org/wiki/Ap%C3%A9ry%27s_constant) - เขาว่า upperbound คือ 2

ถ้า s = 1 ล่ะ อันนี้เรียกว่า harmonic series เหมือจะ converge (1 + 0.5 + 0.25 + …) แต่จริงๆมัน diverge ไปสู่ infinite น่ะครับ.. จำได้ว่าเป็นโจทย์หลอกให้เสียคะแนนสมัย ม. ปลาย อะไรไม่รู้แหละ จำๆไปตอบพิสูจน์ไม่สน 555

**Why does the series $\sum_{n=1}^\infty\frac1n$ not converge?***Can someone give a simple explanation as to why the harmonic series $$\sum_{n=1}^\infty\frac1n=\frac 1 1 + \frac 12 +…*math.stackexchange.com

ถ้า s < 1 ล่ะ ก็คิดแบบปกติจะได้ infinite ยกตัวอย่างเช่นถ้าเป็น -1 ส่วนก็จะกลับด้านขึ้นมา ได้ 1 + 2 + 3 + 4 + … **คิดแบบปกติ**ได้ infinite ก็คือ diverge ออกไป ถ้า -3 อะไรงี้ยิ่ง diverge เร็วขึ้น แต่ จะบอกว่า “ได้ infinite” ก็ไม่ค่อยถูกเพราะมันไม่มีจริงครับ

## Analytic continuation สู่ Riemann zeta function

ถ้าใช้เทคนิค [analytic continuation](https://en.wikipedia.org/wiki/Analytic_continuation) ที่พยายามอธิบายฟังก์ชั่นนอกขอบเขต s > 1 ออกไปล่ะ (s ≤ 1)

อันนี้เป็นคณิตสาย complex analysis ที่เราสามารถใช้จำนวนเชิงซ้อนมาอธิบายคณิตศาสตร์ที่เร้นลับได้ครับ (เช่นบริเวณที่เคยได้ infinite ในระบบจำนวนจริง) เขาว่าสมัย Euler ยังไม่มีให้ใช้งาน จำนวนเชิงซ้อนก็คือที่ +i ส่วนจินตภาพ (imaginary number) เข้ามา กลายเป็นคณิต 2 มิติ มีกฏใหม่ๆของมันเอง

ผมก็ไม่เคยเรียน analytic continuation ด้วยแหละเพิ่งแค่ไปอ่านๆ wiki มา แต่พอดีฟังก์ชั่น infinite summation ที่ว่า**เป็น analytic function** สมบัตินี้ อนุญาติให้เราสามารถทำ complex analysis ได้ เปิดทางให้เราต่อได้ครับ

เดิมเราอยู่บนเส้นจำนวนเส้นตรงเส้นเดียว ทีนี้เราเพิ่มมิติขึ้นมาอีกอันจะเกิดอะไรขึ้น (s = a + bi) ส่วนที่เคย valid เราจะพยายามทำให้ valid เหมือนเดิมไหนๆจำนวนจริงก็เป็น subset ของจำนวนเชิงซ้อนนะครับ (a + 0i)

เรียกฟังก์ชั่นใหม่ที่ analyze ต่อเนื่องมานี้ว่า **Riemann zeta function**

- ยัง converge อยู่เหมือนเดิม ถ้าใส่ s อะไรก็ได้ที่ส่วนจำนวนจริง > 1 (จะ +bi อะไรก็ได้ ซึ่งพิสูจน์แล้ว)
- ทีนี้ในส่วนที่เคย diverge ทั้งหมดกลายเป็น well-defined แล้ว (ไม่ infinite แล้ว) ด้วยพลังของ complex number
- มีบางจุดที่ทำให้ฟังก์ชั่นนี้ได้ 0 เกิดขึ้น
**<- ปัญหาเงินล้าน : จุดไหน?**

## พลังของยกกำลัง i

![](../../assets/03474694d56c885d.png)

ถามว่า! complex number มีพลังเปลี่ยน infinite เป็น well-defined งี้ได้ไง ลองนึกดูว่าถ้า 1/n^s แล้ว s เป็น (-1+4i) ติดลบงี้แต่ก่อนต้อง diverge สู่ infinity ใช่มั้ยครับ แต่มี i แถมมาด้วยแล้วอะไรๆก็เปลี่ยนไป

เราอาจจะจำได้ว่า i² = -1 เพราะว่า i = sqrt(-1)

แต่นี่มันเลขแล้วยกกำลัง**ด้วย** i แล้วมันคือบ้าอะไร ตรงนี้ต้องขอบคุณ Euler อีก

![](../../assets/697e30a83ca956b8.png)

**Euler's formula - Wikipedia***where e is the base of the natural logarithm, i is the imaginary unit, and cos and sin are the trigonometric functions…*en.wikipedia.org

สมการเทพที่ Euler หาเจอมานี้จำได้ว่าเคยใช้สอบงงๆแล้วลืมๆมันไป จะเห็นว่าในสูตรมียกกำลัง i แล้วอีกด้าน i ร่วงลงมาเฉยเลย แถมมี cos sin มาเกี่ยวแล้วดันเกี่ยวกับ π ได้อีก คิดมาได้ไงก็ไม่ทราบแต่เอาเป็นว่าไหนๆก็เกี่ยวกับ π แล้ว คิดซะว่ายกกำลัง i แล้ว**มันจะหมุนๆ **ไปก่อนก็แล้วกัน

(สำหรับคนที่สนใจในไอ้ยกกำลัง i นี้จริงๆ)

**Intuitive Understanding Of Euler's Formula***Euler's identity seems baffling: It emerges from a more general formula: Yowza -- we're relating an imaginary exponent…*betterexplained.com

ต่อไปจะขอยืมภาพมาจากคุณ 3Blue1Brown จากวิดิโอนี้ ซึ่งเป็นวิดิโอที่แนะนำให้ดูมากๆครับ

![](../../assets/d4a8f170eef145ab.png)

![](../../assets/ed8364ffff1813ea.png)

หมุนๆที่ว่าคือยังไง ลองดูภาพซ้ายที่แสดงส่วน valid (s > 1) มาเพิ่มมิติให้ไปบนล่างได้ (ก็คือ i) แล้วภาพขวาเป็นผล convergence ที่ได้ จะเห็นว่าเส้นตั้งสีแดงผลออกมากลายเป็นกลมๆ ก็คือหนึ่งในพลังของยกกำลัง i ที่ว่านี้ครับ

ถ้า complex analyze ต่อเนื่องออกไปก่อนเขต s > 1 ล่ะ

![](../../assets/05a5edc3c7face02.png)

จะเห็นว่าที่ 0,0 มีเส้นโค้งมาโดนด้วยแล้วทีนี้ (ด้วยพลังของ i, ว่าได้ว่าเป็นพลังของ complex analysis) อันนี้สำคัญแต่เอาไว้ก่อน

## ที่มาของสมการดัง 1 + 2+ 3 + … = -1/12

เห็นเพจเรียกไลค์หลายๆเพจแค่เอาภาพโจทย์ operator precedence มาล่อก็เกิดเป็น civil war ระหว่างฝ่ายซ้ายไปขวากับฝ่ายคูณก่อนบวกแล้ว ก็เลยคิดเล่นๆว่าถ้าเอาคำถาม 1 + 2 + 3 + … ได้เท่าไหร่ จะมีคนตอบอะไรบ้าง 555

โด่งดังมาจากวิดิโอนี้ ซึ่งไม่แนะนำให้ดูเท่าไหร่เพราะค่อนข้าง clickbait-y แล้วก็เหมือนโชว์มายากลว่าจะจับได้รึเปล่า มัวแต่ลีลา หมั่นไส้ 555

คือ 1 + 2 + 3 +4 + … มันได้ infinite ในระบบจำนวนจริงแหละ แต่ถ้า derive แบบที่ว่าไปจะทำให้ divergent series กลับกลายเป็นมีค่าคงที่ขึ้นมาได้ เรียกว่า “zeta function regularization” (ในคลิปเหมือนพยายามไม่พูดถึง)

**Zeta function regularization - Wikipedia***In mathematics and theoretical physics, zeta function regularization is a type of regularization or summability method…*en.wikipedia.org

**1 + 2 + 3 + 4 + ⋯ - Wikipedia***Among the classical divergent series, 1 + 2 + 3 + 4 + ⋯ is relatively difficult to manipulate into a finite value. Many…*en.wikipedia.org

ถ้าดูภาพนี้ ถ้าใช้ s = -1 แล้วมันจะโค้งไปหา -1/12 จริงๆ ตารางก่อนโค้งที่เห็นให้คิดซะว่าเป็น a+bi ใดๆ bi คือแกน y ครับ

![](../../assets/d1fbe12eeffd0d1c.gif)

นอกจากนี้ยังมี 1 + 1 + 1 + … = -1/2 (ใช้ s = 0) กับ 1+ 2 + 4 + 8 + … = -1 อีก 555

**1 + 1 + 1 + 1 + ⋯ - Wikipedia***In a short period of less than a year, two distinguished physicists, A. Slavnov and F. Yndurain, gave seminars in…*en.wikipedia.org

**1 + 2 + 4 + 8 + ⋯ - Wikipedia***In mathematics, is the infinite series whose terms are the successive powers of two. As a geometric series, it is…*en.wikipedia.org

ถ้าทางคณิต complex number เห็นเขาว่า ไอ้การโค้งๆนี้ มันเป็นการเอา infinite ด้านบวกกับลบมาหักล้างกันอย่างชาญฉลาดทางอ้อมครับมันเลยออกมาจับต้องได้

นึกง่ายๆก็เส้นแนวนอนตรงๆที่เคยไปถึงไหนไม่รู้กลายเป็นมาอยู่ใกล้แค่เอื้อม …แต่จะว่าไปคำว่า “วงกลม” นี่ก็มีความ infinite ในตัวของมันอยู่ก็คือวนไปได้เรื่อยๆนั่นเอง โอ้ว! จะเห็นว่าไปๆมาๆสมการ euler ก็เริ่มดูสมเหตุสมผลแล้ว วงกลม, i, e, sin, cos, infinite… เหมือนจะเกี่ยวกันหมดจนได้

เรื่องการโม้เลขจาก infinite series นี่ก็ทำให้นึกถึง series ที่เป็น conditional convergence คือแค่เรียงๆใหม่ก็ได้ค่าไม่เหมือนเดิมแล้ว

**Conditional convergence - Wikipedia***Bernhard Riemann proved that a conditionally convergent series of real numbers may be rearranged to converge to any…*en.wikipedia.org

## เหมือนเลขเสกมา แต่ไม่ไร้สาระ

จะว่าผลที่ derive มาจาก zeta function regularization เป็นเลขขี้โม้ก็อาจจะได้ แต่ทางฟิสิกส์ดันมีบางอย่างที่เหมือนจะตรง เช่นพลังงาน quantum ระหว่างแผ่นในสูญญากาศที่คิดตามหลัก quantum แล้วได้ infinite แต่พลังงานไม่จำกัดถ้ามีจริงคงจะดี เขาเลยลองวัดดูจริงๆแล้วผลออกมาเหมือน Riemann zeta function ที่แทนค่า s = -3 เฉยเลย แสดงว่าอาจจะไม่ใช่เรื่องเล่นๆ

**Infinity or -1/12?***Recently a very strange result has been making the rounds. It says that when you add up all the natural numbers…*plus.maths.org

**Casimir effect - Wikipedia***The Casimir effect can be understood by the idea that the presence of conducting metals and dielectrics alters the…*en.wikipedia.org

## ความลับของ Prime number

ในเปเปอร์ “On the Number of Primes Less Than a Given Magnitude” ที่เขียนโดย Riemann นี่แหละที่บอกวิธีทำ complex analysis แต่ว่ามีบอกต่ออีก เกี่ยวกับความลับของ prime number

**On the Number of Primes Less Than a Given Magnitude - Wikipedia***" Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse" (usual English translation: " On the Number of Primes…*en.wikipedia.org

ก่อนอื่นคงรู้จัก prime number (2 3 5 7 11 13 ..) ที่มนุษย์โลกยังไม่รู้ว่ามันมี “สูตร” อะไรของ sequence ที่ว่านี้ แค่คิดได้ว่าเลขนี้เป็น prime มั้ย ตัวต่อไปต้องงมหาเอง แถมต้องคิดเช็คใหม่อีก ออกมาเป็นการบ้านสุดทรมานที่เราเคยทำกัน

### จุดไหนได้ 0

เหมือนแต่ก่อนตอนทำการบ้าน เพื่อการศึกษา อยากรู้ว่าฟังก์ชั่นหน้าตายังไงจะได้ตีกราฟได้ ต้องเอาไป = 0 ให้รู้ว่าตัวแปร x y ค่าเท่าไหร่ทำให้ผลเป็น 0

Riemann บอกว่า ความลับของ prime number นี้เกี่ยวข้องแน่ๆ กับจุดที่ทำให้คำตอบเป็น 0 ได้ของฟังก์ชั่น Riemann zeta function แต่จุดพวกนั้นอยู่ไหน พวกโลภมากที่อยากจะได้ หาให้เจอเซ่ ฉันทิ้งไว้ในโลกอันกว้างใหญ่นี่แหละ! หะฉิเกโรว อยู่เมโว

**Prime number theorem - Wikipedia***In number theory, the prime number theorem ( PNT) describes the asymptotic distribution of the prime numbers among the…*en.wikipedia.org

### Prime-counting function

แม้ว่าเป้าหมายหา explicit function ที่ใช้เสก prime จังๆได้จะดูเกินไปหน่อย แล้วถ้า “prime-counting function” ล่ะ (มี prime กี่ตัวใต้เลขนี้ เช่นถ้า 10 ก็ตอบ 4 เพราะมี 2 3 5 7) ก็ยังเหมือนจะมาเกี่ยวข้องอย่างมากกับ Riemann zeta function อีกจนได้ครับ! Riemann บอกว่าฟังก์ชั่นของเขาเนี่นอธิบายได้ว่า Prime-counting function นี้จะต้องโค้งขึ้นช้ากว่า integrate ของ 1/ln แน่ๆ ซึ่งตรงกับที่ Gauss และสหายค้นพบไว้แล้ว

**Prime-counting function - Wikipedia***In mathematics, the prime-counting function is the function counting the number of prime numbers less than or equal to…*en.wikipedia.org

prime-counting function ที่ค้นพบนี่เหมือนจะไร้ประโยชน์แต่จริงๆน่าสนใจ เพราะเราได้รู้ว่า prime ก็มี character ของมันอยู่จริงไม่ได้มั่วแบบสิ้นหวัง (เช่นถามว่าใต้เลข 49283498 มี prime x ตัวเป็นไปได้มั้ย ทีนี้เราตอบได้แล้วว่าได้หรือไม่ได้ แบบแน่ๆ)

### Euler product

Euler ได้พิสูจน์ว่าถ้าเอาเลข prime มาเรียงคูณกันไปเรื่อยๆนี่ สุดท้ายมันจะได้เหมือนกับ Riemann zeta function เฉยเลย! (อย่าลืมว่า Riemann zeta function เป็นการเอามาบวกกันแล้วก็แค่เลขเรียงกันไม่เห็นเกี่ยวกับ prime.. ดังนั้นดูเผินๆอันนี้ค่อนข้างมหัศจรรย์)

**Euler product - Wikipedia***In number theory, an Euler product is an expansion of a Dirichlet series into an infinite product indexed by prime…*en.wikipedia.org

### โอกาสสุ่มได้ Coprime

1/RiemannZetaFunction(n) เนี่ย เป็นโอกาสที่เลือกสุ่มเลขมา n ตัวแล้วทุกตัวเป็น coprime กัน (หรม. เป็น 1) เช่นเลือกเลขอะไรก็ได้มั่วๆมา 3 ตัว โอกาสคือ 1/1.202 = 83% เลยนะ

**Coprime integers - Wikipedia***In number theory, two integers a and b are said to be relatively prime, mutually prime, or coprime (also written…*en.wikipedia.org

มองไปทางไหนก็เจอ prime ขนาดนี้แล้วเราเลยยิ่งต้องหาให้ได้ว่าจุดไหนกันแน่ที่จะทำให้เป็น 0

## Trivial zeros กับ Critical line และปัญหาเงินล้าน

![](../../assets/36e75d0141e3cf89.png)

ถ้าค่า s ที่เข้าไปเป็นเลขคู่วิ่งไปทางลบนี่ มันจะม้วนไปลง 0 เด๊ะๆแน่ครับ อันนี้เขาว่าง่าย เลยตั้งชื่อว่า trivial zeros

แต่! มีเส้นตั้งเส้นนึงตั้งชื่อว่า critical line เส้นนี้อยู่ที่ x = 1/2 แน่ๆ (อย่าลืมว่าส่วนนี้เคยอยู่ในเขต undefined ก่อนจะทำ complex analysis) แล้วมีส่วน y (ส่วน i) เป็นจุดประปรายอย่างที่เห็น hypothesis เลยกล่าวว่า

นอกจากตรง trivial zeros แล้ว ค่าอื่นๆที่ input เข้าไปแล้ว sum ออกมาได้ 0 ทั้งหมด อยู่บน critical line (1/2 + ???i)

**Riemann hypothesis - Wikipedia***In mathematics, the Riemann hypothesis is a conjecture that the Riemann zeta function has its zeros only at the…*en.wikipedia.org

ผ่านมาร้อยกว่าปียังไม่มีใครมาบอกได้ว่าประโยคนี้จริงแน่ จนกระทั่งเมื่อวานนี้ครับ

### ทำได้ไง

เหมือนว่าพระเอกคือ “Todd function” ซึ่งผมยังไม่ได้ไปดูว่าคืออะไร แต่เห็นว่ามีบทความกับการถกเถียงขึ้นมานเน็ตบ้างแล้ว แล้วก็แน่นอน ไม่น้อยเลยที่กำลังดราม่าว่าไม่ใช่ของจริง! แก่แล้วพอเถอะ…

**Riemann hypothesis, fine structure constant, Todd function***This morning Sir Michael Atiyah gave a presentation at the Heidelberg Laureate Forum with a claimed proof of the…*www.johndcook.com

**What is the definition of the function T used in Atiyah's attempted proof of the Riemann…***In Michael Atiyah's paper purportedly proving the Riemann hypothesis, he relies heavily on the properties of a certain…*mathoverflow.net

**Is there a way to discuss the correctness of the proof of the RH by Atiyah in MO?***I just made a question in MO to discuss the correctness of the proof provided by Prof. Atiyah for the Riemann…*meta.mathoverflow.net

**Riemann hypothesis, the fine structure constant, and the Todd function**** | Hacker News**[Riemann hypothesis, the fine structure constant, and the Todd functionnews.ycombinator.com](https://news.ycombinator.com/item?id=18059880)

**Nice try but I am now 99% confident that Atiyah's proof of RH is wrong, hopeless***The live video stream from Atiyah's talk (9:45-10:30) was mostly overloaded but we may already watch a 49-minute-long…*motls.blogspot.com

ตอนนี้เห็นว่าเขาจะทำบทความอธิบาย proof สำหรับคนไม่ใช่นักคณิตให้อ่านได้อยู่ แล้วก็คงต้องมี peer review อีกครับ ว่าจะจริงมั้ย… ตอนนี้ wiki ของ millenium prize problem ยังไม่เห็นว่าแก้เป็น solve แล้ว สมมติถูกจริง คิดว่าน่าจะต้องตีความต่อไปว่าบน critical line นี้มี pattern น่าสนใจแบบไหนรออยู่

## ถ้าสมมติแก้ความลับของ prime number ได้แล้วจะเกิดอะไรขึ้น

ถ้าเรารู้ว่า prime number ไม่ลับอีกต่อไป อาจจะโลกแตก 555 เช่นพวก security ของคอมหลายอย่างก็ใช้สมบัติที่ว่า prime มันลับในการเข้ารหัส ถ้าจะแฮคก็ทำได้แค่ brute force แบบเป็นล้านปีเสร็จก็เลยสรุปว่าปลอดภัย แฮคไม่ได้ ทีนี้ถ้า prime มันไม่ลับแล้วทุกอย่างก็อาจจะเละ..

เอาใหญ่ใหญ่กว่านั้นก็ไขปริศนาของธรรมชาติและโลก เพราะเขาเชื่อกันว่าที่ธรรมชาติเป็นธรรมชาติและอธิบาย 100% ไม่ได้ ส่วนหนึ่งเพราะ prime number กุมความลับอยู่ (what is the model of naturalness?)