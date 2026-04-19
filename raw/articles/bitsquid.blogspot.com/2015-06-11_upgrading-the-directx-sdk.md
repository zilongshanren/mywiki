---
title: Upgrading the DirectX SDK
url: https://bitsquid.blogspot.com/2015/06/when-i-joined-bitsquid-month-ago.html
author: Amandine Coget
published: '2015-06-11'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

## Step 1: Explore

First stop: MSDN's article. I had heard that the DirectX SDK was now included in the Windows SDK, but I wasn't sure what that covered.[This article](https://msdn.microsoft.com/en-us/library/windows/desktop/ee663275%28v=vs.85%29.aspx)sums it up. With a teammate, we went through the whole list, figuring out what we were and were not using. In the end, the only problematic components were XInput, XAudio2, and D3DX9Mesh. The bulk of the codebase had already been converted away from using D3DX, which was great!

However another thing needed clearing up. Our minspec is still Windows 7. How was that going to work? Luckily, MSDN had the answer again.

[This article](http://blogs.msdn.com/b/chuckw/archive/2012/11/14/directx-11-1-and-windows-7.aspx)reveals that the Windows 8.X SDK is available on Windows 7. This is covered in more details on

[this page](http://blogs.msdn.com/b/chuckw/archive/2012/08/22/directx-sdk-s-of-a-certain-age.aspx)and

[that page](http://blogs.msdn.com/b/chuckw/archive/2013/10/03/a-brief-history-of-windows-sdks.aspx).

## Step 2: Well let's just try then

I changed the paths in our project generation files to the Windows SDK. I also added the June 2010 SDK, but only for XAudio2 and D3DX9Mesh (more on XInput further down). After fixing only a few compile errors, things seemed mostly fine... until I got a runtime crash about ID3D11ShaderReflection. Huh?##
Step 3: GUIDs and the magic `#define`


I had wrongly assumed that the link errors I had been seeing when changing the paths were caused by DX9, because I read too fast.
Linking with the old dxguid.lib made the errors go away, so I didn't think about it more.
However, a large part of DirectX relies on GUIDs, unique hardcoded identifiers.
When debugging, I noticed that IID_ID3D11ShaderReflection had the wrong value compared to the Windows SDK header,
which was causing the crash.
I went on a goose hunt for what was somehow changing this value,
and wasted a day to looking for a wrongly included file.But by default, those GUIDs are

`extern`

variables, and will get their values from lib files.
And I was linking with an old one.
Mystery solved!
I removed dxguid.lib from the linker, but that of course caused the GUIDs to be undefined.
The solution for that is to `#define INITGUID`

before including windows.h.
Thanks to the Ogre3D forums for pointing me towards
[the relevant support page](https://support.microsoft.com/en-us/kb/130869), since they encountered the same issue before. At this point everything was fine, except that it was failing on the build machines.

## Step 4: d3dcompiler

The first error had been around for a long time. We had so far, unknowingly, relied on the d3dcompiler DLL being present in System32! Since System32 is part of the default DLL search path, this is easy to overlook, especially when the DirectX SDK is a required install anyway. We were now relying on a more recent version, supposed to be included in the Windows SDK. Yet still it was failing... because we did not have a proper installation step. I tweaked the project files again, adding a copy step for that DLL. CI, however, was still failing.## Step 5: XInput

XInput comes in several versions in the Windows SDK. 1.4 is the most recent one as I'm writing this, and is Windows 8-only. To use XInput on Windows 7, you need to use version 9.1.0. For that, ensure that[the magic](https://msdn.microsoft.com/en-us/library/windows/desktop/aa383745%28v=vs.85%29.aspx#setting_winver_or__win32_winnt)is set to the proper value (see further up on the page). You also need to explicitly link with XInput9_1_0.lib and not XInput.lib, or Windows 7 will get a runtime crash trying to fetch XInput1_4.dll, which doesn't exist on Windows 7. In my case this was breaking the automated tests on a Windows 7 machine, but was completely fine on my Windows 8 workstation.

`_WIN32_WINNT #define`

## Step 6: Profit?

As far as I can tell this should be the end of it, but the rendering team has yet to stress-test it. We'll see what breaks as they poke around :)Hopefully this can save you some time if you're doing a similar upgrade, or convince you to give it a try if you've been holding back.

[Cross-posted from personal blog]

That's a great post, thanks! I've been planning to upgrade my project to new SDK but always been afraid of that. Now I know how to do it!

ReplyDeleteExcellent information Providing by your Article, thank you for taking the time to share with us such a nice article. Amazing insight you have on this, it’s nice to find a website that details so much information about different artists.


ReplyDeletewho want to download and install WhatsApp Plus Apk on their Smart Phone, and then it's important that they use for installation. Yes, it will use up at any time when installing this application.This application also has a cool and new theme and supports more than 100 languages.

Broadcast messages: You can also send broadcast messages to up to 600 people at the same time.

Thanks for the guide. Yellowstone Coat

ReplyDeletegoogle 1765

ReplyDeletegoogle 1766

google 1767

google 1768

google 1769

Our team of world-class experts is ready to answer all your questions and concerns 7 days a week. We love helping our clients ValidCBDOil learn more about CBD products and how they can fit into your life. Most people have heard of a cannabinoid called THC, which is the compound in cannabis that gets users high. Unlike THC, CBD is non-intoxicating and does not cause a high.

ReplyDeleteamazing website, this is really some good quality content. loved the way you explained through words keep writing the best article


ReplyDeleteKilling Eve Diego Jacket

You have performed a great job on this article. It’s very precise and highly qualitative. You have even managed to make it readable and easy to read. You have some real writing talent. Thank you so much. สล็อตออนไลน์

ReplyDeleteI am very happy to discover your post as it will become on top in my collection of favorite blogs to visit. สล็อตแตกง่าย

ReplyDeletei love reading this article so beautiful!!great job! เว็บสล็อตเว็บตรง

ReplyDeleteThanks for taking the time to discuss this, I feel strongly that love and read more on this topic. If possible, such as gain knowledge, would you mind updating your blog with additional information? It is very useful for me. เกมสล็อต

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteA crucial first step in enhancing compatibility, performance, and access to more recent development capabilities is updating the DirectX SDK. Careful updates contribute to a more seamless and effective workflow, much as thesis editors who improve and strengthen academic work. Developers who want to keep projects up to date will find this topic very helpful.

ReplyDelete