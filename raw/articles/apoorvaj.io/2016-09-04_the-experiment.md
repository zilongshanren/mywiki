---
title: The experiment
url: https://apoorvaj.io/exploring-calling-conventions
published: '2016-09-04'
source_blog: apoorvaj.io
source_site: https://apoorvaj.io/
category: graphics
fetched: '2026-04-13'
---

When I was in the process of creating the OpenGL loader that I
described in my [last blog
post](https://apoorvaj.io/@/loading-opengl-without-glew.md), I forgot to add the WINAPI prefix to the function
declarations. Someone pointed out to me on Twitter that the code would
fail on 32-bit compilation. I checked, and it did. Addition of the
`WINAPI`

macro fixed this problem. The `WINAPI`

macro expands to `__stdcall`

on 32-bit compilation on
Windows.

I had encountered `stdcall`

and more of these mysterious
keywords in the past, but only had a vague idea of what they did. And so
I did some web research, dumped some assembly files, and studied a
three-way diff. What follows is an analysis of `cdecl`

,
`stdcall`

and `fastcall`

, and how assembly code
differs between these three calling conventions.

I wrote a small C program:

I compiled the program and generated the assembly using the command
`gcc -S -m32 main.c`

. I did this three times, changing the
value of `__attribute__`

to `cdecl`

,
`stdcall`

, and `fastcall`

respectively. Then I
diffed the results.

![](../../assets/57fd79ea620bd57e.png)


You can find the output text [here](https://gist.github.com/ApoorvaJ/7942dde540712eebb6ad76d7cf251957).

Let’s have a look at the interesting parts of the generated assembly programs:

Let’s have a look at the `cdecl`

assembly, starting from
the `main:`

block. In the stack diagrams that follow, memory
addresses decrease as you go down. Thus, in the diagrams below, stacks
grow downward.

The `ebp`

register stores the base pointer, which is the
base of the stack for the given stack frame. This pointer keeps pointing
to the same location for the lifetime of that stack frame. The
`esp`

register stores the stack pointer. This pointer moves
as the stack grows and shrinks. These two lines of code create a new
stack frame. `pushl %ebp`

pushes the previous value of
`ebp`

on the stack, and the `movl %esp, %ebp`

moves `ebp`

such that both now point at the same
location.

While returning from a function, you’ll do a `popl %ebp`

or a `leave`

to restore the value of the previous stack
frame.

A value of 16 is subtracted from `esp`

. Note that this is
the stack growing downward, and conceptually, `esp`

always
denotes the top of the stack.

The two parameters - 88 and 99 - are pushed onto the stack. This is
because the `cdecl`

calling convention doesn’t allow the use
of registers for passing parameters. 4 bytes are allocated per parameter
because they are ints. The amount of stack space allocated doesn’t
necessarily equate to the sizes of the parameters. Extra space may be
added for alignment purposes.

Now, the function `foo`

is called. It executes and
returns. Then, we execute an `addl`

instruction to increment
`esp`

, which shrinks the stack. This instruction cleans up
the stack growth that happened when we pushed the two parameters to the
stack. This is because in `cdecl`

, the caller is responsible
for the cleanup.

The assembly for the `stdcall`

variant is identical to the
`cdecl`

variant, except that in this variant, the callee is
responsible for stack cleanup. As a result, the `addl`

instruction in the main function used for cleanup is absent, and the
`ret`

instruction in the `foo`

function is now
`ret $8`

.

The code here is substantially different, since `fastcall`

allows us to pass parameters through the `ecx`

and
`edx`

registers. The parameters are now stored in registers
instead of pushing them on the stack. Note that `fastcall`

only allows us to use these two registers. If more parameters need to be
passed, they spill over into the stack.

Although this code shows up as a substantial diff as compared to the
previous variants, it is (unsurprisingly) functionally similar. It
manually allocates stack space by decrementing `esp`

. Then it
moves the `ecx`

and `edx`

values on to the stack,
based on addresses relative to `ebp`

. Then it proceeds with
the same logic the other variants.

Addresses are different here because the parameters now belong to a different stack frame, than in the previous variants.

To summarize, calling conventions dictate how parameters are passed to functions, and who is in charge of the cleanup. These are the results we found:

| Convention | Cleanup responsibility | Parameter-passing |
|---|---|---|
`cdecl` |
caller | stack |
`stdcall` |
callee | stack |
`fastcall` |
callee | `%ecx` , `%edx` ,
stack |

Fortunately, in 64-bit compilation, there aren’t as many variants of calling conventions, and things seem to be a bit more sane. As a result, the specifics of the calling conventions investigated above may not be extremely valuable in a modern execution environment. However, this does give us an insight into the mechanics of parameter-passing and stack allocation and cleanup, which should be relevant even today.

If you would like to study this in more detail, Agner Fog has written
a [really
good document](http://www.agner.org/optimize/calling_conventions.pdf) on the topic.