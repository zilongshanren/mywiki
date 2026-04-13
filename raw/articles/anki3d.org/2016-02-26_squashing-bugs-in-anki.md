---
title: Squashing bugs in AnKi
url: https://anki3d.org/squashing-bugs-in-anki/
author: Panagiotis Christopoulos Charitos
published: '2016-02-26'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

There are some universally accepted truths in software and one of those truths is that all software has bugs. Some people are more careful than others but nobody is perfect and nobody can write 100% bug free code. Another truth is that hunting bugs is rarely a fun job. It shifts the focus and sometimes it forces a mental context switch (graphics guys know that context switches can be slow). I always considered AnKi as a playground. A codebase where I can experiment, learn and have fun. Since the inception of AnKi I knew that bugs and debugging in general will spoil that fun so I had to find a way to have a robust codebase so I can focus on the fun parts. I think to some degree I’ve managed to avoid the endless pains of debugging by using the tricks I’ll describe in the following lines.

The first and, in my opinion, the most powerful tool against bugs is the almighty assertions. AnKi has a ton of assertions. To put it into perspective, there are 852 assertions throughout the code and it’s roughly **1 assertion every 84.8 lines** of code. Some subsystems like util (AnKi’s equivalent of STL) have to be extremely robust so this particular subsystem has 1 assertion every 37 lines of code. In practice AnKi almost never segfaults when assertions are enabled. In the majority of cases an assertion is triggered and finding out what’s wrong is a mater of minutes.

Another thing I’ve tried early on and improved over the years is based on the idea that the **commonly used subsystems have to be as robust as possible**. One of these subsystems is util (contains a list, something like std::vector, hashmap, memory management, strings and other). Util is a widely used subsystem and it’s extremely important to be reliable. As I mentioned earlier, util is rigged with assertions. On top of that there are quite a few **unit and performance tests**. So unit tests is another weapon against bugs. In AnKi’s case unit testing is not that excessive but they cover some commonly used cases.

AnKi loves wrappers. To protect against common mistakes there are some **wrappers that have debug capabilities**. One example is anki::Array (something like std::array). anki::Array wraps constant size arrays and it asserts on out of bounds access (unlike std::array). Also, there is SArray that is constructed using a pointer to some memory and a size. SArray will also assert on out of bounds assess. These wrappers, and more, ensure that stupid mistakes will be caught.

The last weapon is the excellent **valgrind** and more precisely valgrind’s memcheck tool. Once and a white I run a demo on top of valgrind just to make sure that everything is in order. There were some occasions where all of the above methods failed but valgrind found the culprit. Unfortunately in complex workloads valgrind can be quite slow.

Of course C++ bugs are not the only source of bugs. Half of the bugs in AnKi are graphical glitches and rendering problems. Graphics related bugs heavily depend on the GPU and the driver and debugging those can be painful. Spending a whole week debugging can be kind of painful. There are some tools that help graphics related problems but those will not be covered by this article.

To sum up, what worked for AnKi is tons of assertions, robust core subsystems, some unit testing and quality code.

That’s all for now.