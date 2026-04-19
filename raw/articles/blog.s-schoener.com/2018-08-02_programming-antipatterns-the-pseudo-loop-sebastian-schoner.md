---
title: Programming Antipatterns - The Pseudo-Loop | Sebastian Schöner
url: https://blog.s-schoener.com/2018-08-02-antipattern-pseudo-loop/
author: Sebastian Schöner
published: '2018-08-02'
source_blog: Hi there! | Sebastian Schöner
source_site: https://blog.s-schoener.com/
category: graphics
fetched: '2026-04-19'
---

Here is a piece of Go code:

```
for i, x := range xs {
if x == target {
doThingsWithX(i, x)
return true
}
}
return false
```


If you are wondering what `i, x := range xs`

means, know that it goes over the list `xs`

, binding `i`

to the index and `x`

to the content. Just think `enumerate`

if you know some Python.

This style of loop is what I would call a *pseudo-loop*: It has the form of the loop, but a good part of the loop body will execute at most once: `doThingsWithX(i, x)`

. This example may not seem so bad because I actually had the good taste to put the processing in its own function. There are plenty of cases where the original author did not, like this one that I just found:

```
for i, worker := range workplace.Workers {
if worker == targetID {
workplace.Workers = append(workplace.Workers[:i], workplace.Workers[i+1:]...)
workplaceHan.pool.Workplace.Update(workplace)
worker.Workplace = ecs.InvalidEntityID
worker.CurrentAssignedJob = components.InvalidWorkerJob
worker.Blocked = false
workplaceHan.pool.Worker.Update(worker)
if npc, ok := workplaceHan.pool.NPC.TryGet(targetID); ok {
npc.FailState = components.NPCFailStateNoWorkplace
npc.FailStateParams = npc.FailStateParams[0:0]
workplaceHan.pool.NPC.Update(npc)
}
return
}
}
```


Most of the body of the loop will again execute at most once. When reasoning about programs or just reading this, I find this quite irritating. It unnecessarily complicates matters. You have a wall-of-code in a loop, but it will never, well, *loop*! What a waste.

I would much rather write the code like this (maybe with an inverted check to reduce nesting, but that is a matter of test - and scope, as it turns out):

```
if i, ok := IndexOf(xs, x); ok {
doThingsWithX(i, x)
return true
}
return false
```


Here, you don’t pretend that the actual meat of your code will run in a loop. You do what has to be done in the loop and remove the rest from it.

Unfortunately, because this is Go and Go does not have generics or templates, you will have to define the `IndexOf`

function for each and every type separately, all with new names etc. I can totally understand that you would not want to do that initially, but in the long run it is definitely worth it. If you have not caught onto it [yet](https://blog.s-schoener.com/2018-07-29-go-problem/), I’m absolutely not a fan of how Go facilitates bad coding practices…