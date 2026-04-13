---
title: Dual Quaternions
url: http://gameenginebook.blogspot.com/2012/01/dual-quaternions.html
author: Jqgregory
published: '2012-01-05'
source_blog: Game Engine Architecture
source_site: http://gameenginebook.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Selected email conversations, errata and announcements regarding "Game Engine Architecture" by Jason Gregory

Thursday, January 5, 2012

Dual Quaternions

Hello, I've been reading through Game EngineArchitecture, and must commend you on an excellent book. I'm a lead-programmer with just over 10 years experience making games, so I'm not directly in the target audience, but I've still found it a very interesting read. I just wish it had existed a few years earlier! Anyway, the section on Dual Quaternions was something that interested me - I hadn't heard of them before, and the possibility of representing rotation, translation and scale in 8 floating point numbers sounded useful - to good to be true really! However, having skimmed through the cited .pdf file, I can find no mention of them representing scale, and this resource http://isg.cs.tcd.ie/kavanl/papers/sdq-tog08.pdfsuggests also that they cannot represent scale. Quote: "Dual quaternions cannot represent non-rigid transformations, such as scale and shear. This means that dual quaternion skinning, unlike linear blend skinning, is restricted only to rotating and/or translating joints." Anyway, thought I'd mention it. If I've misunderstood them and scale is possible, then apologies. If not, then perhaps a section for corrections on the website would be useful. Kind Regards, Andy Weinkove.

____________

Hi Andy,

You are quite right, that is an error. Dual quats represent a combined rotation and translation... basically a "screw motion" and are incapable of describing any kind of scaling transform.

Although there is a relatively simple method to add scale to dual quaternion skinning. See the authors website here: http://isg.cs.tcd.ie/projects/DualQuaternions/

Although there is a relatively simple method to add scale to dual quaternion skinning. See the authors website here: http://isg.cs.tcd.ie/projects/DualQuaternions/

ReplyDelete