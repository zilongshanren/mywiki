---
title: Upload/Download ของใน AWS S3 ต้องมี IAM Policies อะไรบ้าง
url: https://gametorrahod.com/upload-download-aws-iam-policies/
author: Sirawat Pitaksarit
published: '2016-12-12'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/44d4b5ee4e23ed35.png)

หลังจากลองผิดลองถูกมาหลายรอบใน Unity AWS Plugin ก็พอเข้าใจ Error ต่างๆ

โค้ดที่แสดง Error คือนี่

```
client.GetObjectAsync(bucket, s3path, (responseObj) =>
{
if(responseObj.Exception == null)
{
var response = responseObj.Response;
if (response.ResponseStream != null)
{
...
}
}
else
{
Debug.LogError(“S3 Exception!”);
Debug.LogError(responseObj.Exception.Message);
}
});
```


ก่อนอื่นจะบอกว่า

`Debug.Log(responseObj.Response.HttpStatusCode.ToString());`


อันนี้ตอน Error ใช้แล้วไม่ขึ้นอะไรเลย แถมมันทำให้ callback ไม่ดำเนินต่อไปข้างหน้าด้วย งง แต่ใน Tutorial ของ Amazon บอกเหมือนใช้แสดงเออเร่อเป็นภาษาคนได้ พอลองจริงๆ มัน null ตั้งแต่ responseObj.Response แล้ว ก็เลยเอาออกไป

เออเร่อแรก

`Exception of type ‘Amazon.Runtime.Internal.HttpErrorResponseException’ was thrown.`


อันนี้ ใน client (IAmazonS3) ตั้ง Region ผิดประเทศ ไม่ตรงกับ bucket ที่จะเอามา พอตั้งถูกแล้วเจอเออเร่อต่อไป

`Access Denied`


อันนี้แปลว่า Policy ใน IAM ไม่ตรง จากการลองผิดลองถูกพบว่าอันนี้ใช้ได้

```
{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Action": [
"s3:Put*",
"s3:Get*"
],
"Resource": [
"arn:aws:s3:::duelotterssavestorage/*"
]
},
{
"Effect": "Allow",
"Action": [
"s3:List*"
],
"Resource": [
"arn:aws:s3:::duelotterssavestorage"
]
}
]
}
```


Point คือ! ถ้าเอา List ของ bucket **เฉยๆ (ไม่มี /*) **ออกแล้วมันจะ Access Denied เพราะเหมือนว่าการ Get ไฟล์มา มันต้อง list ไฟล์ก่อน? น่าจะเป็นแบบนั้น แล้วก็ของ List ห้ามเติม /* เพราะว่าเป็นการกระทำกับ bucket ไม่ใช่กับไฟล์ข้างใน

ส่วน Put กับ Get เป็นของไฟล์ข้างใน เราจึงต้องให้ Policy กับของข้างใน (/*) ไม่ใช้กับ bucket

เอามารวมๆแบบนี้ก็ได้เหมือนกัน แต่มันมักง่ายไปหน่อย แล้วก็ทำให้ไม่เข้าใจอย่างแท้จริงว่าอะไรเป็นอะไร

```
{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Action": [
"s3:Put*",
"s3:Get*",
"s3:List*"
],
"Resource": [
"arn:aws:s3:::duelotterssavestorage/*",
"arn:aws:s3:::duelotterssavestorage"
]
}
]
}
```


ทีนี้เออเร่อกลายเป็น

`The specified key does not exist.`


อันนี้แสดงว่ามาถูกทางแล้ว แต่ชื่อไฟล์ไม่ตรง อย่าลืมว่าไฟล์ใน S3 จริงๆแล้วไม่มี folder structure เก็บเป็น linear หมด ชื่อ folder จริงๆแล้วก็เป็นชื่อไฟล์ ดังนั้น ชื่อไฟล์ผิด ก็อาจแปลว่าชื่อโฟลเดอร์ผิดด้วย ซึ่งถ้าใส่ให้ถูก มันก็จะเรียก Get ของได้แล้ว เย้

ส่วนการ Upload (Put/POST) น่าแปลกใจที่ตอนนึง client ผิด Region ก็อัพโหลดสำเร็จ สงสัยเพราะการใช้ POST ใน Unity มันต่างจาก Get/Put โดยตรง อาจจะมีการบริการทำ region ให้ถูกต้องให้เราอยู่เบื้องหลัง (Unity ใช้ Put โดยตรงไม่ได้ ต้องพึ่ง HTTP POST)

จาก Policy ที่เห็นนั้น ก็ทำระบบ Save Backup สำเร็จจนได้ (คือ POST ขึ้นไปเป็น backup ส่วน Get ลงมาก็แค่ต้องรู้ชื่อไฟล์ที่ถูก)