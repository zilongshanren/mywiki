---
title: 'UE4 UMG UUserWidget: Which fires first, NativePreConstruct or Blueprint PreConstruct?'
url: https://allarsblog.com/2020/01/29/ue4-umg-uuserwidget-which-fires-first-native_preconstruct-or-blueprint-preconstruct/
author: Michael Allar
published: '2020-01-29'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

Short answer, NativePreConstruct fires first. NativePreConstruct then fires Blueprint PreConstruct.

Practical answer and probably why you googled what you googled to arrive at this page:

`UUserWidget::NativePreConstruct`

directly calls `UUserWidget::PreConstruct`

which means if you follow the common paradigm of calling Super when overriding `NativePreConstruct`

:

```
function UThing::NativePreConstruct()
{
// Typical to call Super first, this invokes the Blueprint PreConstruct
Super::NativePreConstruct();
//Do stuff here
Blah();
Blah();
Blah();
}
```


What will happen is the Blueprint `PreConstruct`

of your Widget will get called before the meat of your `NativePreConstruct`

implementation. Something you should keep in mind. You can freely do the following to reverse the order:

```
function UThing::NativePreConstruct()
{
//Do stuff here
Blah();
Blah();
Blah();
//Then call Super, which will then call the Blueprint PreConstruct
Super::NativePreConstruct();
}
```


This will ensure that your User Widget's Blueprint `PreConstruct`

runs after the meat of your `NativePreConstruct`

.

Now this may have been incredibly obvious to most people, but not explicitly knowing this caused me a slight enough annoyance to write a blog post about it.