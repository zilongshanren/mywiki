---
title: Tumblr Fail
url: https://claire-blackshaw.com/blog/2010/06/tumblr-fail/
author: Claire Blackshaw
published: '2010-06-01'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Tumblr Fail](../../assets/4e402aebc4c1a4e8.png)

### Tumblr Fail

So I wrote this long article about how I switched to an Atomic data model.

How this is **one possible implementation** of the proposed model. Different code would be written based on language, memory and cpu restrictions. The implementation is a **proof of concept**. It does **not define the model**.

### Atomic Model

The atomic model uses a damage protocal. It stores a value and the time that value was set.

- Testing point before any atom returns unkown.
- Testing between or at an atom returns last value change
- Testing past last atom return last known value

### Blind Spot & Discovery

This system means if a value change occurs and then is changed back before an agent observes it again then they are unaware of event. If however the observed value is different to the last known value then they agent knows an event has occurred and can inquire or investigate.

Anyway I got to run and catch the bus, sorry for short version.