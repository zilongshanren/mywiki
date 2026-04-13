---
title: ไขความลับ ทฤษฎีหมูกรอบ
url: https://gametorrahod.com/mu-krob-theory/
author: Sirawat Pitaksarit
published: '2019-07-19'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

**Update : ตอนนี้ย้าย blog อาหารไปอีกที่แล้ว จะได้ไม่ปนกับ blog โปรแกรมมิ่งครับ : https://jingjang-cooking.com/mu-krob-theory/**

เรื่องก็คือตอนแรกแค่อยากทำหมูสามชั้นทอดสีน้ำตาลที่เคี้ยวแล้วไม่ต้องคายหนังกินกับข้าว ทอดกระเทียม ยังไม่ถึงขั้นหมูกรอบขาวเหลืองแบบที่ร้านที่ใส่กะเพราหรือเป็นข้าวหมูกรอบที่ราดน้ำแดงๆ

คืออยากทำประมาณนี้ ร้านสารพัดหมูนี้ที่เมเจอร์รัชโยตรงโซนลานข้างนอก อร่อยมาก มี 4 สไตล์หมูให้เลือก น้ำจิ้มแจ่วเด็ดที่มีมะขามเปียก แล้วก็ผักต้มฟรี แค่ 40 บาท เพอร์เฟ็คสุดๆ

![](../../assets/fa6fa13e247adb0c.jpg)

![](../../assets/ad9f6cec814a2451.jpg)

## Take 1 : Naive approach

เรื่องมันเริ่มมาจาก ตอนแรกว่าจะทดสอบอีกความเชื่อนึง ที่ว่าผสมๆไปเหอะ แป้งข้าวเจ้าข้าวโพด ก็เลยจะลองว่าอันผสมแป้งข้าวโพดกับไม่ผสม ต่างกันยังไง (เลือกแป้งข้าวเจ้าล็อคไว้ เพราะเป็นสิ่งที่มีในส่วนผสมของโกกิ) อันนี้ไม่ได้กะจะทำหมูกรอบ (ขาวเหลือง) แต่เอาแบบหมูสามชั้นทอดกรอบแค่นั้น (น้ำตาลๆ)

![](../../assets/d9a46180323ce97c.jpg)

![](../../assets/6545613b3caef4a2.jpg)

![](../../assets/5feb070c49d6e7e8.jpg)

![](../../assets/7cc911a27c96fd70.jpg)

ทอดออกมาดำก็เลยไม่รู้เรื่องว่าแป้งไหนดีกว่ากัน 555 แต่ที่สำคัญกว่า คือ**หนังมันต้องคาย** **หนังไม่กรอบ **ถึงจะไม่ได้ทำหมูกรอบขาวเหลืองก็เหอะ แต่หมูสามชั้นผัดซอสแบบนี้ก็อยากได้แบบกินได้เพลินๆเลย

ตอนแรกคิดว่าต้องไฟไม่แรง จะได้ทอดจนกรอบได้ก่อนดำ แล้วเอาหนังลงทอด แล้วก็ห้ามหั่นด้วยเพราะไม่งั้นจะตั้งด้านหนังลงระหว่างทอดไม่ได้ แต่พอไปถามเพื่อนแม่ครัว เพื่อนบอกว่าวิธีที่ถูก **ต้องต้มก่อน**แล้วค่อยเอามาทอด

ฟังดูมีเหตุผล เหมือนตอนทำไข่พะโล้ เมื่อต้มจนคอลลาเจนในหนังกลายเป็นเจลาติน ทีนี้ก็จะเคี้ยวหนังเข้าได้

### Bonus take

ก่อนไปต่อเอาที่เหลือมาอบแทน คิดว่าใช้เวลานานขึ้นได้แล้วจะรอด แต่สุดท้ายหนังก็ยังแข็งๆอยู่ดี (แต่รสโอเค ชอบน้ำเกลือข้างล่างที่ไหลออกมา กินเปล่าๆกับข้าวยังได้)

![](../../assets/94f0d33b635b72fa.jpg)

![](../../assets/3eafdef115815bbe.jpg)

![](../../assets/8c47083d52f3cc19.jpg)

## Take 2 : ต้ม? ส้อมทิ่ม? แห้ง?

จากการสอบถามเพื่อนเพิ่มเติม มีสิ่งต้องทำเพิ่มขึ้นอีก

- แห้ง : อันนี้เบสิคของอาหารชุบแป้งทอดเพราะถ้า soggy แล้วน้ำมันกับน้ำอยู่ด้วยกันมันจะระเบิดกันเองแล้วไม่ได้ทำให้หนังกรอบ พอเข้าใจได้
- ต้ม : อันนี้ที่ว่าให้หนังกินได้
- ส้อมทิ่ม : เหตุผลคือน้ำมันจะได้เข้าไประเบิดจากข้างในให้กรอบ

ตอนนี้นี่เองที่เริ่มเปลี่ยนความสนใจ จากหมูสามชั้นผัดซอสที่กินได้ มาทำหมูกรอบขาวเหลืองดู คิดว่าถ้าทำอันนั้นได้น่าจะไขความลับแห่งหนังหมูไปประยุกต์ทำแบบไม่กรอบได้

ไปเจอมาหลายเว็บบอกว่าตอนต้มสามารถ infuse ได้ คิดว่าไม่น่าจะถึงขั้นทำให้ผลการทดลองเพี้ยนจากกรอบเป็นไม่กรอบเพราะใส่เม็ดเก๋ากี้ลงไป นี่ก็เลย ต้มแบบต้มทำหมูพะโล้เลย **ต้มจนเปื่อย**

![](../../assets/0233d7e76b26b42a.jpg)

![](../../assets/95c832767176ae9c.jpg)

![](../../assets/52c41d7792b4428c.jpg)

แช่ผ่านไปสามคืน ออกมาจากตู้เย็น แห้งสุดๆ แล้วก็เอาลงไปทอดหลังจากชุบแป้ง ที่ผสมน้ำเย็นเจี๊ยบเพื่อชะลอปรากฏการณ์ glutenize ตามความรู้อาหารชุบแป้งที่ศึกษามา กรณีที่อยากให้เหนียวนุ่มแบบนั้น คือตอนทำขนมปัง แบบนั้นอยากให้ร้อนมากกว่าเย็น คนที่มีหัตถ์ตะวันจะได้เปรียบ

![](../../assets/8c14435776331a91.jpg)

![](../../assets/6ef58df6dd86681f.jpg)

![](../../assets/832b4f0a857db4ae.jpg)

![](../../assets/c2e4ca486c372643.jpg)

![](../../assets/b53a5bfe16dfd4b3.jpg)

แบ่งการทดลองเป็น 4 ชุดคือ ทิ่ม ไม่ทิ่ม ทิ่มโกกิ ไม่ทิ่มโกกิ ผลออกมาปรากฏว่า เหมือนกัน!!

อันนี้ทอดโดยใช้วิธีที่เจอมาจากเว็บนึง คือเขาว่าทำด้านเนื้อให้โอเคก่อน แล้วสุดท้ายค่อยเอาหนังลงจ่อน้ำมัน ต้องไม่ร้อนเว่อร์มากไม่งั้นดำก่อนกรอบ ดูภาพอาจจะเห็นฟองๆที่ดู promising

แต่ข้างในเป็นหมูพะโล้! คือมันเป็นหมูพะโล้ชุบแป้งทอดกรอบ ไม่ใช่หมูกรอบ และไม่ใช่หมูสามชั้นทอดด้วย... นุ่มจนขนาด ไม่สามารถใช้มีดผ่าแล้วคงรูปได้

![](../../assets/9cae40d49163fdf6.jpg)

![](../../assets/97b773231e4e7e99.jpg)

มันก็อร่อยนะแต่มันไม่ใช่หมูกรอบ เหมือนอารมณ์ขาหมูเยอรมันมากกว่า (ถ้ามีซอสเขียวนี่เข้ากันเลย...) ถ้านับเป็นหมูกรอบ หนังอันนี้เรียกกันตามเว็บฝรั่งว่า silky skin เป็นหนังกระจอก กรอบก็จริง แต่เป็นแผ่นบางๆ ไม่ระเบิด แล้วก็ที่สำคัญ ดูทุเรศ

![](../../assets/5116cc0ea0b01326.png)

### Why

- ต้องต้มนานน้อยกว่านี้?
- ต้มน้ำตื้นๆให้สุกแค่หนัง เนื้อจะได้เหลือความเคี้ยวได้ จริงๆเนื้อไม่จำเป็นน่าจะต้องลดความคงทนมันเพราะส่วนนี้ติดมันในเนื้อน่าจะนุ่มพอดีอยู่แล้ว
- ต้องแห้งกว่านี้?
- ต้องอบ? ไม่ใช่ทอดเลย?

### แห้งแบบไหนคือแห้งจริง?

สงสัยอีกอย่างคือ ภูมิปัญญาเว็บฝรั่งไม่ตรงกับคนไทย ที่เจอมาหลายเว็บมากที่บอกว่าแช่ตู้เย็นให้แห้งได้??

![](../../assets/143f87d23ee38eda.png)

![](../../assets/01b99899a7200df6.png)

![](../../assets/31b8aa5dead15685.png)

![](../../assets/06f1394542ca773c.png)

![](../../assets/c2fb183db0cd83fe.png)

อีกท่านึงที่ support ความแห้งคือ ให้ทาเกลือหนาๆ แล้วค่อยขูดเปลือกเกลือออกทีหลัง เหตุผลคือเกลือจะช่วยดูดความชื้น

แต่เพื่อนไทยบอกว่าการแช่ตู้เย็นให้แห้งมันจะไปแห้งได้ไง ต้องตากแดดสิ เอ๊ะ อันนี้รู้สึกแปลกๆตรงที่ผักเวลาแช่นานๆยังแห้งจนกรอบได้แล้วทำไมเนื้อไม่เหมือนกัน?

![](../../assets/3dd698bfce953241.png)

### White vinegar??

ไปกันใหญ่อีกครั้ง เมื่อเจอหลายๆเว็บบอกให้ทาน้ำสมสายชู "แล้วจะกรอบ" โดยที่ไม่มีคำอธิบายอื่นอีกเลย? ทำไม?

### Baking powder / baking soda

อันนี้พอฟังขึ้นอยู่ว่าถ้าทาผงฟู แล้วเอาไปอบ มันก็จะ ฟู 55555 จริงๆคือเป็นความฟองฟอดเวลามันโดนความร้อน ฟองที่ว่าคือ carbon dioxide (C + O O = CO2) แล้วฟองพวกนี้น่าจะเข้าไปในรูที่เสียบไว้แล้วระเบิดออกมา (น่าจะ) ศัพท์ทางเทคนิคคือ มันเป็น leavening agent อีกตัวที่น่าจะคุ้นกัน คือยีสต์ ที่พอใส่น้ำร้อนให้มันกลับมามีชีวิตแล้วมันจะกินน้ำตาลแล้วตดออกมาเป็น CO2 แต่ทำงานช้ากว่า ค่อยไปค่อยไปกว่า เหมาะกับขนมปังคนละชนิดกับแบบที่ใส่ BP/BS

## รวบรวมความรู้จากเน็ตเพื่อหา correlation

ในเมื่อแต่ละคนบอกไม่เหมือนกัน แต่ละเว็บก็บอกไม่เหมือนกัน แต่ที่สำคัญ ทุกเว็บได้หมูกรอบแต่เราไม่ได้หมูกรอบ 555

ถ้าลัดไปทำตามสูตรเด๊ะๆเลยคิดว่าน่าจะออกมากรอบ แต่สูตรต่างๆที่หลับหูหลับตาบอกไม่เคยพูดถึง fail case มีแต่ถ้าเป๊ะได้ ไม่เป๊ะไม่รู้ไม่ชี้ ไหนๆก็ fail แล้ว เลยอยากจะใช้ approach เหมือนเขียนเปเปอร์คือต้อรู้ก่อนว่าแวดวงเราใครทำอะไรได้ผลยังไงบ้าง แล้วค่อยๆเอามา debug ของๆเรา ก่อนจะ derive สูตรของเรา ซึ่งถ้าไปตรงสูตรที่อ่านมาก็ไม่เป็นไรแล้วเพราะรู้ว่าทำไมต้องแต่ละขั้น ละแต่ละขั้นถ้าขาด จะได้หรือไม่ได้ ทดแทนด้วยอย่างอื่นได้ยังไงบ้าง (เช่นถ้ารู้เหตุผลว่าทำไมต้องทิ่ม แล้วไม่มีที่ทิ่ม กรีดเอาได้มั้ย หรือต้องเป็นรูทรงกลม อะไรงี้)

บทความที่อธิบายเรื่องนี้ได้ดี :

อ่านดูตรงที่บอกว่าถ้าคนของทำขนมปังแล้วจะเกิด gluten คือ ด้วยเหตุผลแค่นี้ ทำให้ทุกอย่างกระจ่างขึ้นมาเลย แล้วพลิกแพลงต่อได้ว่าเมนูไหนควรคนมากหรือคนน้อย แต่มันเป็นสิ่งที่สูตรไม่บอกนี่สิ เพราะสูตรบอกว่าแค่ "คนให้เข้ากัน"

So cookbooks are wonderful, but there's much that recipes don't tell you about cooking. Understanding how ingredients interact and the logic behind techniques helps you cook successfully.Once you know what makes a recipe work, you can fill in the gaps yourself.If you are already accomplished in the kitchen, understanding the science behind cooking is the ideal foundation formaking changesand creating new recipes. Become a better cook with science!

ว่าจะให้นี่เป็น guide หมูกรอบแรกในประเทศไทยที่อธิบาย fail case ได้ ไม่ใช่แค่สูตร ต่อไปนี้จะสรุป point สำคัญจากแต่ละเว็บ และเขียนไว้ว่ามีเหตุผลมั้ย

- ทิ่ม ไม่มีเหตุผล
- ทาเกลือ ไม่มีเหตุผล (อร่อย?)
- แช่ตู้เย็น
**เหตุผล**to dry out the skin - อบ

- สูตรป้าจาเร็ต ป้าบอก ป้าไม่อบ ป้าทอด
**เหตุผล**อบใช้เวลานาน ทำให้เนื้อแห้ง ทอดดีกว่า - ล้างเนื้อด้วยน้ำเย็น ไม่มีเหตุผล
- ต้ม 15 นาที
- ทิ่ม ไม่มีเหตุผล
- ทาเครื่องปรุง ไม่ต้องทาด้านหนัง ไม่มีเหตุผล
- ทอดด้านหนังลง 5 นาที

(ต่อจากนี้เวลาไม่มีเหตุผล จะไม่พิมพ์ว่า "ไม่มีเหตุผล")

- เว็บเดียวกัน แต่ทีนี้เปิดมาอย่างองอาจ "There is no need to poke the pork skin, no vinegar, no pre-boiling the pork belly." ไม่ทิ่ม ไม่สายชู ไม่ต้ม
- อบไอน้ำ ในเตาอบใส่จานน้ำ แล้วหมูลอยอยู่ข้างบน
- หลังอบเสร็จ เช็ดให้แห้ง
- ด้านหนังทาเกลือหนาๆเป็นแผ่น ด้านเนื้อทาเครื่อง
- อบร้อนกลาง 1 ชม. ตำแหน่งเตาอบคือติดเพดาน
- เอาแผ่นเกลือทิ้ง
- อบร้อนสูงอีก 40 นาที ตำแหน่งติดเพดานเหมือนเดิม (ทำไมต้องแวะเอาเกลือทิ้งก่อน??)

- เว็บเดียวกันกับอันแรกแต่ทีนี้ ไม่ต้องทิ่ม ก็คือทำตามเว็บที่แล้วเด๊ะ
- "You don’t need to dry the skin overnight, marinade the meat, score the skin, or puncture holes."
- ใช้เกลือ
**หนาๆ**เพื่อให้หนังกรอบ "What really intrigued me was that it uses a salt crust to crisp the skin." คือพอทำเสร็จแล้วให้ยกแผ่นเกลือนี้ทิ้ง หนังข้างในจะเหลืองทองไม่ดำ - แช่ตู้เย็น
**เหตุผล**เพื่อให้แห้ง "I also wanted to make sure the skin was extra dry, so I went ahead and put it in the fridge for several hours to dry out and give time for the meat to marinate." - ตอนทาน้ำหมัก ห้ามทาหนัง
**เหตุผล**ต้องให้หนังแห้งไงล่ะ - ท่าเดิมกับเว็บที่แล้วหมด อบไอน้ำ ถอดเปลือก อบต่อ

- เปิดมาด้วยสามเหตุผล
- To achieve a crispy crackling, you need the pork skin to be very dry.
- Salt helps to draw moisture out of the pork
- and leaving overnight uncovered in the fridge helps to dry out the pork.
**but if you dont have time for this a hair dryer can work wonders.**ใช้ไดรเป่าผมแทนได้**เอาเกลือออกให้หมด**หลังจากแช่ข้ามคืน อ้าว อันอื่นเขาเอาเกลือพอกกัน- เคลือบ
**น้ำมัน**และน้ำส้มสายชู Covering with a mixture of hot oil and DYC white vinegar ไม่มีเหตุผล อันนี้มาแปลก มีน้ำมัน

- ก่อนทิ่ม ต้ม แค่ 3 นาที (อีกเว็บที่ผ่านมา 15 นาที)
- ทิ่ม เว็บนี้มีเหตุผลที่ดี! "The fat oil produced in the roasting process need ways to come out. Why we need oil coming through the holes? Because hot oil brings hot temperature, which can keep the rind something like gently deep-fried for a quite long time." ถ้าอบต้องมีที่ให้ไขมัน
**ออกมา**(แสดงว่าตรงข้ามกับเหตุผลที่ให้น้ำมันเข้าไประเบิดผ่านรู ของแบบทอด?) ทำไมต้องออกมา? ไม่งั้นมันจะทอดอยู่ข้างในระหว่างอบ ต้องให้มันออกมาทอดข้างนอก.. อืมม - ทาผงฟูกับน้ำส้มสายชู มีเหตุผล! "
**Applying baking soda or white vinegar can help to soften the skin**and thus making the crispy pork belly even fluffy" ทำให้หนังนุ่ม พอหนังนุ่มแล้ว.. จะกรอบเบา เหมือจะตรงข้าม แต่คิดดูดีๆของที่นุ่มเวลาโดนความร้อนแล้วจะโปร่งและกลายเป็นกรอบ - แต่ว่าสามารถล้างทิ้งได้หลังจาก 30 นาที "But the remaining flavor of baking soda may bring some bitter taste to the skin. So the best solution is to set the pork for 30 minutes and then wash the skin before air-drying." โอเค แสดงว่าผงฟูกับน้ำส้มสายชู take effect ใน 30 นาทีเข้าไปในหนังเสร็จ จบเลย ไม่มีผลตอนทำอาหารจริงๆ? ไม่มีผลกับความร้อน?
- ทำเกลือ เหตุผล! ดูดความชื้น "The salt layer can help to absorb water and keep the skin dry. Cover a layer of sea salt on the surface can help to absorb the water released in the early of the roasting and keep the rind dry."
- let it dry in the fridge. อีกเหตุผลที่สนับสนุนการใช้ตู้เย็นทำให้แห้ง
- ใช้ท่า พอกเกลือ
**กับน้ำส้มสายชู**ไฟกลาง เอาเกลือออก ไฟแรง คล้ายกับที่ผ่านมา

อันนี้เอามาแถม ข้างในไม่มีอะไร แต่ตลกตรงที่ว่าสงสัยเหมือนเราว่าตกลงน้ำส้มสายชูนี่เป็นเวทย์มนต์หรือยังไง แต่ก็ไม่มีใครมาตอบ 555

- ทาน้ำส้มสายชูไปเถอะ ไม่มีเหตุผล "Apparently, rubbing some vinegar on the pork skin will do the trick."
- พรรคแช่ตู้เย็นให้แห้ง "I would leave the meat to dry out uncovered in the refrigerator overnight."
- ทิ่มโดยไม่มีเหตุผล
- ที่เหลือคล้ายๆเดิมไม่มีอะไรใหม่ ท่าอบเบาไอน้ำ แล้วอบแรงจากด้านบน แต่อันนี้ไม่พอกเกลือ ไม่มีเอาเปลือกเกลือออก
**มี diff จากสูตรที่ผ่านๆมา!**ดูดีๆสูตรพอกเกลือ จะอยู่ top rack ตั้งแต่ต้น เอาออกมาแกะเกลือ แล้วก็กลับเข้าไปใน top rack แต่สูตรนี้ที่เกลือกับน้ำส้มสายชูอยู่แบบนั้น แล้วก็เป็นแบบโรยไม่ใช่แบบพอก ไม่มีการเอาออก ตอนแรกอยู่ rack กลางก่อน แล้วค่อยเอาจริงที่ top rack สั้นๆให้ crackle ตีเป็นความรู้ได้ว่า พอไม่มีพอกเกลือเป็น buffer แล้ว เลยต้องออมมือตอนแรกด้วย

diff นี้เป็นอีกอย่างนอกจากเรื่อง fail case ที่สูตรมักจะไม่พูดถึง ว่าสูตรเราต่างกับสูตรอื่นตรงไหนบ้างและให้ผลต่างออกไปยังไง ดังนั้นเราจะมาสรุปด้วยตัวเอง

- ทิ่ม อันนี้เหตุผลคือ "the first step is to create "one thousand holes" in the skin so that the fat will render." Render นี้ก็คือความหมายเดียวกับคนที่บอกว่าเพื่อให้น้ำมัน
**ไหลออกมา**[https://www.thespruceeats.com/what-does-render-mean-2313707](https://www.thespruceeats.com/what-does-render-mean-2313707) - ทำให้แห้ง โดยการใช้เกลือกับ baking soda (baking power (ผงฟู) ที่ผ่านมา ต่างกับ baking soda..) เหตุผลคือ ดูดความชื้น (ทั้งคู่? เบสก็ดูดความชื้น?) "Scotese's trick to crispy pork belly is to rub equal parts baking soda and salt into the skin—the combo of baking soda and salt will draw out moisture and set you up for success." อันนี้ตอนแรกคิดว่า baking soda/powder เป็นตัวทำให้กรอบอย่างเดียวซะอีก
- อันนี้ใช้พัดลมแทนตู้เย็น Let the pork belly strips "hang out overnight, uncovered, ideally in front of a fan," which will dry them out even more.
- เอาเกลือกับ baking soda ออกให้หมด อันนี้ support เหตุผลเดิมว่าเกลือกับ baking soda ทำให้หนังนุ่มไปแล้ว ไม่มีประโยชน์อีกต่อไป เออแล้วก็อันนี้ยังไม่ได้ต้ม แสดงว่าเป็นขั้นตอนที่แทนการต้มให้หนังนุ่มได้? (โดยการ "ต้มระหว่างทิ้งให้แห้ง" ทางเคมีแทน?)
- ใส่น้ำส้มสายชู แต่ทีนี้มีเหตุผล "Then, as a final step to ensure that the baking soda is neutralized, pour a tiny bit of vinegar over the skin (the less it foams, the better—if it is foaming a lot, rinse the strips again)." แค่เช็คว่า baking soda ล้างหมดยัง (tiny bit แปลว่า ไม่ได้ตั้งใจให้เกิดเอฟเฟคทีหลัง)

- จั่วหัวอย่างองอาจว่า (no skin poking, no vinegar) คือจะ imply ว่าการเสียบกับน้ำส้มสายชูมัน undesirable แต่ที่ผ่านไม่ทำไม่ได้ไม่งั้นไม่กรอบ?
- The most popular method is to poke and brush on the skin a mixture of vinegar + salt or baking soda. อันนี้พูดถึงความไม่มีเหตุผลที่ผ่านมา อย่างไม่มีเหตุผลอีกรอบ
- However this method is quite time-consuming and you always have to worry about not poking the skin too deep, because if you do the fat will leak to the skin while roasting and stop it from popping and turning crispy. ?? เขาบอกว่าถ้าสูตรทิ่ม แล้วทิ่มลึกไป ไขมันจะซึมเข้าไปในหนัง แล้วทำให้ไม่กรอบ ????? อันนี้งงสองชั้น คือไขมันมันคือหนังอยู่แล้ว แล้วซึมเข้าไปในหนังอีกได้ไง แล้วก็ชั้นสอง การทิ่มน่าจะเป็นการทำให้ไขมันออกมา แล้วก็ชั้นสาม เกี่ยวอะไรกับ too deep ถ้าบอกว่า fat leak into the
**meat**อันนี้เข้าใจได้ว่าทิ่มลึก ไขมันเลยซึมเข้าไปในเนื้อแทน แต่คำว่า stop it นี้ it คือหนังแน่นอนไม่ใช่เนื้อ เพราะเนื้อไม่ใช่สิ่งที่จะ turning crispy ได้.. งง - แต่สุดท้ายอันนี้ลิ้งค์ไปหาสูตรพอกเกลือ อบ แล้วเอาออก อันที่ผ่านมา

- หลายคนบอกว่า oil ไม่ใช่สิ่งที่ทำให้เกิด crackle
- น้ำส้มสายชูกับเกลือ มีคนบอกว่าใช่ (คือมีน้ำส้มสายชูตอนอบจริงๆ ไม่ได้ล้างออก)
- คนบอก แห้งก็พอแล้วที่จริง น้ำมันเอามาทำไม
- "The fat bubbles up through the cuts and makes it crispy." ทฤษฎีที่ว่าไขมันจะ
**ขึ้นมา**ในรูหรือรอยตัด เพื่อให้กรอบ

This is what makes all the difference ไม่มีเหตุผล..**Pricking lots of holes in the skin = puffy crackling with bubbles.**Salt draws moisture to the surface, helping to guarantee you’ll get crispy crackling every single time. โอเคอันนี้ใช้ได้ เกลือหนาๆทำให้ดูดความชื้น ออแล้วก็ rock salt ทำให้ไม่ตกไปในรูที่ทิ่มไว้ เดี๋ยวเค็มไป เอาไว้ดูดความชื้นล้วนๆ (บ้านเรา ใช้ดอกเกลือแทนน่าจะได้)**Roast covered in rock salt = crispy crackling.**- มีอธิบายเพิ่มเติมของท่าเอาเกลือออกแล้วอบต่อแรงๆ เพราะว่าการอบเบาที่ผ่านมา เกลือ take effect ดูดความชื้นไปในเตาอบแล้ว
**แต่ยังไม่ได้เอาจริง**เมื่อความชื้นหมดในเตาอบ (ก็คือแช่เย็นมายังไม่พอ ให้เกลือมาช่วยต่อในเตาอบ) แล้วค่อยแกะเปลือกออกแล้วยิงแรงๆใส่จังหวะที่แห้งสนิทเพื่อให้กรอบเต็มที่ - ข้างล่างมีอีกอย่างบอกว่า ถ้าไม่ทิ่มก็ได้
**แต่จะกรอบแบบไม่มีฟอง**อันนี้เป็นเว็บแรกที่แยกความกรอบกับความฟองออกจากกัน แปลว่าการทิ่มเป็น modifier ให้กรอบแบบเป็นฟอง - อันนี้มีอธิบายกรณีทิ่มลึกไป pierce too far into the fat (or even worse, into the flesh), the juices will bubble up onto the skin, and the wetness as the skin is being grilled/broiled will cause little splotches where the skin is not super crispy. น้ำเนื้อจะออกมาทำให้หนังกลับเป็นไม่แห้ง อันนี้โอเคเลย

- อันนี้มี hot take ที่ไม่เหมือนที่อื่น White Vinegar helps dry out the skin ปกติคนจะบอกว่าเกลือดูดความชื้น ทีนี้น้ำส้มสายชูก็ดูดด้วย? but it has a secondary purpose of removing the odour! ดูดกลิ่นอันนี้เห็นด้วย ถึงจะไม่รู้ว่าทำไมก็เถอะ (เกลือก็ดูดกลิ่น?)
- place the Pork in the Fridge UNCOVERED overnight – the skin will dry out. ตู้เย็นคือแห้ง
- ถ้าไม่มีเวลาแช่ "Otherwise if you don’t have time – the hand towel & white vinegar should be adequate and leave it for 30 minutes for the vinegar to do it’s job" ยังยืนกรานกับทฤษฎีแห้งด้วยน้ำส้มสายชู มีบอกด้วยว่า 30 นาทีคือ take effect เรียบร้อย

อันนี้มีสูตรแปลกขึ้นไปอีก

He rubs a six-and-a-half-pound slab of pork belly on its meat side with salt and other seasonings—which he coyly refused to divulge—and hangs it up for half an hour or so to allow the marinade to soak in. He then roasts it, meat side facing a medium fire, until it is about 70 percent cooked through; the heat cannot be too high during this phase, or the skin will lose too much moisture and later refuse to crackle properly.

อันนี้ขั้นแรกคือยังไม่ได้ทิ่มด้วยซ้ำแต่หมักเนื้อเรียบร้อย แล้วอบจนเกือบสุด แต่มีเหตุผลว่าห้ามร้อนมากเดี๋ยวส่วนหนัง**จะเสียความชื้นมากจนทำให้ไม่กรอบ **ตกลงความแห้งทำให้กรอบหรือไม่กรอบ??

Then he removes the pork, pierces its skin all over with an instrument that looks like a wooden mortar with sharp metal prongs protruding from the end, rubs it with just a little salt, and hangs it up for an hour or two in a well-ventilated area. This cooling period, he told me, further promotes the subsequent blistering of the skin.

ทีนี้เอาไอ้ที่เกือบสุกมาทิ่ม ใส่เกลือ **แล้วทิ้งไว้ให้แห้ง **อันนี้แปลกตรงที่ cook ก่อนแล้วค่อยแห้ง เพื่อต่อยกสอง ไม่ใช่แห้งในตู้เย็นมา แล้วยก 1 ยก 2 ต่อๆกัน เหมือนสูตรที่ผ่านมา

In a second round of roasting, Goie faced the skin inward over a fierce, flaring fire. Too low a heat produces what he calls "scorpion skin," tough and chewy—a result of the skin's moisture cooking off too gradually. A sufficiently intense fire turns pockets of moisture in the skin to steam, which expands explosively, creating tiny bubbles with walls of protein that crisp in the scorching heat. Goie let the skin roast until it built up a stratum of char, an assurance that the top layer had fully puffed. He pulled the pork out of the oven and scraped off the char with a blade, to reveal a sandy, golden layer of crunch. "If the skin is thick and not quite done, I do another round of charring and scraping," he explained.

ในยกสองต้องไฟแรงแบบทันที เพื่อให้ expand explosively อันนี้ก็ตรงกับ common sense อยู่ที่หลายๆท่าที่ต่อยกสอง (หลังถอดเปลือกเกลือ ฯลฯ) ต้อง preheat oven

ต่อมามีเหตุผลใหม่

Then I recalled something Pung had said: "Some chefs apply things on the skin—salt, lime juice, baking soda, maltose—to make it more crispy." Acid, alkaline, and alcoholic ingredients all help to denature the skin proteins, disrupting their physical structure and loosening them up, which promotes blister formation and browning.

บรรดาของวิเศษต่างๆ "to make it more crispy" เนี่ย จริงๆถึงจะดูเป็นกรด เบส แอลกอฮอลไม่เกี่ยวกันเลย แต่ทุกอย่างทำลายโปรตีนบนหนัง ทำให้หลวมขึ้น แล้วเกิดฟองง่าย.. อ่าาาาาา

From past failures, I knew that sugar, vinegar, and condiments like soy sauce gave me poor or patchy results, but recipes that used a rubdown of gan sui, or alkaline water, a solution of sodium and potassium carbonates, usually achieved a high degree of puff.

มี remarks ว่าน้ำตาล ซอส **และน้ำส้มสายชู **ทำให้กรอบไม่ดี น้ำส้มสายชูนี้เป็นของฮิตในสูตรที่ผ่านมาพอสมควร ส่วนของที่เป็น alkaline นี้ดี (ก็คือ จำพวก baking soda / powder?)

To reap the benefits of an alkaline wash without soapiness, I ultimately settled on three steps to treat the skin. First, I decided to prick the raw pork skin, which would allow some alkali to seep in.

คนนี้ให้เหตุผลของการทิ่มส้อมต่างออกไป ไม่ใช่น้ำมันระเบิด แต่เพื่อให้ alkaline water เข้าไปได้ต่างหาก

Second, a scald: holding the pork slab vertically over the sink, I used a measuring cup to stream a boiling-hot solution of baking soda and water over the pricked skin side only, to gently soften and denature it.

น้ำ baking soda ที่ว่า **ต้องร้อน **ด้วย ซึ่งไม่มีเหตุผล แต่เหมือนจะพยายามบอกว่าเพื่อให้ soften อย่างนุ่มนวล.. ความร้อนคือความนุ่มนวล?

Third, just before roasting, I brushed the skin with Chinese rose-scented rice wine. Its light acidity neutralizes any remaining soda traces, and its alcohol helps denature the skin proteins.

สุดท้ายทาแอลกอฮอล เหตุผลคือเพื่อสู้กับเบสที่ใส่เข้าไปให้กลับมาเป็นกลาง แล้วก็แอลกอฮอล์ก็ช่วยทำลายโปรตีนตามที่อ้างมา

- ทิ่ม
- ทาซอสด้านเนื้อ ไม่ทาซอสด้านหนัง
- หันหนังขึ้น แช่ตู้เย็น
- ตอนจะอบ โรย baking soda ก่อน ตามด้วยเกลือทับลงไป อันนี้เข้าใจว่าความระเบิดอยู่ที่ baking soda เลยให้โรยก่อนเป็นชั้นชัดเจนไม่ใช่ผสมๆไปเหมือนสูตรอื่น ฉลาด!
- มีบอกว่า ถ้าเปลี่ยน baking soda เป็นน้ำส้มสายชู (เกลือพอกเหมือนเดิม) แล้วกรอบขึ้นอีก กับ texture ดีกว่า

เหยด อันนี้ของจริง ทดลอง 8 อย่างเทียบกัน นี่แหละพ่อครัวที่โลกรอ

![](../../assets/b39725a6442fdb51.jpg)

So everyone agrees main prerequisites are dry skin, good fat layer, scored/pierced skin, salt and lots of heat.

But after reading the two threads I learnt that sometimes the reason we don’t get good crackling is that we haven’t denatured the skin enough as the tough skin prevents the blistering and crackling from forming.

So we can denature the skin by scoring, piercing, heating or using chemcials to attack it

"denature" เป็นเหตุผลเดียวกับเว็บก่อนที่บอกไปที่ว่า กรด เบส แอลกอฮอล์ อะไรก็ช่าง เป็นการทำลายหนังเพื่อให้คลายตัวลง อันนี้ยกไปถึงการทิ่มว่าเป็นการทำลายเซลล์หนังอย่างนึงด้วย (ไม่ใช่ในเหตุผลที่ว่าให้ไขมันซึมออกมา ให้ไขมันซึมเข้าไป)

- คนนี้เป็นสายต้มก่อน แต่ไม่ได้ต้มจริงๆ แล้วก็ไม่ใช่ต้มน้ำตื้นแล้วเอาหนังลง แต่เป็นเทน้ำร้อนผ่านหนังเอา ลวกๆแค่นั้นแล้วก็เช็ดให้แห้ง ดูดี

ทีนี้ ทั้ง 8 เทสที่ว่าคือ

- รอยหั่นมากกว่าเพื่อน คนนี้ไม่ได้ทิ่ม แต่หั่นเป็นเส้นๆเอา
- ใช้ไฟพ่นเฉยๆ แต่ไม่ได้เอาให้กรอบ เอาให้แห้งๆ เหตุผลคือพยายามทำลายด้วยความร้อน
- น้ำเลมอน acidic = denature
- น้ำส้มสายชู acidic = denature อันนี้ acid น้อยกว่าน้ำเลมอน ผลที่คาดไว้คือน้ำเลมอนกรอบกว่าเพราะ denature มากกว่า
- lye water / kan sui อันนี้เป็น 50% potassium carbonate นั่นเอง alkali = denature เขาว่าอันนี้เทคนิคจีนดั้งเดิม
- baking powder นี่คือ 50% sodium bicarbonate ซึ่งก็ alkali = denature แต่หาในไทยได้ง่ายกว่า เบสเข้าครัวนี่นอกจากอันนี้ก็นึกไม่ออกเหมือนกัน แต่เขาว่านี่ alkaline น้อยกว่า lye water ดังนั้นผลที่คาดไว้คือ denature น้อยกว่า
- 40% vodka อันนี้ก็ denature protein แล้วเขาว่าช่วย dehydrate ด้วย (เห็นด้วยอยู่ เพราะแอลกอฮอล์มัน ระเหย?)
- น้ำกีวี่?? contains a protein digesting enzyme called Actinidain and i use this to tenderise tough cuts of beef. โอ้โห อันนี้เพิ่งรู้

ทั้งหมดที่ทาแล้ว เอากลับเข้าตู้เย็นให้แห้งอีกรอบ โอเค รอบคอบ!

Just had a peek this morning and the torched, lye and lemon sections defintely looked a lot drier then the rest followed by the vinegar, soda, vodka.

The wettest looking where the plain scored one and the kiwi one.


น่าสนใจที่ของที่กรดกับเบสสูง แห้งเร็วกว่าเพื่อน แต่ก็จะแช่ตู้เย็นต่อไปให้แห้งสนิท

Great experiment! BTW, baking powder is pH balanced because it includes an acid along with the soda.

ออ้าว ปรากฏว่า baking powder ใช้เป็นตัวแทนของเบสไม่ได้ เพราะจริงๆเป็นกลาง!! สูตรที่ผ่านๆมาที่ใช้ baking powder แล้วอ้างว่าใช้ความเบสก็คือผิด แต่ถ้าอ้างว่า "ทำให้ฟู" (ด้วยฟองฟอด ที่ไม่เกี่ยวกับความเบส?) นี่ก็ไม่รู้เหมือนกัน แต่พอดีการทดลองนี้อ้างว่าเบสจะ denature ก็เลยต้องเอาเคสนี้ออกไป

ตอนอบ ใช้วิธีคล้ายๆที่ผ่านมา คือ middle oven ซักหน่อย แล้วค่อย under the grill แรงๆตบท้าย ภาพแต่ละอย่างแนะนำให้เข้าไปดูเอง แต่ lye water ทำ crackling ได้มากที่สุดแต่ chewy นิดๆ baking power ดันใช้ได้ดีเฉย ส่วนที่ fail ชัดๆอันเดียวคือ kiwi สงสัยทำให้เนื้อนุ่มได้ แต่หนังมีแต่ไขมันนี่สิ

แล้วก็อีกการค้นพบคือ soda เป็นอันเดียวที่อาจทำให้เกิด lifting ได้ คือหนังหลุดออกมาจากเนื้อ

My parents actually said last night that although the crackling was good they have made better. They been in the restaurant trade for over 30 years now and they said that back 20 years ago they could get the most amazing crackling with the minimum of effort. They said they just pierced the skin, rubbed salt and hung it to dry for a few days and the whole piece would blister perfectly.

มีตำนานว่าไปร้านนึง **แค่**ทิ่ม ทาเกลือ แล้ว**แขวนไว้ไม่กี่วัน **แค่นี่ก็เทพแล้ว ต้องไม่แช่ตู้เย็นเหมือนที่เพื่อนไทยว่าจริงๆ? (แต่เนื้อน่าจะต้องระวังเน่า)

just for geeky fun I measured the ph of the different solutions

lemon juice 2.3

vinegar 3.1

baking powder 6.5

alcohol 8.5

Lye water 14

so it seems that the quality of the crackling is proportional to the alkalinity of the liquid.

เขาว่าไว้อีกว่ายิ่ง alkaline ยิ่งดี ถ้าเทียบวัดผล pH กับผลความกรอบที่ออกมา (กรดไม่ช่วยกัดกร่อนเหรอถ้างั้น?)

![](../../assets/834c24d8dd5689ff.jpg)


แต่ alkanity ถึงจะช่วยให้กรอบ ก็มีปัญหาหนังลอย ไม่ใช่แค่นั้น แต่รสเหมือนสบู่! เขาบอกกินเปล่าๆก็โอเคแต่พอเทียบกับอันที่ใส่ vodka แล้วให้ vodka ชนะ

Also the crackling starts to form at the score and puncture points first probably due to the hot oil escaping from those points first.

เขาเฝ้าดูฟองขึ้นพบว่าฟองขึ้นตรงที่ทิ่มก่อนจริงๆ เขาคิดว่าเป็นเพราะน้ำมันร้อน**ออกมา**จากจุดพวกนี้ก่อน

มีอีกอย่างคือ browning หรือ maillard ซึ่งมีข้อมูลนึงบอกว่า ถ้า**เพิ่ม pH **แล้วจะ brown ง่ายขึ้น แปลว่า ยิ่งเป็นเบสยิ่งได้สีเข้ม

หลังจากกระทู้นั้นหยุดไป 5 ปี ก็มีอีกคนมาตอบคำตอบของ vodka

The vodka may assist in this manner, or others, due to any one or combination of the following effects:

1) The ethanol sucks the water out of the skin cells through osmosis, directly drying at least the top layer of skin

2) The ethanol damages the cells/cell membranes, allowing them to burst more readily (?)

3) The ethanol dissolves some of the fat in the skin, whereupon application of heat causes the ethanol to boil away and create additional blisters

Reading material:[http://www.ncbi.nlm.nih.gov/pubmed/9539383][http://www.alcoholjournal.org/article/S0741-8329(02)00198-2/abstract][http://www.paulaschoice.com/expert-advice/skin-care-basics/_/alcohol-in-skin-care-the-facts]

น่าสนใจ แล้วก็ในเรื่องคำว่า "blisters"...

อันนี้เป็นปีกไก่ แต่มีอย่างนึงที่เกี่ยวกับเราคือ **blistering **ก็คือการกรอบเป็นฟองนั่นเอง

As you can see, there is something to the notion that adding baking soda to raise the pH (thus making the wings more alkaline)indeed does helpwith browning—the baking soda–treated wing in the center is significantly browner than the plain wing on the left. The baking powder–treated wing is also browner, though to a lesser degree. (Baking powder is made of baking soda mixed with a powdered acid, and its overall makeup is only slightly alkaline.)

Unfortunately, the baking soda wings had a very distinct metallic bitterness that immediately eliminated them as an option. Baking powder was promising for its effect on browning, but did nothing to aid rendering or blistering.

ใช้เพิ่ม pH นี้ทำให้ brown ขึ้นแล้วก็เขาว่า baking powder ที่กระทู้ที่ผ่านมาว่าเป็นกลาง จริงๆแล้วเป็นด่างนิดหน่อย

Raising the pH does indeed improve browning, but it also creates an environment that weakens the peptide bonds naturally present in proteins. In theory, this means the proteins can break down more easily into shorter pieces, creating a texture that is less leathery or papery and more crispy.

และต่อมาก็สรุปว่าไม่ใช่แค่ brown แต่ทำให้สลายโปรตีนได้ แนะนำให้เข้าไปอ่าน เว็บ Serious Eats นี้ปกติเป็นเว็บที่ตอบปัญหาว่าทำไมได้หลายเมนูมากจนถึงขั้นเข้าเว็บเดียวก็ได้ เสียดายไม่มีหมูกรอบอยู่ในเว็บนี้

มาเว็บไทยบ้าง อันนี้เป็นท่า ต้ม อบ (2 step แบบเบาก่อนแล้วจ่อแรง) แต่มีทอดซ้ำอีกครั้งน่าสนใจดี หาจุดสำคัญมาดังนี้

- "นำหมูสามชั้นไปต้มในน้ำเดือด แล้วหรี่เป็นไฟอ่อน ประมาณ 15 - 20 นาที เพื่อให้หนังหมูสุก นิ่ม ทำให้ใช้ส้อมหรือเหล็กแทงหนังหมูได้สะดวก การแทงหนังหมูก็จะให้ตอนทอด หนังหมูจะพองสวยงาม กรอบ" อันนี้ต้ม 20 นาที เหตุผลให้แทงง่าย (สูตรฝรั่งที่ผ่านมา หลายๆคนแทงตอน raw ด้วยซ้ำ) ส่วนแทงเพื่อให้พองกรอบ
- "เอาเกลือ (และน้ำส้มสายชู) ทำที่หนังหมูเพื่อไล่ความชื้นและทำให้หนังหมูตึง" เกลือกับความชื้นโอเคแต่ตึงนี้ไม่แน่ใจว่าคืออะไร
- "สำหรับหนังหมูอาจจะใช้น้ำส้มสายชูทาที่หนังหมูด้วย จุดประสงค์เพื่อให้หนังหมูแห้ง" เหมือนฝรั่งคนนึงที่บอกว่าไม่ใช่แค่เกลือ น้ำส้มสายชูทำให้ของแห้งได้

พันทิปอันต่อมา จั่วหัวคล้ายๆเว็บฝรั่งเว็บแรกที่ว่าไปคือ "ไม่ต้องต้ม ไม่ต้องตากแดด"

ก็คือบอกกลายๆว่าการต้มกับตากแดด มันไม่ถึงกับเป็น catalyst แต่เป็น contributing factor ดังนั้น การที่จะบอกว่าอันที่เราทำ fail ว่าเพราะเราไม่ได้ตากแดดกับไม่ได้ต้ม มันก็ไม่ถูก เราต้องพลาดจุดอื่นที่สำคัญกว่านี้ไม่ใช่ว่ามาเดาว่า ไม่เป็นหมูกรอบ เพราะ "ไม่เป๊ะ"

อันนี้ให้เหตุผลว่า ถ้า oven ก่อนทอดให้ฟู (สูตรนี้คือ ไม่ได้อบแรงให้ฟูเหมือนฝรั่งแต่เผื่อไว้ทอด) ก็ไม่รู้จะตากแห้งก่อนทำไม เพราะความแห้ง เอาไว้ใช้ก่อนขั้นฟู ถ้าเราอบไปให้ไม่ถึงขึ้นฟูแต่กะไปฟูตอนทอด ก็แปลว่าไม่ต้องตากแดดหรือแช่ตู้เย็นเพราะอบทำให้ satisfy ความแห้งพร้อมกับสุกไปในตัว! โอ้ อันนี้สอนอะไรกว่าที่คิด

"จะใช้วิธีต้มจิ้มหนังตากแดดแล้วทอด หรือ ทำแบบใช้เตาอบก็มี แต่วิธีของแหม่มก็เป็ฯอีกหนึ่งวิธีที่ไม่ยุ่งยากค่ะ มาดูวิธีทำกันค่ะ" เป็นความรู้รอบตัวคนไทยจริงๆว่าการทำหมูกรอบต้องต้ม จิ้ม ตากแดด ทอด อะไรซักอย่างวนอยู่ในนี้ แต่ที่แปลกคือตากแดด เพราะไม่มีฝรั่งคนไหนตากแดด ตู้เย็นทุกคน แต่เพื่อนใน Twitter นี้ ตากแดดทุกคน เป็นความรู้ตกทอดจากรุ่นแม่โดยแท้

อันนี้เป็นสายด้านหนังไม่ใช่แค่เกลือ แต่น้ำมันพืชด้วย ทาทับเกลือลงไป ไม่ใช่เกลืออยู่บน (คือกะให้เกลือดูดน้ำ แต่น้ำมันให้ระเบิดลงไป?)

อันนี้น่าเสียดาย อยากให้บางชิ้นเอาน้ำมันออกให้ดูด้วยว่าเป็น myth หรือส่งผลจริง เห็นทำหลายชิ้น

เอาล่ะ เว็บสุดท้าย

อันนี้เปิดมาแรง 555

Firstly, let’s take grandma’s folklore out back and shoot it. Almost every ‘guide to perfect crackling’ mindlessly follows a few techniques, none of which our testing showed as making a jot of difference to the end result.

- ลวกหนังโดยผ่านน้ำร้อนเพื่อรีดไขมันออก ไม่มีผล
- ต้มหนังก่อน ไม่มีผล แถมทำลายเนื้อ
- ทำน้ำมันบนหนัง เขาบอกว่าหนังก็ไขมันจะทาไขมันอีกทำไม ไม่มีผล แต่ช่วยให้เกลือเกาะได้ ดังนั้นควรทาก่อนเกลือ ไม่ใช่เกลือก่อนน้ำมัน
- preheat ให้ร้อนก่อนค่อยเอาเข้าเตา ไม่มีผล
- ทาเกลือแล้วแช่ตู้เย็นให้แห้งดูดความชื้น เขาบอกยิ่งทำให้เนื้อเน่า ดูดจนแห้งเป็นซอมบี้ 555
- โปะเกลือ เขาบอกเค็มก็อร่อยแหละแต่ไม่ได้ช่วยให้กรอบ
- ตัดหนังออกมาทอด อันนี้ไปกันใหญ่ 555 เขาบอกคนจริงต้องไม่ซ่อม

The only thing you can take away from this is that all of these people are doing what grandma said in the hope that a light and fluffy slab of cracking will emerge. Importantly, no one explains the actual reason they can get crackling. Again, it is all down to the method of heat transfer.

Lemon and salt and whatever other voodoo you’ve read about is irrelevant (except for taste!) – this is all you need to know. You need to heat the rind of the pork in what is called ans-curve of temperature. You need to do this using mainly radiant heat. This means you are heating the rind up, then as the heat builds you remove it from the heat just short of it burning but don’t let it cool down too much, and apply heat again. You need to watch what you are doing closely however you will be rewarded with perfect crackling, across 100% of the surface of the rind, every single time without exception.

สั้นๆคือคนนี้ไม่แช่ตู้เย็น ไม่ต้องส้อมทิ่มดูดน้ำพอกเกลืออะไรทั้งสิ้น แต่ต้องคุม radiation heat ดีๆแค่นั้นเอง แต่ก็ยาก! เพราะสูตรนี้ต้องเสียบไม้หมุน แล้วคอยหมุนให้พอจะถึง burning point จะได้รีบ cool down กลับลงมา แล้วความร้อนต้องเป็น radiation heat หรือก็คือก่อไฟด้วยถ่าน หรือเตาอบที่เป็นแท่งแดงๆนั่นแหละ (อีกสองแบบคือแบบเตาลมร้อน กับแบบ contact เช่นการใช้กระทะ)

คือบรรดาเวทย์มนต์ทั้งหลายในสูตรอื่น มันอาจจะแค่ช่วย achieve s-curve temperature ของที่คนนี้อ้างถึง อันนี้ที่ตีความเองนะ เช่น ถึงพอกเกลือ คนนี้จะว่าไม่ช่วยให้กรอบหรอก แต่ที่แน่ๆ ช่วยกันไม่ให้หนังไปก่อนเนื้อเวลาอบได้ จนกว่าเราจะ limit break มาแกะมันออกเพื่อใส่เฮือกสุดท้าย อาจจะได้ผลออกมาเหมือนที่คนนี้ว่า

## ทดลองโบนัส กับซากที่เหลือ

### Oven dried vs sun dried

ตอนนั้นที่เพื่อนว่าแช่ตู้เย็นมันจะไปแห้งได้ไง ต้องตากแดดสิ พอดีมีที่ต้มแล้วเหลืออีกอันยังไม่ได้ทอด ก็เลยจะทดสองสมมติฐานเพื่อนดู

แต่ไม่มีแดด! ก็เลยจะใช้เตาอบแทน โดยเปิดโหมดร้อนจากแค่ข้างบน (simulate เหมือนดวงอาทิตย์) และร้อนแค่ 100 C คือต่ำสุดเท่าที่ทำได้ แล้วก็เอาต่ำอีกโดยการแง้มฝาไว้ แล้วก็วางเล็งให้ไม่อยู่ใต้แท่ง แถมถาดล่างสุด ในโหมดร้อนบน

เห็นเว็บฝรั่งบอกแบบนี้ก็ dehydrate ได้แต่ก็ต้องใช้เวลานานพอๆกับแดด แบบ 5-6 ชม. (แต่ใช้ได้ดีกับเนื้อสัตว์ เพราะถ้าเอาเนื้อไปตากแห้งด้วยแดดข้างนอก เสี่ยงเน่าเพราะแบคทีเรียข้างนอกเยอะ เวลาอุณหภูมิสูงแล้วเติบโตได้ดี)

![](../../assets/ee396cfe1c5d1827.jpg)

![](../../assets/42d656a74c263825.jpg)

ผ่านไปหลาย ชม. เอาออกมา ปรากฏว่าจากต้มแบบพะโล้จนทิ่มได้ง่ายๆ กลายเป็นทิ่มไม่เข้า 5555 อบจนเหนียว อีกอย่าง ชิ้นนี้สัดส่วนมันกับเนื้อไม่ดี แทบไม่มีเนื้อเลยจนจะเป็นมันทาหมูกระทะแล้ว ก็เลยกะจะทิ้งอยู่แล้ว

### Boil -> oven

ยังไม่หมด ไอ้ซากหมูพะโล้ชุบแป้งทอดนั้นตั้งแต่ต้นบทความนั่นแหละ ยังกินไม่หมดเลย ว่าจะเอามาใส่มาม่าแห้ง OK ไข่เค็ม เพราะมันไม่กรอบอยู่แล้วกินนุ่มๆกับของเส้นน่าจะเข้ากัน อารมณ์เหมือนบะหมี่เนื้อตุ๋น

ไหนๆก็ไหนๆ ก็เลยลองเอาหนังที่ fail แล้วไปอบ ก่อนใส่มาม่า อันแรกที่ทำ อย่าลืมว่าตอนนั้นยังไม่ได้คิดจะทำหมูกรอบเหลืองขาวเลย คือจะชุบแป้งทอดแค่นั้น.. ยังไม่ได้แตะเตาอบซักนิด แล้วสูตรที่เห็นๆมา ส่วนมากจะเตาอบอย่างเดียว ไม่ก็อบทอด หรือต้มทอด หรือต้มอบทอด ฯลฯ ไม่มีสูตรไหน ต้ม ทอด อบ อันนี้ทอดแล้วพังเลยเอามาอบซ่อมหวังว่าหนังจะคืนชีพได้

![](../../assets/782c6c5a9647cc2c.jpg)

![](../../assets/4b5dbee2736476a4.jpg)

![](../../assets/a3565df0a965b122.jpg)

ไปไกลกว่านี้ไม่ได้เดี๋ยวดำ เพราะมันดำมาจากทอดระดับนึงแล้ว แต่ถึงจะไม่เกิดฟอง crackle ก็เหอะ แต่รสชาตินี่หนังหมูกรอบเลย (เริ่มเห็นความหวัง..) เหลือแต่ความหนา กับทำให้พองให้ได้ก่อนถึง threshold ดำ ที่อ่านมา ต้องเลย threshold ไปหน่อย แล้วใช้มีดขูดดำๆออก ไม่ก็ใช้ท่าเกลือหนาพอกแล้วแกะออก

## ทบทวนความผิดพลาด และสร้างสูตรของเราเอง

แน่นอนเราไม่ควรเชื่อกับทุกอย่าง เพราะบางอย่างขัดกันชัดๆแต่ก็ได้หมูกรอบออกมาเหมือนกัน ดังนั้นเรามาวางแผนก่อนซื้อหมูสามชั้นรอบต่อไป

### Baking soda / น้ำส้มสายชู

อันนี้ตัดสินใจว่าจะใช้ สรุปที่เรียนมาก่อน

Baking soda กับ baking powder ชื่อเกือบเหมือน แต่ soda เป็นเบส อีกอันเกือบ pH balanced

Baking soda นี่คือ sodium bicarbonate (NaHCO3) ล้วน เป็นเบสแท้ในครัวอย่างเดียวที่นึกถึง ถ้าเจอกรด จะเป็นฟอง แต่ถ้า powder คือ baking soda + กรด เพื่อให้เติมแค่น้ำก็ฟองฟู่ได้

หมูกรอบฝรั่งที่ศึกษามา บางสูตรบอก powder บางสูตรบอก soda เพราะในเนื้อมีกรดอยู่บ้างแล้วเลยแทนกันได้ แต่ว่าเขาว่าเบสสามารถกัดกร่อนโปรตีนได้ ถ้าใช้เวอร์ชั่น soda จะ denature หนังให้นุ่มได้มากกว่า ซึ่งไม่รู้จะลดหรือเพิ่มความกรอบ

แต่เบสมีอีกเอฟเฟคคือทำให้ไหม้เป็นสีน้ำตาลน่ากิน (maillard) อ้างอิงจาก Speeding up the Maillard reaction > [https://blog.khymos.org/2008/09/26/speeding-up-the-maillard-reaction/](https://blog.khymos.org/2008/09/26/speeding-up-the-maillard-reaction/) ดังนั้นถ้าใช้ baking soda หมูกรอบจะดำกว่า

![](../../assets/4cb6c95c9d3e4991.jpg)

![](../../assets/061376178e9e9bdb.png)

แล้วที่ดูมายังมีสาย ทิ้งโซดาไว้ กับสาย ล้างออกด้วยน้ำส้มสายชู เพราะอ้างว่ามัน take effect กับหนังเสร็จแล้ว (ให้นุ่ม ให้ระเบิดกรอบง่าย?) เราไม่จำเป็นต้องทิ้งรส metallic ปะแล่มๆของเบสไว้ น้ำส้มสายชูเลยมาล้างออกให้กลับมาเป็นกลาง

Verdict : จะใช้ baking soda เพื่อ denature หนัง แล้วจะล้างออกด้วยน้ำส้มสายชูด้วยเนื่องจากที่บางคนบอก รส metallic ของ alkalinity ไม่ค่อยโอเคเท่าไหร่ อันนี้เชื่ออยู่ แล้วก็เทียบกับอีกอันที่ไม่ใช้โซดา ส่วนน้ำส้มสายชูก็ว่าจะไม่ทิ้งไว้บนหนังด้วย ว่าจะให้มีแต่เกลือ (ซึ่งมีพอกกับไม่พอก ให้ตัดสินใจอีกที)

### ทิ่มไม่ทิ่ม

คนที่อ้างว่าไม่ต้องทิ่มก็ได้ ส่วนมากเหมือนจะเพื่อความสะดวกสบาย แล้วก็มีอีกเหตุผลนึงคือถ้าทิ่มแล้วเสี่ยงทิ่มไปถึงเนื้อ ทำให้ไขมันที่ควรจะออกมา เข้าไปแฉะใส่เนื้อ

ในเมื่อส่วนมากเป็น inconvenience ดังนั้นเราจะทิ่ม ด้วยความระมัดระวัง ถ้าไม่ทำพลาด กับไม่นับว่าเสียเวลา แบบนี้น่าจะดีกว่าไม่ทิ่มแน่นอน?

แล้วก็มีทิ่มก่อนแช่ค้างคืน กับทิ่มหลังแช่ แต่คิดว่าไม่น่าเกี่ยว ตราบเท่าที่เราทิ่มก่อนทำให้สุก (แบบเอาจริง ไม่ใช่ต้มแรก)

### ต้มไม่ต้ม

ที่อ่านๆมามีเวลาต้มตั้งแต่แค่เทน้ำร้อนผ่าน จนถึงต้ม 3 ถึง 15 นาที หรือไม่ต้มเลยก็มี คนต้ม มีต้มแบบ infuse รส หรือต้มเฉยๆ หรือต้มแบบน้ำตื้นให้โดนแค่หนัง ที่แน่ๆ ไม่มีใครต้มจนเปื่อยเหมือนที่พลาดอันแรก 555

จากการที่ fail มา ขอเดาว่า เนื้อไม่จำเป็นต้องต้ม เนื้อส่วนนี้ติดมัน คิดว่าให้มันสุกไปกับขั้นตอนทำปกติน่าจะดี ส่วนต้มหนังมั้ย มีสองอันที่คิดไว้

- ต้มหน่อย เพื่อทำลายโครงสร้างให้ระเบิดง่าย (เชื่อว่านุ่ม = กรอบ)
- ไม่ต้มเลยดีกว่า รูที่ทิ่มจะได้ระเบิดกับหนังแข็งๆให้บรู้มอย่างรุนแรงที่สุดกับความ contrast กัน (เชื่อว่าแข็ง = กรอบ)

ไม่ต้มก็อยากลอง แต่ว่ามีอุปสรรค คือลองแล้วทิ่มไม่เข้า! คนที่ทิ่มโดยไม่ต้ม เขามีเหล็กแหลมกัน แต่หนังสดๆลองใช้ส้อมธรรมดาแล้วทิ่มไม่เข้า

![](../../assets/49e5554801d87187.jpg)

![](../../assets/ad2443c9366133f1.jpg)

![](../../assets/b53cdc8143bdb520.jpg)

![](../../assets/c10095c77664c130.jpg)

![](../../assets/0f4c1ab1258a14ec.jpg)

ดังนั้นแทนที่จะต้องไปหาซื้อเหล็กแหลม คิดว่าวิธีที่ดีที่สุดคือ จะต้มจนกว่าจะทิ่มเข้า แล้วอีกอัน ต้มมากกว่านั้นซักหน่อย แล้วจะได้เทียบกัน (คิดซะว่าอันแรกเป็นไม่ต้ม แค่ต้มพอทิ่มเข้า) ผลการ debug ออกมาคือ ต้มแค่ 3 นาทีก็เปลี่ยนจากส้อมทิ่มไม่เข้า (แบบทิ่มแล้วยวบหนีตามส้อม) เป็นทิ่มเข้าแล้ว ตอนแรกคิดว่าหนังจะอึดกว่านี้ แต่เคี้ยวเข้านี่น่าจะต้องนานกว่านี้ ต่อจากเคี้ยวเข้าก็เป็นระดับละลายในปากเหมือนหมูพะโล้ ซึ่งอันนั้นเป็นแบบที่พลาดครั้งแรก น่าจะมากไป

ก็เลยตัดสินใจว่า อันนึงต้ม 3 นาที อันนึงต้ม 10 นาที จะได้เทียบกัน ในภาพสุดท้าย อันบน 10 นาที หนังออกมาสีน้ำตาลกว่าเยอะ ส่วนอันต้มสามนาทีหนังออกชมพู จากสีขาวจั๊วะ อ้อแล้วก็ ต้มแบบน้ำตื้นให้โดนแต่หนัง จากที่ตัดสินใจว่าเนื้อจะไม่แตะต้องอะไรเพราะเชื่อในมันที่แทรกอยู่จะละลายมาเป็นความนุ่มระหว่าง cook

### หมัก

![](../../assets/ddd317533c4954d1.jpg)

หลายๆอันที่บอกว่าซอสหมักต้องโดนแค่ส่วนเนื้อ เหตุผลเพราะไม่งั้นหนังจะไม่แห้งดีเวลาออกมาจากตู้เย็น อันนี้ฟังเข้าท่า ก็เลยจะทำงั้น ทางหนัง บางคนก็บอกทาเกลือดูดความชื้นไว้ บางคนบอกไม่เกี่ยว แต่จะทาไว้ละกัน แล้วก็อย่าลืมนี่

From past failures, I knew that sugar, vinegar, and condiments like soy sauce gave me poor or patchy results, but recipes that used a rubdown of gan sui, or alkaline water, a solution of sodium and potassium carbonates, usually achieved a high degree of puff.

ดังนั้นพวกซอสจะต้องหลบๆตรงหนังหน่อย ปล่อยให้มีแค่เกลือ ไม่ก็พวกเบสต่างๆ อันนี้น่าสนใจที่ vinegar อยู่ในส่วนของสิ่งที่ไม่ดี แต่ก็มีสูตรนึงที่ vinegar มีบทบาทแค่มาล้างเบสออกก่อนอบ แทนที่จะทิ้งไว้แล้วไปอบเลย

แล้วก็หลายๆสูตรที่ออกจีนหน่อย ทำรอยบากไว้ตรงเนื้อเป็นช่องๆด้วย น่าจะทำให้ซอสเข้าไปข้างในดี กับไว้เล็งหั่นหลังจากออกมาแล้วน่าจะสะดวกก็เลยหั่นบ้าง

### พอกไม่พอก

มีสายที่ใช้เกลือเม็ดใหญ่ๆพอกแบบกะไว้แกะออกทีหลัง กับสายที่เกลือปกติเข้าไปเลย อันนี้น่าเล่นทั้งคู่ ก็เลยจะลองทั้งคู่ด้วย แต่คงต้องแยกอบคนละรอบเพราะแบบที่เกลือพอก สามารถอบ upper rack ได้ตั้งแต่ต้นเพราะมี buffer

rock salt ไม่มี แต่มีดอกเกลือที่ซื้อมาจากจังหวัดอะไรซักอย่างอยู่ น่าจะใหญ่พอพอกได้เหมือนกัน

มีอีกสองทฤษฎีเกี่ยวกับเกลือพอก (crust) ที่ว่าจะไม่เชื่อ

- "Uses a salt crust to crisp the skin" อันนี้ยิ่งไม่ได้บอกอะไรเลย ไม่ใช้ก็น่าจะกรอบเหมือนกัน แต่เดาว่า point คือช่วยกัน
**ไม่ให้กรอบแบบดำ**เพราะขั้นสุดท้ายเราแกะเกลือออก ก็แกะความดำออกไปด้วยโดยไม่ต้องใช้มีดมา scrape ตอตะโกแบบบางสูตรที่ไม่มีพอก ที่จำเป็นต้องเลย threshold ไปดำหน่อยเพราะไม่งั้นส่วนอื่นยังไม่เหลืองทองแล้วมาขูดแก้ทีหลัง การใช้เกลือพอก เหมือน allow ให้เหลืองทองเท่ากันทุกจุดได้ เกลือพอกเป็นเหมือน capacitor ที่เป็น rubber band คุมอยู่ข้างบน ตรงไหนยังไม่กรอบเป็นฟองก็ไปของมัน ตรงไหนเป็นแล้วก็จะโดนห้ามไม่ให้ไปถึงขั้นกลายเป็นสีดำ - ที่ว่าเปลือกเกลือช่วยดูดน้ำ - อันนี้คิดว่าสิ่งที่เกิดขึ้นจริงๆคือมันกันไม่ให้ความร้อนเข้าไปจังๆมากกว่า ขั้นดูดน้ำ ไม่น่าเกิดขึ้นตอนอยู่ในเตาอบ ถ้าพอกเกลือตอนแช่ตู้เย็นยังพอว่า เพราะเหมือนเทคนิคเช่น dry brining ที่โรยเกลือแล้วแช่ทิ้งไว้แห้งๆ

### ทอดหรืออบ

ที่อ่านมาส่วนมากจะอบ แต่มีสูตรป้านั่นที่ทอดเอาด้วยเหตุผลที่ถ้าทอดแล้วจะคงความ juicy ของส่วนเนื้อขาวได้มากกว่า กับสูตร pantip นึงที่ใช้ท่า ต้ม อบ ทอด ด้วยเหตุผลที่ว่าประหยัดเวลาอบ (ที่อาจต้องรอจนเลยมื้อ) และได้หนังกรอบคล้ายๆกัน ให้ความร้อนสูงจากน้ำมันพืชมาช่วยเร่งหนังระเบิด

ครั้งนี้ เดี๋ยวกรณีแยกจะเยอะไป ขออบอย่างเดียวก่อนละกัน

## Take 3 : ถึงเวลาแก้แค้น

ไม่อยากลองหลายตัวแปรพร้อมๆกันเดี๋ยวผลออกมาไม่รู้เรื่อง เพราะฉะนั้น รอบแรกจะเป็น..

## ต้มหนัง 3 นาที vs ต้มหนัง 10 นาที

ทิ่มเหมือนกัน หมักแค่เนื้อเหมือนกัน หนังโรยเกลือแห้งๆเหมือนกัน แช่ตู้เย็นนานเท่ากัน

พลาดที่นึงคือกะจะแช่วันนึง แต่พ่อมาเยี่ยมเลยอยู่ในนั้นมา 3-4 วัน ไม่แน่ใจว่ามันจะ neutralize ที่ต้มเวลาต่างกันทิ้งไปรึเปล่า หนังดำเชียว แต่อันที่ต้มนานกว่า (อันที่ดูเป็นเส้นแบนน้อยกว่า) ดูจะผิวดำกว่า สอดคล้องกับตอนก่อนแช่

![](../../assets/ce716f9463b9ee4c.jpg)

![](../../assets/e381e8ff8600ab06.jpg)

![](../../assets/4adfe608a0bab916.jpg)

ที่ค้นคว้ามาอาจจะเผลอสนใจแต่ process แต่ลืมดูตัวเลขต่างๆ กลับไปดูมา พบว่าสูตรที่มี 2 phase คือแบบออมมือก่อน แล้วเอาจริงให้หนังกรอบอีกช็อต ไม่ว่าเอาจริงจะเป็นอบ rack บนหรือทอดช่วย **ตอน phase แรก อุณหภูมิเฉลี่ยอยู่ที่ประมาณ 150-175 องศา C **ซึ่งเตากระจอกก็ไปได้ถึง 250 C แล้ว บางคนอาจจะคิดว่าเตาไม่ค่อยดี เอาแรงสุดไปเลย...แบบนั้นไม่ใช่ แรงไป

แล้วก็ เวลารู้สึกจะอยู่ที่ 1 ชม. ถึง 1 ชม. ครึ่ง ส่วนตัวคิดว่า ไอ้ 30 นาทีที่บวกมานี่อาจจะอันตรายไม่รู้ขึ้นกับอะไร (แต่ทั้ง 1, 1.5 ชม. ก็ออกมาเหลืองทองเหมือนกัน) ดังนั้นผ่านไป 1 ชม. แล้วจะลอง debug ว่าควรต่อมั้ย ก่อนเข้า phase 2

และหลายๆเว็บ ภาพตอนดิบ แว้บไปเป็นภาพตอนสุกสวยงามเลย ซึ่งจะทำให้เราพลิกแพลงไม่ได้เวลา gone wrong ระหว่างทาง ดังนั้นเราจะเปิดดูทุกๆช่วงเวลาว่าตอนนี้เป็นไง (ไม่ต้องกลัวเสียความร้อนเนื่องจากไม่ใช่เตา convection แต่เป็น radiation.. รีบเปิดรีบปิดก็โอเค)

### Phase 1 : 10 นาที

![](../../assets/69e55919417077df.jpg)

ขอบดำๆที่เห็น ตอนแรกเผลอบิดไป 250 C ประมาณ 1-2 นาที แบบ มันไปไวมาก - - เกือบละ

### Phase 1 : 25 นาที

![](../../assets/a6ed8e14b1ad6914.jpg)

น่าสนใจ! ชิ้นที่ต้มนาน 10 นาทีเกิดฟองก่อน ทั้งๆที่ทิ่มรูพอๆกัน แสดงว่าหนังที่โดน denature ด้วยความร้อนมากกว่าอาจจะทำให้รูที่อยู่ข้างใน effective กว่า น้ำมันไหลออกมาง่ายกว่า คิดว่าสมมติฐานที่ว่าแน่นๆแข็งๆแล้วระเบิดแรง (ก็คือต้องไม่ต้ม หรือต้มให้น้อยที่สุดเท่าที่พอจิ้มได้) อาจจะไม่จริง

### Phase 1 : 40 นาที

![](../../assets/85c6b7b7e268deb7.jpg)

อันขวาดูน่ากลัว ภาวนาว่าอย่าเพิ่งไหม้นะลูก ยังไม่ขึ้น phase 2 เลย

### Phase 1 : 50 นาที

![](../../assets/d584cd9935da6178.jpg)

ขอยกมาใส่หลอดไฟให้ชัดเจนขึ้น เหมือนเริ่มเห็นสีเหลือง?? จากอีกอัน แสดงว่าของจริงมันจะเหลืองทองใช่มั้ย... จะว่าไป 175 องศานี่มันสำคัญตรงที่มันคุมหนังไม่ให้ไหม้ได้ แต่ทำให้พองได้ แต่ก็ยังไม่ถึงกับพองระเบิด

### Phase 1 : 60 นาที

![](../../assets/6a8db3abc0d70ca2.jpg)

แน่นอน ในเมื่อเราเป็นนักวิทยาศาสตร์ดังนั้นเรามาลองพิจารณารสชาติก่อนเข้า phase 2 กันดู รับรองไม่มีสูตรไหนเคยบอกเพราะมันถือว่ายังไม่เสร็จ

### Intermission

![](../../assets/f1c715b55e0279c7.gif)

ข้างในมีน้ำออกมาค่อนข้างเยอะ ถ้าไม่มีห่อฟอยล์คงลงไปเดือดฟู่ข้างล่างแล้ว

![](../../assets/6958440548437990.jpg)

![](../../assets/811ad07c1bd0023f.jpg)

![](../../assets/ca47a92acecaf4f7.jpg)

![](../../assets/04d83e6448fd12a2.jpg)

![](../../assets/7fdb9c0d81a0d0ba.jpg)

![](../../assets/0c6852e796a57e15.jpg)

![](../../assets/2aab60f00513cc08.jpg)

![](../../assets/566efc147b7fdf94.jpg)

ฝานออกมาชิมนิดนึง ก่อนจะเอาที่เหลือไปต่อ phase 2

- อันที่ต้ม 3 กับ 10 นาที ตอนนี้ดูแทบไม่ต่างกันเลย!
- ความกรอบ.. ตอนนี้เริ่มเข้าใจละว่า crispy มันไม่เท่ากับ crackle เพราะอันนี้มันกรอบแบบ กึก.... ป๊อก! คือมันฟองยังไม่พอนั่นเอง ไม่ใช่ light and fluffy เป็นกรอบเหมือนคุกกี้ ไปดูว่า phase 2 จะช่วยได้มากแค่ไหน
- สีข้างนอกดำมากแต่ข้างในยังขาวอยู่เลยอุ่นใจ
- เรื่องความนุ่มของเนื้อ.. อืมมมมม ตอนแรกที่ทำนายไว้ว่าไม่ต้องต้มส่วนเนื้อเพราะหวังให้มันมาช่วย รู้สึกช่วยน้อยกว่าที่คิด ได้เคี้ยวมันก็ดีแหละแต่แอบอยากได้ละลายในปากมากกว่านี้นิด (แต่ก็ไม่สลายเป็นพะโล้เลยแบบครั้งแรก..) บางคนอาจจะชอบระดับนี้ก็ได้ แต่ส่วนตัวอยากได้นุ่ม innate มาตั้งแต่แรกอีกหน่อย

ก่อนไปต่อ เช็ดหนังให้แห้งให้มั่นใจ ถึงมันจะดูแห้งอยู่แล้วก็เหอะ

![](../../assets/450a0984b878a25b.jpg)

ครั้งนี้เอาไฟ max แล้วใช้ upper rack ส่วนเวลาไม่แคร์ ว่าจะหยิบออกมาเรื่อยๆ ว่ามันดูไปต่อไม่ได้แล้วรึยัง (ถ้าเตาแบบมองเห็นได้ง่ายกว่านี้ก็ดี แต่นี้มันมองไม่เห็นถ้าไม่หยิบออกมา)

![](../../assets/946a0ed2b06b4e94.jpg)

Tips !

- ทางที่ดีควรใช้ไม้บรรทัดวัดก่อนว่าติดแท่งมั้ย ถาดบนมันสูงมาก ถ้าหมูชนแท่งนี่ไหม้เลย
- ฟอยล์กดเก็บๆลงมาให้ดี ให้หนังนูนเหนือฟอยล์ เพราะถ้าเสียบเข้าไปแล้วโดนแท่ง ฟอยล์ไหม้นี่กลิ่นแบบ วิทยาศาสตร์คลุ้งเต็มห้อง เหม็นแบบแสบตามากไม่รู้สารอะไรบ้าง แทบเอาออกมาแก้ไม่ทัน (ดูแท่งแรกดีๆจะเห็นว่ามีคราบฟอยล์ไหม้ติด.. ไม่รู้จะเอาออกมั้ย)

### Phase 2 : 2 นาที

![](../../assets/c3f5666600eee3ee.jpg)

### Phase 2 : 4 นาที

![](../../assets/3aa220e8d29fed86.jpg)

โหหหห ผ่านไปแปปเดียวเริ่มดูเข้าท่า ก็เลยคิดว่าพอดีกว่า *สูตรที่ผ่านมา บอกว่า 10-20 นาทีเลยทีเดียว แต่นี่รู้สึกว่าสุดละ

อะไรที่เกี่ยวกับเวลา + ของที่ขึ้นกับเครื่องมือหนักๆเช่นอบ (ถ้าทอด มันยังพอเหมือนๆกันได้) ควร debug ด้วยตัวเองต่อจากสูตรเสมอ เพราะสูตรไม่สามารถคุมสภาพอากาศหรือเตาเครื่องเดียวกับเราได้

### เสร็จแล้วเป็นไง!

![](../../assets/e3b511276a2eaec7.jpg)

![](../../assets/a5451b9809362e30.jpg)

เปลี่ยนจากกรอบ**ป๊อก** เป็นกรอบ**กรอบ**แล้ววววว T T ยังมีอะไรให้พัฒนาอีก แต่อย่างน้อย attributes ก็เหมือนหมูกรอบตาม definition แล้ว phase 2 นี่สำคัญจริงๆ

ทุกสูตรที่ดูมา ถ้าลองจับมารวมกันมีสิ่งที่ไม่มีสูตรไหนพูดถึงเลย แต่คิดว่าสำคัญมากคือ**คอนเซ็ปต์ของ phase 1 / phase 2** (พิมพ์มานานละ แต่ขอ define ตรงนี้) บางสูตร ต้ม อบ อบ บางสูตร ต้ม อบ ทอด ฯลฯ แต่จุดสำคัญคือ ใน phase 1 จะต้องเลี้ยงหนังไว้ไม่ให้ crackle ก่อนเวลา แล้วไปใส่ทีเดียวเร็วๆใน phase 2 เปลี่ยน texture ไปเลย

![](../../assets/fe17e82286824c38.png)

เพราะแบบนี้ ไอ้แรกสุดที่ทำหมูพะโล้ โผล่มาทอดเลยมันเลยอาจจะ ขาด attribute บางอย่างของ phase 1 เช่น "ไม่ว่าจะแช่ตู้เย็นกี่วัน ก็ไม่มีทางแห้งได้จริงถึงระดับเซลล์" (อันนี้เดาว่ามีจริง) พอเราโผล่มาจัดเต็มด้วยน้ำมัน requirement มันก็เลย fail แล้วไม่พอง (สูตรพันทิปที่โกงทอด ก็เลยต้องมีอบก่อน)

แล้วก็นึกได้ว่านี่มันเหมือนอะไรบางอย่าง ตอน phase 1 ที่กรอบป็อกมันเหมือน.. **ข้าวเกรียบมโนราห์ที่ยังไม่ทอด**ไงล่ะ! น่าจะหลักคล้ายๆกัน phase 1 คือการพยายามเปลี่ยนหนังให้อยู่ใน "มโนราห์ state" แต่ยังไม่ฟู ใน phase 2 ก็เปรียบได้กับการทอดข้าวเกรียบให้จากแข็งๆ (แต่ก็กรอบ.. แบบแข็งๆ) ให้กลายเป็นฟู

### Scraping

บางสูตรเห็นเขาตั้งใจเลยไปขั้นไหม้ แล้วเอามีดมาขูดทีหลังให้เพอร์เฟ็ค ก็เลยลองบ้าง

![](../../assets/adeb3b9b2102e8ba.jpg)

![](../../assets/8bb8d62b14a1f634.jpg)

คือมันก็ออกแหละแต่ออกไวกว่าที่คิด ถ้าไม่แคร์หน้าตาแล้วอยากเอามะเร็งออกเฉยๆก็โอเค แต่ครั้งหน้าควรเบาๆมือกว่านี้

### รอยบากที่ทำไว้

![](../../assets/c69686509f83fff9.jpg)

![](../../assets/6189b97bddbb3501.jpg)

รอยที่ทำไว้ให้ของหมักเข้าไปได้ มาช่วยให้หั่นง่ายขึ้นด้วย เพราะหั่นจากทางหนังมันจะลื่นแล้วก็ยาก ส่วนหั่นจากอีกทาง อย่าลืมว่าหมูนี้มีชั้นมันอยู่ตรงกลาง ถ้าไม่มีรอยมาก่อน มันจะดิ้นเลื่อนหรือแม้กระทั่งขาดได้เลย มีรอยนี่ช่วยได้มากกว่าที่คิด

![](../../assets/fdfaaefeb721fb2f.png)

### อบซ้ำได้มั้ย

หลังจากหั่น sample ไว้ใส่มาม่าแล้ว ที่เหลือแอบอยากลองอบต่อว่าจะไปได้อีกมั้ย

![](../../assets/39a18c73a1b3b334.jpg)

![](../../assets/64c142e9d96633b6.jpg)

ผลออกมา เหมือนกับว่าไม่ค่อยได้ผลแฮะ การพอง คิดว่ามันต้องเป็นจังหวะที่ดันพื้นผิวออกมาสดๆเท่านั้น พอมัน set ตัวแล้ว เราไม่สามารถแก้อีกรอบได้ เหมือนกับว่าจังหวะนั้นมีน้ำมันและอื่นๆ เหมือนขนมปังที่อบจากเล็กๆเป็นฟู ก็ไม่น่าจะอบต่อให้ฟูต่อได้เหมือนตอนมาจากเล็กๆ (เพราะอะไร?)

นี่คงเป็นเหตุผลของที่ว่าไม่ว่าสูตรไหนๆก็ต้องมี phase 2 (แม้กระทั่งสูตรพันทิปที่โกงทอดทีหลัง ก็ต้องมีการอบนำร่องก่อน) เพราะไม่งั้นการพองจะเกิดขึ้นไวไปแล้วมันจะจบตรงไหนไม่รู้ใน phase 1 แบบไม่ defined พอ เราเลยต้องอย่าให้ถึง breaking point นั้น เลี้ยงไฟเบาๆไว้ก่อน อันนี้น่าจะเป็นจุดสำคัญมากของหมูกรอบ

### สิ่งที่ยังไม่ถูก

- หมักเนื้อให้เค็มกว่านี้ ไม่ต้องออมมือ
- ดำตรงหนังนี่ มันขมแบบไม่อร่อยเลย ตอนแรกคิดว่าไหม้ๆหน่อยน่าจะอร่อย แต่นั่นใช้ได้แค่กับเนื้อ หนังมันประมาณว่า ดำคือขม 100% เหมือนฟ้าทะลายโจรยังไงยังงั้น ดังนั้น เทคนิค buffer เกลือนี่ก็น่าสนใจมาก
- หนังก็จืดไป ออมมือเกลือไปหน่อยเพราะเห็นหลายๆสูตรชอบเตือนว่าระวังมัน salty
- ลดเวลา phase 1 เหลือซัก 40-50 นาที จะได้มี headroom เยอะๆใน phase 2 ให้พองโดยไม่ดำได้
- สรุปคือต้มหนังกี่นาทีก็คล้ายๆกัน... ล่ะมั้ง ไปเน้นต้มเนื้อให้นุ่มกว่านี้แล้วไม่แคร์หนังน่าจะดีกว่า ดังนั้นรอบต่อไปจะต้มทั้งชิ้นไม่ต้องมาคอยระวังหนัง แต่ถ้าให้เทียบ อัน 10 นาที พองสะใจกว่า แต่มันดำ ซึ่งน่าจะแก้โดยวิธีอื่น
- น้ำหมัก ลืมใส่พริกไทย
- น้ำหมัก แอบอยากลองใส่น้ำตาล ปกติใส่สารพัดของกุ๊กกิ๊กครัวไทยหมดแล้วก็พอ แต่รู้สึกว่าถ้ามีน้ำตาลอาจจะเพิ่ม depth ได้ ออกหวานจะได้เป็นสไตล์บาร์บีคิวหน่อยๆ เรื่องน้ำตาลนี้ เป็นการเพิ่มอีก 1 reaction ต่อจาก Maillard reaction คือ Caramelization ซึ่งให้รส complex แบบ burnt sugar แบบที่ฮิตกันในชานมตอนนี้นี่แหละ

ปล. บทความนี้[https://amazingribs.com/tested-recipes/salting-brining-curing-and-injecting/salting-and-wet-brining](https://amazingribs.com/tested-recipes/salting-brining-curing-and-injecting/salting-and-wet-brining)บอกว่าน้ำตาลก็ช่วย Maillard ได้ เว็บนี้ก็อธิบายดีแต่เน้นแค่เรื่องบาร์บีคิว

ปิดฉากของที่ไม่อร่อยพอด้วยตัวเองทุกอย่าง ด้วยการโยนใส่มาม่ากลายเป็นอาหาร 1 มื้อ เย้

![](../../assets/bc57b55df2d85554.jpg)

## Condiments vs no condiments

condiments ที่ว่าคือเราจะราด baking soda และล้างออกด้วย vinegar เพื่อตบ pH กลับมาก่อนเอาไปอบ เทียบกับไม่ราดดู ทีเหลือเหมือนกัน + แก้ไขสิ่งที่ยังไม่ถูกทั้งหมด (แก้ให้เหมือนกัน)

เรื่องต้ม ทีนี้เลยเอาตามแผนต้มทั้งชิ้นเพื่อจุดประสงค์ทำ damage ให้เนื้อไม่ได้แคร์หนัง แล้วก็ที่เรียนมา การเปลี่ยน collagen เป็น gelatin เน้นเวลามากกว่าความร้อน ดังนั้น ก็เลยเปิดไฟ 1 แล้วแช่ไว้แบบนั้นซักครึ่ง ชม.

To keep meat tender yet safe during braising, you must maintain an important balance. Cooking temperatures must be high enough to kill microorganisms, yet not so high that the meat toughens. Use a thermometer to check the temperature of the surrounding stock and keep it at a simmer of 180 F/82 C-190 °F/88 °C.

เดี๋ยวว่าจะซื้อ thermometer อยู่ จะได้เช็คกับบทความต่างๆได้

![](../../assets/3ccbdce8f7be54b1.jpg)

อันนี้พอดีเก็บซุปที่ต้มรอบแรกจนออกมาเป็นพะโล้ไว้อยู่ เสียดายใบ bay ที่แช่ไปแล้วเพราะในขวดนึงมันมีไม่กี่ใบ เลยเอามาใช้ใหม่ ต้มแบบท่วมเลย

ผ่านไป 30 นาทีไม่รู้นุ่มพอยังเพราะต้องเผื่อไปนุ่มใน phase 1 ด้วย แต่ถ้ายังเดี๋ยวรอบหน้าค่อยเพิ่มเวลาต่อ ผลออกมา surprise จิ้มหนังไม่เข้า 555 อีกแล้วเหรอ!

![](../../assets/eb91f52595d1b83b.jpg)

แสดงว่า ไฟเบา ถึงจะใช้เวลานานก็เหอะ แต่ไม่สามารถเทียบเท่าไฟเดือดแล้วโดนหนัง 3 นาทีได้เลยแฮะ สรุปคือ ต้องต้มหนังล้วนอีกหน่อยอยู่ดีเพื่อให้จิ้มได้ ดังนั้น แบ่งซุปมาต้มตื้นๆอีกหน่อย

![](../../assets/d35e4d958215a020.jpg)

![](../../assets/438e4a4bd7f104a0.jpg)

ออแล้วก็เรื่องขนหมูที่ยังเหลืออยู่ตั้งแต่ซื้อมาจากห้าง หลายๆที่บอกให้เอามีดขูดแต่นี่ลองแล้วก็ไม่ออก ถึงกรอบพองแล้วจะมองไม่เห็นก็เหอะแต่ควรมีมีดปอกเปลือกผลไม้ไว้เอาออกจะได้รู้สึกดี

น้ำหมักหลังจากแก้สูตรเท่าที่พอใจแล้ว ก็ท่าเดิม หมักแค่เนื้อ หนังซับให้แห้งละโรยเกลือ (เยอะกว่าเดิม)

![](../../assets/eb214782d559df84.png)

![](../../assets/88b239c2dac09e95.png)

### Osmosis vs diffusion / หมักก่อนต้ม หรือ ต้มก่อนหมัก ?

เออแล้วก็เพิ่งมานึกออก.. หมักหลังต้มเนื้อไปแล้วแบบนี้แล้วมันจะเข้าเนื้อมั้ยหว่า? (คือคิดว่าเวลาโปรตีนแข็งตัวจนเนื้อขาวไปแล้ว กลัวความอร่อยของน้ำหมักจะเข้าไปไม่ได้) กลับกัน ถ้าหมักตอนดิบให้พอใจ แล้วเอามาต้มทีหลัง ที่หมักไปแล้วจะหลุดมั้ยหว่า?

ตอนนี้เชื่อแบบที่ว่า ต้มแล้วหมักก็เข้า ดีกว่าหมักแล้วไปต้มแล้วมันล้างออก (หรือต้อง หมัก ต้ม หมัก?) แต่เนื้อที่เห็นนี้ก็ dry brine มาแล้ว (ก็คือโรยเกลือแล้วแช่ตู้เย็นไว้เฉยๆ) คิดว่าน่าจะเค็มมาแต่แรกบ้าง

มาลองใช้เหตุผลวิเคราะห์กันด้วยการทดลองจากบทความนี้ ใน context ของการแช่น้ำเกลือ (wet brine) หรือทาเกลือ (dry brine) แล้วจากนั้นเราค่อยมา apply กับการหมัก เพราะคิดว่าน่าจะคล้ายๆกัน

เรื่อง osmosis จริงๆมีอีกอย่างคือ diffusion ที่อาจจะงงว่ามันเหมือนกันมั้ย ซึ่งตอนพยายาม brine โดยการแช่เกลือ หนังสือส่วนมากบอกว่าตอนแช่เกลือ จะอธิบายว่าด้วย osmosis น้ำข้างในเลยออกมา เพราะข้างนอกเข้มกว่า ก็เลยเท่ากับว่าเกลือดูดน้ำ

แต่นี่ไม่ได้พูดถึงว่าทำไมหมักเกลือแล้วอร่อย ถ้าแค่นั้นก็แค่น้ำเปลี่ยน สมมติดูดน้ำออกมาแล้วไงต่อ? อีกอย่างความอร่อยไม่ใช่น้ำ (solvent) เราอยากจะให้ความเค็มของเกลือเข้าไปต่างหาก (ซึ่งมาเทียบกับของหมักของเราก็คงมีอะไรคล้ายๆกันด้วย)

การทดลองนี้บอกว่าจริงๆแล้ว เกลือเคลื่อนที่เข้าไปน้อยมากๆแม้จะหมักซะนานเลย กลับกัน เกลือเลื่อนเข้าไป**อย่างจริงจัง**ตอนโดนความร้อนต่ำต่างหากไม่ใช่ตอนหมัก (ดูการทดลองที่แปะกระดาษกรองผสมสารดักเยี่ยวปลาแล้วสีชมพูกว้างขึ้นมากหลัง cook ไฟอ่อนๆ) ซึ่งเกลือเข้าช้าตอนยังไม่ทำอาหารนี่ก็ดีแล้วนะเพราะจะได้ช่วยดึงน้ำไว้แถวนั้น แล้วมันจะป้องกันการ overcook ได้ ทำให้สามารถทำให้ตรงกลางสุกได้สบายใจโดยที่นอกยังไม่ไปซะก่อน แล้วค่อยมาเอารสเค็มเข้าตอนทำอาหาร property นี้ perfect มากเหมือนเกลือเกิดมาเพื่อมาทำแบบนี้เลย กลายเป็นเนื้อรสเกลืออ่อนๆทั้งชิ้นตอนสุกออกมาแล้ว

ซึ่งนี่คือ diffusion ต่างหาก เวลาเกลือโดนน้ำแล้วแตกเป็น charged ion แล้ว มันจะมี random walk ของมัน ไม่มีทิศทาง (เพราะ osmosis ถูกมองว่ามีทิศทาง) แต่ยังไงก็มอง osmosis เป็น form of diffusion ได้ ถ้าคิดว่ามี membrane อยู่แล้วทุกอย่าง random walk แต่ว่าทางนึงแน่นกว่า random ไปมา ก็เลยเกิดความต่างขึ้น (เกลือ random เข้าไป ยากกว่าน้ำ random ออกมา)

One can think of this osmotic pressure barrier as a reduction in the effective diffusion constant, and by averaging over many interconnected cells, still conclude a Gaussian process is an accurate model.

แล้วก็ในเมื่อสูตรแรนดอม Gaussian ใช้ได้ (กับ [Fick's Law](https://en.wikipedia.org/wiki/Fick's_laws_of_diffusion)) ทำให้รู้ว่าการหมักนาน 2 เท่า ไม่ได้ทำให้เจ๋งขึ้นสองเท่า เพราะมัน slow down overtime ดังนั้นเวลาที่ใช้ตอนแรกค่อนข้างคุ้มค่า เวลาหมักน้อย ก็อย่าได้กังวลมาก (อีกอย่าง อย่าลืมมันเอาจริงตอน low heat ตอนแรกเคลื่อนเข้านิดเดียวเอง)

อีกอย่างคือความ hygroscopic ของเกลือ ก็คือ เกลือสามารถ**ยึดน้ำ**ไว้ได้ แต่ไม่ใช่ว่าเกลือมีออร่าที่ดูดน้ำจากรอบๆเข้ามาหาตัว

เวลาโรยเกลือบนเนื้อดิบ สิ่งที่เห็นคือเนื้อจะเป็นมันวาวแปปนึงแล้วก็แห้ง คำอธิบายทั่วๆไปคือก่อนอื่นเกลือดูดน้ำ จากนั้น น้ำเกลือที่ว่าเนื้อจะเกาะไว้ (a**d**sorption) เป็น 2 ขั้นตอน แต่คนนี้บอกว่า

Well, a tiny quantity of juices loosely bound in the meat, as well as humid air near the surface, are hygroscopically absorbed by the salt. A thin slurry results. This layer continues to build until all the salt is dissolved. If there was a pre-exisiting layer of water on the surface, the salt would dissolve faster, but a layer of water is notrequired

Simultaneously, salt is diffusing into the meat, and would do soeven without the surface brine. No osmotic pressure or an "attraction" of water from the meat- the same phenomena occurs on a concrete sidewalk. Eventually, the salt diffuses fully into the meat, and some of the moisture follows along, trapped by the water's polar charge. Most of it simply evaporates. It's not a two-step process, though appears to be so due to the slow rate of dissolving salt crystals

Simply diffusion and hygroscopic surfaces working in parallel.

เป็น hygroscopy กับ diffusion เกิดพร้อมๆกัน

ต่อมาข้างล่างโชคดีมาก มีทดสอบ diffusion ของ MSG ต่อจากเกลือ ซึ่งอย่างที่รู้กันว่าผงชูรสคืออร่อย ดังนั้นถ้ารู้นิสัยมันน่าจะเอามาใช้กับน้ำหมักได้

ในการทดลองนี้ มีขั้นที่เอาออกมาจากน้ำ MSG มาล้างก่อนทดสอบด้วย Ninhydrin คือ การล้างมันไม่ได้ทำลายสิ่งที่เข้าไปข้างในแล้วขนาดนั้น ดังนั้นการหมักแล้วจำเป็นต้องล้างทีหลัง (ในกรณีของเราคือ หมักก่อน แล้วต้มหน่อย แล้วแช่ตู้เย็นต่อ) ก็ไม่ได้ destructive ขนาดนั้น แต่อย่าลืมผลการทดลองของเกลือพบว่าการเคลื่อนที่ส่วนใหญ่เกิดตอน heat ต่ำด้วย แต่ในที่นี้ เอาแค่ซึมเข้าในน้ำ MSG เย็นๆ

ผลคือ MSG ช้ากว่าเกลือ 3x ส่วนน้ำตาลโมเลกุลใหญ่ ช้ากว่าเกลือ 5x - 10x การโรย MSG ก่อนย่าง จริงๆอร่อยแค่ผิวแต่พอกัดเข้าไปแล้วอร่อยเพราะมันนัวในปากจนเหมือนอร่อยมาจากข้างใน จริงๆไม่ใช่ ข้างในที่เดินทางไปถึงอาจจะแค่เกลือ

Time to apply : กลับมาที่ของหมักของเรา ซึ่งประกอบด้วยเกลือ น้ำตาล หรือ MSG ก็ตาม.. สรุปว่า**ผมพลาด! **Sequence ที่ถูกต้องจริงๆคือ หมักตอนดิบก่อน (ตอนนี้ diffuse แถวๆผิว เข้าไปยาก) ทีนี้ถึงขั้นต้มเนื้อให้นุ่มพอดีตามที่อยากแก้ด้วยไฟอ่อน อันนี้มันเป๊ะเลยว่าเป็น condition ที่เกลือจะเดินทางเข้าไปง่ายขึ้น ได้กำไรสองต่อทั้งเนื้อนุ่มทั้งเกลือเดินทางเข้าไป

ความคิดที่ว่า "เนื้อหมักแล้วมาลงน้ำล้างออกเสียเปล่า แง" คือผิด อันนี้จริงๆคือควรทำด้วยซ้ำเพื่อให้เกิดการ diffuse ที่ความเร็วสูงขึ้นจากนิดๆที่ยังขังอยู่แถวผิว

หลังจากพลิกด้านหนังมาต้มจนทิ่มได้ละจะแช่ตู้เย็นต่อ ขั้นนี้จริงๆคิดว่าไม่ต้องหมักอีกช็อตก็ได้มั้งเพราะของที่อยากให้เข้าไปถึงแก่น มันได้เข้าไปแล้วตอนต้ม low heat! ที่ฉลาดสุด น่าจะเก็บน้ำหมักไว้ทาหลังออกจากตู้เย็น เพื่อให้มันไปเคลือบสวยๆในเตาอบต่างหาก (ไม่ได้หวังให้รสเข้า เพราะหวังไปแล้วตอน low heat)

ส่วนเรื่องส่วนผสมของน้ำหมัก คิดว่าของที่เข้ายากๆอย่างน้ำตาล ไม่มีประโยชน์ที่จะหมักตอนแรก แต่เอาไว้ทาทีหลังก่อนเข้าเตาดีกว่า ไม่งั้นเสียของเพราะต้มแล้วก็หลุดหมด ยังไม่ทันวิ่งเข้าไปเลย

แต่ในเมื่อพลาดไปแล้ว เอาไว้รอบต่อไปครับ เผลอต้มก่อนหมักไป

### ออกมาจากตู้เย็นแล้ว ถึงเวลาของ condiments

![](../../assets/2e6ffdedb95e28bc.jpg)

ชิ้นที่ใหญ่กว่านิดนึง จะให้มี baking soda ผสมน้ำค้างอยู่ 30 นาทีก่อนล้างออกด้วยน้ำส้มสายชูให้กลับมาเป็น pH neutral แล้วไม่ทิ้งน้ำส้มสายชูไว้ด้วย เพื่อทดสอบว่าสามารถ denature ให้ผลออกมาต่าง โดยไม่เอารสสบู่ของเบสมาด้วยได้มั้ย

แล้วก็ baking soda นี่มันไม่ค่อยละลายน้ำแฮะ เอาไปอุ่นร้อนแล้วก็เหมือนเดิม.. เอาเท่าที่ได้ละกัน แต่ใส่กรดไม่ได้นะ ไม่งั้นมันจะฟองฟอดแล้วก็เหลือแต่น้ำเปล่าเพราะ CO2 หลุดออกไปได้ อันนี้เราอยากคงความเป็นเบส

### Phase 1

![](../../assets/64b0d15a4ab0cd60.jpg)

![](../../assets/458b3dfc2007b74c.jpg)

- อยู่ๆ ก็กลายเป็นภาพขวาได้ภายใน 30 นาที?? รอบแรกใช้ตั้ง 1 ชม. แล้วก็ อันนี้ชิ้นเล็กกว่ารอบแรกครึ่งนึง หรือว่าชิ้นเล็กลงเท่าไหร่ ก็ใช้เวลาน้อยลงตามไปด้วย ตอนแรกคิดว่าความร้อนลงมาจากข้างบน ทำให้แผ่นใหญ่เล็กแค่ไหนก็โดนเหมือนๆกันตราบเท่าที่พื้นที่ผิวข้างบนมันคือข้างบนซะอีก ถ้าแปรผันตาม volume แบบนี้ก็คล้ายๆไมโครเวฟ
- อันที่โปะโซดา (ซ้าย) ดำช้ากว่า.. อันนี้มั่นใจว่าล้างน้ำส้มละเช็ดแห้งแล้วนะ ไม่แน่ใจว่าเป็นเพราะเบสหรือเป็นเพราะชื้น แต่ที่แน่ๆบางเว็บที่ผ่านมาบอกว่าเบสทำให้ดำ แต่นี่เราล้างออกหมดแล้วเลยไม่มีผลกับความดำมาถึงขั้น cook (เป็นกลางแล้ว) ดังนั้น จะสรุปว่า condiments มีส่วนช่วยให้หนังดำช้าลง ซึ่งดีมั้ย ดีตรงที่ว่าอันนี้มันไวจนน้ำข้างล่างฟอยล์ยังไม่ออกมาเลย ถ้าดำช้าทำให้ให้เวลาน้ำออกมาได้มากขึ้น

### Phase 2

![](../../assets/7305a31465f6a685.jpg)

![](../../assets/2d8b517b59046f8b.jpg)

![](../../assets/4a7c37b6659c7792.jpg)

- ความกรอบออกมาพอๆกัน ถ้าไม่นับความดำที่ carry over มา
- แล้วก็สังเกตุได้ว่า ไอ้ชิ้นที่ดำไปก่อน ตรงขอบที่ดำมากๆ เหมือนจะไม่เหลืองกลับมา จริงอยู่ที่ phase 1 คือการเปลี่ยนจากหนังแดงเป็นดำคล้ำจนน่ากลัว แล้ว phase 2 เอากลับมาเหลืองทองได้ แต่เหมือนมันจะมีจุดนึงที่เลยไปแล้วไม่พองตามที่เห็นในภาพกลาง
- หั่นมากินแล้วแยกไม่ออก 555 แต่พี่คอมเมนต์ว่า อันไม่ soda กินง่ายกว่า?
- น้ำหมักมาถูกทางแล้ว ยกเว้นที่ผิดคิวตอนที่ต้มก่อนหมัก
- แล้วก็ต้มเนื้อที่ใช้น้ำพะโล้ต้ม รู้สึกยังได้กลิ่นใบ bay กับสมุนไพรต่างๆติดมาเป็น aftertaste รู้สึกว่าโอเค วิธีนี้จะเก็บไว้
- โซดา.. ใช้ก็ดีมั้งเพราะมันดำช้าลง แต่ดูฟลุคๆยังไงไม่รู้ 555 อาจจะต้องลองอีกทีว่าไม่ได้เตาเพี้ยน แบบ ทางขวาแรงกว่าซ้าย

![](../../assets/b87e7d945a04a1fe.jpg)

- พี่ซื้อเหล้าส้มกลับมาจากญี่ปุ่น กินเปล่าๆกับแอลกอฮอล อร่อย 555 คราวหลังไม่ต้องต้มมาม่ารอแล้วเอามากินเปล่าๆกับเครื่องดื่มดีกว่า

### สิ่งที่ยังผิด

- ไอ้ 30 นาทีไฟ 1 ที่ต้มไปตอนแรก ออกมาสุดท้าย นุ่มขึ้น นิ้ดดดดดด เดียว ดังนั้น การทดลองต่อไปจะเป็นการหา optimal ต้ม ที่ทำให้พออบ 2 phase ออกมาแล้ว นุ่มพอดี
- ผิดคิวเรื่องหมัก ที่ว่าไป

## To the optimum tenderness

การทดลองครั้งต่อไปนี้ มีจุดประสงค์คือต้มให้นุ่มขนาดไหน ถึงจะอบออกมาแล้วนุ่มพอดี แต่การจะ vary เวลา เพื่อเทียบกันอาจจะกระทบผลไปถึงหนังได้

ดังนั้นเพื่อให้หนังมันเป็นค่าคงที่จะได้เทียบแค่เนื้อ เราจะใช้เทคนิคใหม่ "inverted ต้มตื้น" ก็คือที่ต้มหนังตื้นที่ผ่านมา คว่ำหนังลงละไฟแรงสั้นๆ ทีนี้ **เราจะตั้งหนังขึ้นแล้วให้น้ำท่วมจนเกือบถึงหนัง **แล้วเลี้ยงไฟเบาเหมือนต้มพะโล้ ให้เน้นเวลา เพื่อละลายคอลลาเจนเป็นเจลาตินแทน

![](../../assets/3b1878a788aab110.png)

![](../../assets/b886da65c909cdd3.jpg)

แล้วก็นี่ไปซื้อ thermometer มาแล้ว 100 บาทจากร้านเครื่องเขียน ทนได้ถึง 360 C เพื่อจะได้เปิดแก๊สเบอร์ไหนก็ตามที่ให้อุณหภูมิน้ำ 82-88 ที่เหมาะจะสลายคอลลาเจน แต่ไม่ทำให้เนื้อ tough

แล้วก็เพื่อความมันส์ จะให้มีชิ้นที่เวลาก้าวเข้าเขตพะโล้.. ใช่แล้ว เหมือนตอนแรกที่เราพลาดไปไงล่ะ แต่ครั้งนี้เราจะคุมหนังไว้อย่างดี อยากรู้ว่ามันจะออกมาเป็นยังไง มันจะออกมาเป็น hybrid หมูกรอบมายา ที่ครึ่งล่างพะโล้ครึ่งบนหมูกรอบได้มั้ย**「The Phantasm Crispy Pork」**

### Inverted ต้มตื้น

![](../../assets/32403c38470dcff9.jpg)

หน้าตาเป็นแบบนี้ ว่าจะให้ชิ้นเป็น 30 60 90 120 นาที

แต่! เจออุปสรรคไม่คาดคิด

![](../../assets/f17e200584f0cc69.jpg)

อย่างแรก หมูสามชั้นเกรดอาจจะไม่ค่อยดี บางชิ้นเบี้ยวแล้วคว่ำตั้งไม่ได้ ดูชิ้นล่างสุด หนังโดนน้ำไปบ้างแล้วใสเลย

![](../../assets/666e816c75351ba7.jpg)

![](../../assets/13f139413491f06f.jpg)

อย่างที่สอง เกิดปรากฏการณ์หนังเบี้ยว เนื่องจากต้มแค่เนื้อมันเลยนุ่มแค่เนื้อแล้วหงิกงอแต่หนังไม่ตามไปด้วย.. คราวหลังอาจจะต้องต้มหนังด้วยถ้าอยากได้สวยๆแต่ไม่รู้หนังต้มนานๆจะหายกรอบมั้ยไง ครั้งนี้เลยอยากคุมมันไว้ก่อนแล้วจะดูแค่เนื้อ แล้วก็ถ้าชิ้นเป็นแผ่นใหญ่ๆอาจจะโอเคแต่ที่ห้างมันขายเป็นเส้นๆแบบนี้มันเลยเบี้ยว-prone

ส่วนพิสูจน์ความหลบหนังสำเร็จหรือไม่ก็คือเอาส้อมทิ่ม... โอเคไม่เข้า แสดงว่าเป็น 30 นาทีที่หลบหนังสำเร็จ (จากการทดลองที่ผ่านมาที่เราได้รู้ว่า 3 นาทีไฟแรงต้มตื้นก็ทำให้ทิ่มเข้าได้)

อัน 90 นาทีต้มออกมาเป็นงี้

![](../../assets/87ee2be21c215938.jpg)

สังเกตุเห็นว่าเริ่มเป็นขุยละ นี่คือ border of พะโล้ ถ้าไปไกลกว่านี้สงสัยจะหั่นเป็นเส้นไม่ได้

ส่วนอัน 120 นาที..

![](../../assets/23459ec5c59f2155.jpg)

![](../../assets/590ea270ea874df1.jpg)

![](../../assets/4dab6fcc6828977d.jpg)

เกิดปัญหาคือชิ้นมันไม่สวยอยู่แล้ว ระหว่างต้มทำคว่ำ แถมหนังเลี้ยวลงมาครอบเนื้อ แล้วก็ขนาดต้มหนังแล้วยังจิ้มไม่เข้าเพราะทรงเพี้ยน เลยต้องเอาไปต้มต่อ ตอนต้มต้องจับไว้ไม่งั้นเหลวคว่ำ... เพื่อการทดลองเราจะยังดันทุรังทำพะโล้กรอบนี่ต่อไป

แล้วก็นี่สำคัญ ครั้งนี้เราจะไม่แช่ตู้เย็นเลย มั่นใจกับการต้มหลบหนังมาก จากความรู้ที่เรียนมา ก็แปลว่าตู้เย็นไม่จำเป็นถ้าไม่มีความชื้นเข้าไปอยู่แล้ว (แต่ถ้าแช่ก็คงดีกว่า ยิ่งแห้งยิ่งดี)

### ได้เวลาอบที่ต้ม 30 60 90 120 มา phase 1

![](../../assets/b7400926b212b438.jpg)

![](../../assets/7886998083f46c45.jpg)

ผ่านไป ~45 นาที พบกับสิ่งน่าสนใจ

![](../../assets/1561bc13ca978b45.png)

อันสุดท้ายเป็นอันแถมจากพี่ ที่ต่างกันดังนี้

- ต้มแบบท่วม ไม่แคร์อะไรทั้งนั้น ไฟแรง แต่แปปเดียว
- หนังใช้วิธี score แทนไม่ใช่ส้อมเสียบ
- ไม่ได้แช่ตู้เย็นเหมือนกัน เอามาเข้าเลยพร้อมๆกัน

ภาพนี้สอนอะไรเรา? แปลว่าการที่น้ำโดนหนังตอนต้มเนี่ย **มันมีผลจริงจังมาก **แม้จะเวลาผ่านไปไม่นานก็ตาม 3 ชิ้นแรกถึงเวลาต้มเนื้อจะต่างกัน แต่เวลาลวกหนังพอจิ้มได้ คือ 3 นาทีเท่ากัน ความกรอบออกมาคล้ายๆกัน ชิ้น 120 นาที อย่างที่บอกว่าเนื้อมันเบี้ยวแล้วคว่ำจนหนังจม ทำให้ความชื้นเล็ดเข้าไป (ซึ่งแก้คืนได้ด้วยตู้เย็น แต่นี่ไม่ได้แช่) ส่วนชิ้นสุดท้ายของพี่ที่ต้มไม่แคร์สื่อเลยยังขาวอยู่เลย

พอบอกพี่ว่านี่จบ phase 1 ถึงมโนราห์ state หมดแล้ว แล้วต่อไปจะ phase 2 จะให้อบต่อมั้ย ที่ขาวอยู่เนี่ย พี่บอกว่า เอาไป phase 2 ด้วยกันได้เลย ก็เลยโอเคตามนั้น

### Phase 2

![](../../assets/00abd39fa08666fa.png)

![](../../assets/def6f6238f1b6d97.png)

พบว่าความนุ่มของเนื้อมันตามมาได้จริงๆ หนังที่เป็นตอตะโก อันนั้นพลาดและได้เรียนรู้อะไรใหม่แต่เดี๋ยวค่อยมาบอก รอบนี้เน้นหาความนุ่มของเนื้อที่ดีที่สุด

จากการชิม พบว่า 30 คือเคี้ยวหนึบมาตรฐาน 60 คิดว่านี่แหละรู้สึกนุ่มกำลังดี 90 นี่เริ่มใกล้พะโล้ไปหน่อย กับไม่ชอบความชุ่มกับความขอบขุยๆ ไม่ไหม้สะใจเหมือน 30/60 ส่วน 120... อันนี้เหมือนอาหารต่างดาว หนังกรอบ แต่เนื้อดันเป็นพะโล้ แปลกก็ใช่แต่รู้สึกไม่อยากกินอีกเท่าไหร่ แถมภาพ 120 อีกนิด ดูไปดูมาเหมือนเป็ดย่าง สังเกตุ หนังที่เบี้ยวลงกลายเป็นส่งผลเสียในเตา radiation เพราะ ideally ผิวควรเรียบ

![](../../assets/858aede848988683.jpg)

![](../../assets/cbf5428221dc616a.jpg)

ทีนี้เรื่องความพลาดใน phase 2 คือตำแหน่งแท่งร้อนในเตา ตอนแรกคิดว่าเป็น phase ที่ต้องทำ burst damage เลยคิดว่าตำแหน่งที่อยู่ใกล้แท่งดีที่สุด

![](../../assets/aaa667d88b40d55f.png)

แต่มันร้อนจริงๆ คือร้อนเป็นเส้น 555 ตำแหน่งที่ถูกจริงคือตรงที่ไม่มีแท่งต่างหาก เพราะ gradient ความร้อนแถวนั้น uniform กว่า อยากให้ร้อนก็แค่อบนานขึ้น ดีกว่าเอาไปไว้ใต้แท่ง ถึงพยายามกลางแล้วก็มีติ่งท้ายเลยไปใต้แท่งอยู่ดี สังเกตุว่ามีดำๆอยู่ท้ายชิ้นทุกชิ้น แล้วก็หลักการนี้ใช้กับ upper rack ถ้าเป็นชั้นลงมาคิดว่าอยู่ใต้แท่งให้ร้อนๆก็โอเคไม่เป็นไร

![](../../assets/d1c9594d4981b384.jpg)

เลิกต้มมาม่ามาทำ cocktail กินกับหมูกรอบแล้ว 555 อันนี้คือ Cointreau strawberry ricky (Cointreau + soda + (muddled) strawberry + lime)

## พอก ไม่พอก

สูตรพอกเกลือแล้วแกะก่อนเข้า phase 2 กับไม่พอก เทียบกันเป็นไง

![](../../assets/2f2aa44b8b164308.jpg)

![](../../assets/2b12750a348fc3dd.jpg)

![](../../assets/d4b7ffdfc1f28dcf.jpg)

ใช้ความรู้ทั้งหมดที่ร่ำเรียนมา ต้มหลบหนัง 60 นาทีด้วยความร้อน 82-88 องศา ต้มหนังไฟแรง 3 นาที ทิ่ม ทาน้ำหมักแค่เนื้อ ทาเกลือที่หนัง แช่ตู้เย็นให้แห้ง หลังออกมา เคลือบน้ำหมักที่เผื่อไว้อีกช็อตก่อนเข้าเตา ทา baking soda ยุ่งยากครั้งนี้ไม่ทำ

ที่ต่างคือ อันที่เกลือพอก จะให้อยู่ upper rack ตั้งแต่ต้น (แต่ไฟไม่แรงนะ) ตามสูตรที่คนพอกเกลือบอกใช้ upper rack ตลอดได้ แต่ปัญหาคือเราไม่สามารถ debug ได้ง่ายๆเพราะเกลือบังอยู่มองไม่เห็น สงสัยต้องกำหนดเวลา 1 ชม. แล้ว believe... ว่าแกะออกมาจาก phase 1 แล้วจะอยู่ในมโนราห์ state

![](../../assets/cb27901911a9840f.jpg)

ออกมาจาก phase 1 ..

![](../../assets/19579e2020f3d78f.jpg)

![](../../assets/fb21f922dbf92db9.jpg)

![](../../assets/064c50f326a9892b.jpg)

![](../../assets/87a73caf2aa173b6.jpg)

![](../../assets/fdbd9de552bd16f8.jpg)

มีปัญหาใหญ่ เอาไม่ออก 555555 แต่ช่างแม่ง เข้า phase 2 ดู ส่วนสภาพ ดูมีฟองก็จริงแต่สีค่อนข้างโอเคกว่ารอบอื่นๆ ดูดำน้อย

![](../../assets/db8faa28a0db9619.jpg)

![](../../assets/bcfad3d0fb1d233d.jpg)

![](../../assets/aba9d4940da86974.jpg)

![](../../assets/f8c25b2af7808fca.jpg)

![](../../assets/ed5e080f7b27dbbe.jpg)

หือ! รู้สึกว่าสีสวยที่สุดเท่าที่ทำมาเลย เสียอย่างเดียว กินไม่ได้เพราะล้างเกลือไม่ออก 555 ก็เลยเอาไปล้างน้ำแล้วมากินเหนียวๆแทน เครื่องดื่ม ทำ Countreu strawberry ricky อีกรอบ ครั้งนี้กรองซากสตรอเบอร์รี่ตำออกให้แดงแค่น้ำ ถือว่าดีขึ้น

![](../../assets/6cb3121ff3353ee5.jpg)

## พอกไม่พอก take 2

คราวนี้ไปซื้อเกลือใหญ่ๆมาแล้วจะได้เอาออกได้หมดจด สำหรับคนจะไปหาบ้าง มันคืออันที่ font สีเขียว

![](../../assets/23f4e374c3fd2d92.jpg)

เริ่ม

![](../../assets/9db33db20a34aad7.jpg)

![](../../assets/aac94ae1bd106f45.jpg)

![](../../assets/2443e6064aae7910.jpg)

![](../../assets/040240a87e0af3ff.jpg)

![](../../assets/8732b3426bc255e8.jpg)

ผลออกมาเป็นงี้

![](../../assets/9bae3d09980ba37f.jpg)

![](../../assets/9d433026e2cc9b70.jpg)

การมีเกลืออยู่ทำให้ท้าย phase 1 เราสามารถยั้งไม่ให้ไปถึงขั้นที่มีฟองได้ครับ ซึ่งจะเห็นว่ามีผลตามคือมีความชื้นอยู่ด้วย ควรเช็ดออกก่อนเข้า phase 2 จะมองว่าอันไหนดีกว่า? ผมเห็นว่า ideal มโนราห์ state คือที่พร้อมจะกรอบแต่ยังไม่เลยไปก่อน ดังนั้นคิดว่าถ้าเป็นแบบในภาพนี้แต่อบนานอีกหน่อยก็จะดีที่สุด ก็คือเรียบ แต่เกรียมกว่านี้ นี่ไปต่อไม่ได้เพราะอีกข้างมันจะดำแล้วยังต้องเผื่อไว้ phase 2 อีก ซึ่งความจริง 2 methodology มันไม่ควรมาอยู่บนชิ้นเดียวกัน

แต่เราก็จะดันทุรังทำต่อทั้งๆที่มีสองด้านแบบนี้อยู่ดี เน้นให้ด้านที่มีเกลือดูดีโดยไม่แคร์อีกด้านนึง ต่อไปนี้คือ phase 2 ที่เอาออกมาดูรัวๆแล้วรีบยัดกลับเข้าไป

![](../../assets/067fdb4b2e91993b.jpg)

![](../../assets/b9c1aa82406b4637.jpg)

![](../../assets/25aee0847f196678.jpg)

![](../../assets/2f4dd3a58679ab96.jpg)

![](../../assets/c2c27aa800921d9c.jpg)

![](../../assets/ab561435c9853596.jpg)

อันนี้หลังจากต่อจน overkill อีกนิด

![](../../assets/435b2137ef8179dc.jpg)

ได้ความรู้ใหม่ดังนี้

- การพอกเกลือ
**ไม่ได้ช่วยให้กรอบขึ้น**สังเกตุจากทั้งสองด้าน ได้เดินทางผ่านสภาพที่ฟองดูดีก่อนกลายเป็นไหม้ทั้งคู่ มีสภาพกรอบเท่ากันทั้งคู่ - แต่การพอกเกลือ เพิ่ม potential ในการได้กรอบแบบสวยงาม ไม่มีจุดไหม้ ได้มากขึ้น จากการที่เราออกจาก phase 1 ได้อย่าง consistent กว่านั่นเอง (ออกแบบเป็น "silky skin" ทั้งแผ่นได้โดยไม่มีตรงไหนเลย)
- ซึ่งสิ่งนี้ คือน่าจะที่เกิดขึ้นตอนใช้เกลือผงทำ แล้วออกมาเค็มจนกินไม่ได้อันที่แล้ว อันนั้นเหลืองสวยมาก น่าจะเพราะเรา buffer ตอน phase 1 ไว้ได้นี่แหละ

## แบบเตา Convection

ครั้งนี้เราจะ based on สูตรนี้ ซึ่งตรงกับทฤษฎี 2-phase ที่ค้นคว้ามา แต่เพราะเป็นเตาลมร้อนทำให้นิยาม phase 1 ที่จะเข้ามโนราห์ state ไว้เป็นอบแบบคว่ำหนังลงนั่นเอง เพราะเป็นลมร้อนเลยคิดว่าความร้อนน่าจะม้วนลงมาทำให้หนังแห้งได้พอสมควรไม่เหมือนเตาแท่งแดงแบบโหมดแท่งบน ทำแบบนั้นอาจจะไม่ถึง threshold

### ก่อนจะเริ่ม

อ่านขั้นตอนแล้วลอง apply สิ่งที่เรียนรู้มา

- "แค่ 50 นาที" คือเท่ากับเวลา active time ของที่ทำผ่านๆมาหลังจากออกจากตู้เย็นให้แห้งแล้ว แต่ "แค่" เพราะว่าสูตรนี้ไม่นับเวลาตากแห้ง ที่เป็น inactive time อันนี้คือ 50 นาที cover หมด
- "จขกท. โรยมั่งไม่โรยมั่ง ก็กรอบทุกรอบนะ" ตรงกับที่ว่าไปว่าเกลือไม่ได้ช่วยให้กรอบหรอก ช่วยให้อร่อย ส่วนระดับพอกหนา ช่วยให้ consistent มากกว่า
- "ด้านเนื้อแช่สัก 5 นาที ด้านหนังแค่ชุบแล้วขึ้นเลยค่ะ" อันนี้ตรงกับการทดลองนึงที่ผ่านมา อันที่ต้มเสร็จแล้วเอาไปลุยเลยเหมือนสูตรนี้นี่แหละโดยข้ามตู้เย็น อันที่ต้มไม่หลบหนัง กรอบช้ามาก เพราะความชื้นเข้าไปคาในหนัง
- ข้อที่แล้วสอนอะไรเรา? มันสอนว่าหนังสภาพ neutral ก็ไม่เลวนั่นเอง! คือการแช่ตู้เย็นเหมือนเป็นการ ensure ว่าแห้งมากกว่าหรือเท่ากับ neutral หรือถ้าสายต้มก่อน จะได้แก้ความชื้นกลับมา ถ้าเราหลบตั้งแต่แรก ก็ไม่จำเป็นต้องตากแห้งหรือแช่ตู้เย็น
- คนไทยส่วนมากเชื่อว่าต้อง "ตาก" แห้ง แต่ฝรั่งแทบทุกคนใช้ตู้เย็น อันนี้ยังจริงอยู่ แต่ยังไงสูตรนี้ก็พิสูจน์อีกว่า neutral ไม่ใช้สภาพที่แย่ การแช่ตู้เย็นหรือตากแห้ง ไม่ได้ชี้เป็นชีตายว่าจะกรอบมั้ย ตราบใดเท่าที่เราระวังไม่เติมความชื้นเข้าไป
- Balance ของ 2 phase ในสูตรถือว่าแปลก คือ P1 - 20 นาที P2 - 30 นาที phase 2 นานกว่า phase 1 แต่ที่ทำที่ผ่านมา phase 1 นี่ถึงขั้น 40-50 นาที แต่ phase 2 แค่ 5 นาทีก็กรอบจนจะดำแล้ว เดี๋ยวจะดูว่าทำไม
- 2 phase ไฟแรง 220 องศา
**เท่ากัน**แต่ออมมือโดยการคว่ำหนังลงแทน นับว่า innovative ไม่เห็นสูตรฝรั่งไหนที่ไม่ปรับความแรงไฟ

แต่สูตรนี้ก็ยังมีความไสยศาสตร์อยู่ ซึ่ง proof ได้ง่ายๆแค่แยกทำสองชิ้น แต่เขาไม่ได้ทำแล้วพูดเหมือนเป็น fact

### สิ่งที่สงสัย

- ถ้าไม่ชุบน้ำส้มสายชูกับน้ำปลาแล้วจะเหลืองสวยงามน้อยลงจริงมั้ย หรือมันสวยอยู่แล้ว
- เตาลมร้อนมีจุดแตกต่างกับเตาแท่งอย่างไร

สรุปเราต้องทำ

- คว่ำ หงาย 220 เหมือนกันเด๊ะ แต่อันนึงไม่ชุบน้ำส้มสายชู ให้เห็นชัดๆว่าไสยศาสตร์หรือความจริง

และดูว่าเตาลมร้อนมีอะไรต้องระวังต่างจากเตาแท่งบ้าง

![](../../assets/b18ae7556cce13e9.jpg)

![](../../assets/ffc26eb96a5cf9fb.jpg)

![](../../assets/8ff8bf36dd865bba.jpg)

![](../../assets/770a33451abda4d7.jpg)

ทำพิธี อันนึงในน้ำปลามีน้ำส้มสายชู จุ่มด้านเนื้อ 5 นาที จุ่มหนังแปปเดียวขึ้น แล้วก็ต้มหนังพอเสียบได้ เนื้อไม่แคร์ ไม่แช่ตู้ ลุยเลย (ทดสอบที่ว่า neutral ก็ยังได้)

หลังจากออกจาก P1 เป็นแบบนี้

![](../../assets/b552a7eabfae84fb.jpg)

![](../../assets/00ca31d817cce782.jpg)

![](../../assets/15c9eb3987aad5fb.jpg)

เนื่องจากสูตรนี้ P1 20 / P2 30 มันเลยดูแบบ อืมมม ดิบไปรึเปล่าน้าก่อนเข้า P2 แต่ตามสูตรไปก่อน

![](../../assets/11409fe711650a2e.jpg)

![](../../assets/a7e9bc1f55bfca8e.jpg)

![](../../assets/367fe90dc357931d.jpg)

ออกมาเป็น

![](../../assets/5edc78bdf0ab477b.jpg)

![](../../assets/c75db2c0ae3501be.jpg)

![](../../assets/e4acb4ede805f9fe.jpg)

![](../../assets/28a955d07eea1d67.jpg)

ก่อนอื่น คำตอบของการทดลองคือ **น้ำส้มสายชูไม่เกี่ยว **เหมือนกันเด๊ะ น่าจะความเชื่อล้วนๆ แล้วก็รสเปรี้ยวหายไปด้วย แยกไม่ออกเลยว่าอันไหนใส่ แต่ถ้าชอบเปรี้ยวเอามาจิ้มทีหลังเหมือนกินกับน้ำราดแดงๆ ร้านหมูแดงหมูกรอบดีกว่า

ทีนี้วิจารณ์เรื่องความเตาลมร้อน

- เนื่องจาก P1 P2 อุณหภูมิเท่ากัน แต่ใช้วิธีคว่ำ หงาย ผลที่ได้คือด้านเนื้อค่อนข้างกรอบแห้ง ส่วนด้านหนังกรอบขึ้นแบบไม่ explosive มาก ดูขึ้นมาเป็น linear น่าจะเพราะเตาลมร้อน
- แต่ถึงจะดูฟองไม่สะใจก็เหอะ แต่มันกรอบนะ!
- เนื้อดำสะใจ ทำให้เปลี่ยนรสซอสทั้งหมดได้ จนเข้าไปในหมวด barbeque ได้ ถ้าไม่ใช่ลมร้อนคงจี่ซอสแบบนี้ยากต้องมาคอยพลิกด้าน อันนี้เหมือนมันอบอวลให้เลย
- ถ้าในน้ำหมักที่ทาก่อนอบใส่น้ำตาลนิดหน่อย จะ caramel เป็นรสคล้ายๆกุนเชียง
- ถึงคุมความร้อนยากกว่า แต่คิดว่าเตาลมร้อนมี potential ทำหมูกรอบ perfect ได้มากกว่าเพราะไม่ใช่แค่หนังที่กรอบ เนื้อก็เกรียม

Close up ความเนื้อ (ขอบ) แห้ง ที่เป็นผลมาจากการคว่ำหนังใน P1 ข้างในโอเคชุ่มอยู่

![](../../assets/2a78029c91f3b7b7.jpg)

![](../../assets/df0db179b700ffcd.jpg)

ก่อนจะจบบทความนี้ซะที มีทริคชุดสุดท้ายมาแนะนำ

### หนังต้อง parallel กับความร้อน

อาจจะไม่ obvious แต่ถ้าต้มเนื้อ หรือได้ชิ้นไม่ดี จะพบว่าไม่สามารถตั้งได้ หรือตั้งแล้วชนเพดานล้มลงมา ยิ่งต้องตั้งบนตะแกรงแล้วตะแกรงดันความห่างช่องเท่าเส้นหมู

วิธีแก้คือ จริงๆควรได้ที่เป็นรูปสี่เหลี่ยมจะได้ไม่ล้มและ parallel ชัวร์ แต่ซื้อมาจากห้างส่วนมากจะเป็นเส้นต้องหาวิธีอื่น

![](../../assets/c3b3e430db7db80c.jpg)

- ใช้ส้อมยันไว้ ตอนนี้หนัง parallel แล้ว แต่ข้อเสียใหม่คือ มันจะไม่อยู่ตรงกลาง
- ใช้ foil แล้วพยายามปั้นๆฐานให้มันสามารถวางได้ แต่ก็ยากอยู่

### รูปทรงของความร้อนสำคัญใน P2

เช่น เตาลมร้อนในตัวอย่างนี้ ฝาเป็นรูปวงกลม ใน phase 2 ที่ต้องใช้ความร้อนเร่งให้กรอบในโช๊ะเดียวนี้รูปร่างจะสำคัญมาก ไม่เหมือน phase 1 ที่พออบอวลนัวๆให้แห้งทั่วกันได้

![](../../assets/4ca587ca784741ce.jpg)

![](../../assets/49ed79b23abe8be9.jpg)

จะเห็นว่าฟองแหว่งจริงๆ ซึ่งถ้าไม่ใช่เตา convection แต่เป็นเตาแท่ง มันจะแท่งเหมือนแท่งหมูได้เลยก็เลยไม่มีปัญหา อันนี้ตรงกลางที่มันควรอยู่โดนส้อมเอาไปละ

คิดว่า.. เราทดลอง และ myth busting กันเยอะพอสมควรจนหายสงสัยแล้ว! หมูกรอบไม่ใช่เวทย์มนต์อีกต่อไป ไม่ใช่ว่าเพราะมึงไม่ตากแห้ง ลืมเสียบ ลืมน้ำส้มสายชู เลยไม่กรอบไง อีกต่อไปแล้ว เราสามารถ debug แล้ว fix ได้ ถ้าอะไร มันอะไรเกินไปหรือถ้าอะไร มันยังอะไรไม่พอ no more หลับหูหลับตา

![](../../assets/d9358336fc399aa6.jpg)

ไหนๆก็ภาพปิดท้าย แต่งสีนิดหน่อย 555 ขอบคุณที่ติดตามกันมาจนจบครับ วันจบการทดลอง 20/08/2019 หนึ่งเดือนจากตอนเริ่มบทความพอดี..