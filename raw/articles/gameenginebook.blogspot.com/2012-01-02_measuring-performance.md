---
title: Measuring Performance
url: http://gameenginebook.blogspot.com/2012/01/from-kechi-cheng-date-762010-hi-i-am.html
author: Jqgregory
published: '2012-01-02'
source_blog: Game Engine Architecture
source_site: http://gameenginebook.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**From: Kechi Cheng**

**Date: 7/6/2010**

Hi,

I am reader of Game Engine Architecture. But I feel confused in chapter 7.5.4.3 that talk about 32-Bit Floating-Point Clocks.

You say the time deltas in floating point format, measured in unit of second. But I don’t understand why you multiply the duration of

CPU Cycles by CPU’s clock frequency. I just think the duration of CPU Cycles should be divided by CPU’s clock frequency. I try to use

WIN32 API to test the result, and the test code like:

// Just test

LARGE_INTEGER dwTest;

QueryPerformanceFrequency(& dwTest);

LARGE_INTEGER dwTest1;

QueryPerformanceCounter(& dwTest1);

Sleep(1000);

LARGE_INTEGER dwTest2;

QueryPerformanceCounter(& dwTest2);

float fHiTimer = (float) (dwTest2.QuadPart - dwTest1.QuadPart) / (float) dwTest.QuadPart;

// Just test

The result is correct, so could you tell me why you multiply by CPU’s clock frequency?

Thanks

Kechi Cheng.______________________________________________

You are correct, that's a typographical error. A duration measured in cycles divided by frequency in cycles/second (or multiplied by the inverse frequency, in seconds/cycle) will equal seconds.

Cheers,

J

## No comments:

## Post a Comment