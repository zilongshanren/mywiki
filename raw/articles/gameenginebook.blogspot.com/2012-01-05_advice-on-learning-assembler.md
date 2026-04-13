---
title: Advice on Learning Assembler
url: http://gameenginebook.blogspot.com/2012/01/advice-on-learning-assembler.html
author: Jqgregory
published: '2012-01-05'
source_blog: Game Engine Architecture
source_site: http://gameenginebook.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Selected email conversations, errata and announcements regarding "Game Engine Architecture" by Jason Gregory

Thursday, January 5, 2012

Advice on Learning Assembler

From:Thomas Amundsen

Hi Jason,

I was introduced to your book “Game Engine Architecture” through CSCI 522: Game Engine Development at USC. First, I’d like to say that it is a GREAT book, and can’t thank you enough for writing it!

The biggest question I had after working through the some of the chapters and then reading your blog is, how do you go about learning assembler? I majored in computer science during my undergrad, so I spent about half of a semester learning assembler for some fake architecture. But that didn’t transfer over to the real world, and whenever I see the disassembly in Visual Studio, I have no idea what’s going on. So, I think it would help me a lot to learn this stuff. Do you have any book recommendations, or other general recommendations?

Thanks so much!

- Tom

____________________

Hi Tom,

The best way to learn assembler is to pick a CPU that you have access to (the Intel Pentium or P6 family are probably the most accessible, since they live in most PCs and the latest Macs as well). Then pick up a book on the Intel P6 ISA (instruction setarchitecture), and try coding something!

One way (a not very friendly way, mind you) is to grab the actual Intel docs and pour through them. You could start here: http://download.intel.com/design/PentiumII/manuals/24400101.pdf and then move on to the manuals that describe the actual instructions etc.

But really that gives you too much detail. What you want is to learn the basic concepts of registers, aritmetic/logic units (ALU), and assembly instructions... then start learning the basic instructions and what they do. I don't know of a book offhand that teaches this, but here are a few ideas I found on Amazon:

You could also go old-school and learn the way I did, by reading about a much older... and therefore much simpler... CPU. For example, the 6502 -- the CPU in the old Apple // computers. It is very simple, and therefore a great way to learn the concepts without getting bogged down in details and modern optimizations. Here's one:

## No comments:

## Post a Comment