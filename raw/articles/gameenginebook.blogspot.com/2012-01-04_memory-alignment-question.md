---
title: Memory Alignment Question
url: http://gameenginebook.blogspot.com/2012/01/memory-alignment-question.html
author: Jqgregory
published: '2012-01-04'
source_blog: Game Engine Architecture
source_site: http://gameenginebook.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**From:**Justin Lam

Hi Jason,

Thank you for writing such a wonderful book, I throughly enjoyed Game

Engine Architecture.

I was wondering if you can clarify something for me. I'm trying to understand the code for allocating aligned memory on pages 212-213. The part that I'm having trouble understanding is how you store the adjustment value. You mentioned that the smallest adjustment value is

1 byte, how then can you subtract 4 bytes from the alignedAddress. Wouldn't this put your pointer pass the rawAddress and you're overwriting some memory that is not yours? Can you clarify or elaborate how this works?

Your response is greatly appreciated.

Thanks,

Justin

____________________________________________

Hi Justin,

Thanks for the kind words about the book!

Re your question: you first allocate a block of raw memory (that is not necessarily aligned) that is

*larger*than the requested block size. The number of additional bytes is equal to the requested alignment in bytes. When you get the raw block back, you advance the pointer until it is aligned (by at least one byte, and by at most the number of bytes in the requested alignment). That way, you always have at least one additional byte in which to store the adjustment value.

For example, let's say the requested alignment is 4 bytes, and the requested size is 64 bytes. We'd actually allocate 64+4=68 bytes. If the raw address we get back is

*already*aligned to a 4-byte boundary (e.g. 0x2000), then we advance the pointer by a full 4 bytes, store our adjustment value in the byte just prior to that (0x2003), and then return the adjusted pointer (0x2004). But if the raw address is

*not*already aligned (e.g. worst case 0x2003), then we would adjust the pointer until it is aligned (0x2004) which would still give us one byte (0x2003) in which to store the adjustment.

J

Hi there! I can clearly see that you undoubtedly understand what you are speaking about here. Do you own a degree or maybe an education which is somehow associated with the subject of your article? Can't wait to see your reply.

ReplyDelete