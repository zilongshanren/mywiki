---
title: Static Hash Values
url: https://bitsquid.blogspot.com/2010/10/static-hash-values.html
author: Niklas
published: '2010-10-01'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

At a number of places in the code we want to check these hashes against predefined values. For example, we may want to check if a certain object is the "root_point". With a straight forward implementation, you get code that looks like this:

const char *root_point_str = "root_point"; static unsigned root_point_id = murmur_hash(root_point_str, strlen(root_point_str), 0); if (object.name() == root_point_id) ...We use a static variable to avoid having to hash the string more than once, but this is still pretty inefficient. There is the extra application data, the computation of the hash the first time the function is run. On subsequent invocations there is still the check to see if the static variable has been initialized.

It would be a lot more efficient if we could precompute the hashes somehow to avoid that cost in the runtime. I can see three ways:

- We could run a code generation pass in a pre-build step that generates the hash values and patches the code with them.
- We could use the preprocessor to generate the values.
- We could compute the values offline and hard-code them in the code.

Rewriting the murmur hash algorithm in the preprocessor requires me to bring out some serious preprocessor-fu. But it is fun. It is almost like functional programming: With these lovely macros in place, we can now write:

if (object.name() == HASH_STR_10('r','o','o','t','_','p','o','i','n','t')) ...Having completed this task I feel a bit empty. That is certainly a lot of macro code for an end result that still is kind of meh.

I disregarded hard coding the values to begin with because no one wants to look at code like this:

if (object.name() == 0x5e43bd96) ...Even dressed up in comments, it is still kind of scary:

unsigned root_point_id = 0x5e43bd96; // hash of "root_point" if (object.name() == root_point_id) ...What if someone types in the wrong value? What if we decide to change hash algorithm at some later point? Scary. But maybe we can ameliorate those fears:

#ifdef _DEBUG inline unsigned static_hash(const char *s, unsigned value) { assert( murmur_hash(s, strlen(s), 0) == value ); return value; } #else #define static_hash(s,v) (v) #end ... if (object.name() == static_hash("root_point", 0x5e43bd96) ...That looks better and is completely safe. If something goes wrong, the assert will trigger in the debug builds.

I think I like this better than the preprocessor solution. It will make the debug builds run a bit slower, but that's what debug builds are for, right?

What we do here at keen games is that we have .crc files (text files with one identifier in each line) that run through a ruby script in our maketool (before the compilation starts). This script creates a header file with defines for each symbol in the crc file and the hash (crc32 in our case) value as value. That worked like a charm for all our projects.


ReplyDeleteRegards

Julien

Perhaps you could still put the values themselves into a single file as a define.. at least then the values are in one place, which is useful just in case the hash generation code is changed.

ReplyDeleteWe went with pre-parsing somewhere along the lines of what Julien mentioned. Instead of storing the output in a separate file we just modify the source file in place.









ReplyDeleteWhat we do is to place every string in a macro like this:

H("hello", 0)

Which gets replaced with the appropriate hash in the second parameter. So immediately after the pre-parser has run on the code file it would look like this:

H("hello", 0x263262)

The nice thing is that you only ever need to run the parser on a file that has been modified. The bad thing is that it depends on how well your build system supports modifying a file during a build.

An alternative would have been to make people manually run the parser and then just have a validation process in our continuous integration server that checks all the macros to make sure the numbers are correct.

I dislike relying on a debug build to find mismatches because it assumes that you'll get full code coverage when you are running the build and that is very hard to achieve.

An alternative I have played with is to use template meta-programming to compute the hash. It works but relies on the compiler to remove all unused code which I also don't like to rely on. Something along the lines of what Humus mentions on his blog (http://www.humus.name/index.php?page=News&ID=296)

I've worked with few various systems for that in the past, one I liked the most was pre-parser (almost identical to the one Phil mentioned).

ReplyDeleteProblem with template meta-programming is that usually result is still not a true compile-time constant (even if there is no runtime calculations involved), so it cannot be used in switch/case construct for example. (Mainly because "hello"[0] is not compile time).

Phil: I expect mismatches to be rare and to also crash the release build (with a not-as-nice error message). So I'm not so worried about mismatches. The debug check is more of a belt-and-suspenders thing.




ReplyDeleteIt is also nice to have all hashes tagged with the static_hash() because it makes them easy to find, if that is needed for some reason.

(I could run a pre-parser script on the code, looking for static_hash() and thus get the behavior you are talking about.)

With templates I worry both about compile times and whether all different compilers will actually compile the code down to a single int. That's why I went with a preprocessor solution instead. (Though compile times may be an issue there as well.)

Indeed. Your static_hash function is essentially the same as our H(). Both are easily processed or verified by an external program.

ReplyDeleteUsing sizeof() on a string literal gives you the length of the string+1 for the zero terminator. I believe it's also compile-time constant for all compilers (unlike strlen).





ReplyDeleteIgnoring compile time issues with templates, I mocked up this templated version of murmurhash just for the exercise:

https://docs.google.com/leaf?id=0B9ZOSR6WRNMmZjU2OWE5MmUtMjlhNy00MzA4LTg1ZjEtN2Y1NWU5ZmYxNjk2&sort=name&layout=list&num=50

Compiling with VS2008 shows static_murmurhash("your_string_literal_here") collapses to a 32-bit immediate, although sadly you still can't use this in a switch statement for the same reasons that MaciejS says. ("hello"[0] not considered constant in the case statement)

caveat emptor: do not accidentally use static_murmurhash with a non-literal string. It'll only hash the first 3 bytes of the string. I'm sure you'll figure out why :)

Nice! Then everyone can just pick and choose the solution they found best.



ReplyDeleteBut that Google Docs link doesn't work for me. I get:

"Sorry, the page (or document) you have requested is not available."

Can't access the google docs link either :/ I know this can be implemented properly using C++0x string literals tho.





ReplyDeleteYou could also run the hasing during the variable during static initialization.

int root_point_id = murmurhash("rootpoint");

void foo() {

if (object.name() == root_point_id)

...

}

You still pay a runtime penalty of course but do not have to pay for the runtime branch check to see if a function level static variable is initialized. And you also avoid mismatches between runtime/static hashing algorithms.

This comment has been removed by the author.

ReplyDeleteI've uploaded another one, and it's fully public now so should be accessible:



ReplyDeletehttps://docs.google.com/leaf?id=0B9ZOSR6WRNMmNDI4MjBkYjYtYTY2Ny00MjAwLWE3YTMtMTUwZTFlOWNmZTk1

FWIW, I'm actually seeing VS2005 compile static_murmurhash *and* dynamic_murmurhash down to an immediate if used with a string literal in release builds. The static version is therefore unlikely to be used due to the downsides when it is accidentally used with a non-literal string.

Hi, could you include a licence to the two google doc links?

DeleteJohan: It's an option, but I'm not too fond of static initializers, in fact in the Bitsquid engine we avoid them completely. The reason is not only the static initialization order fiasco, but also the fact that they are tricky to instrument and profile, when you are in the business of minimizing your startup times.

ReplyDelete@Justin Oh, that's just what Humus does then:



ReplyDeletehttp://www.humus.name/index.php?page=News&ID=296

As I think you noticed, you are not really using templates for compile time evaluation, you are just relying on the optimizer to fold the constant expressions. Note that the compiler will only do that up to certain string length. After 23 characters or so it will start invoking the function at runtime. You can increase that threshold a bit using forceinline, though.

Agreed, though It looks like Humus approaches it by manually and explicitly overloading functions, while the templated version takes care of that in the implementation that I've mocked up :)





ReplyDelete@ignacio. Yeah the templates just massage it into a form that minimizes coder work by not defining all the different flavors of hashes corresponding to string lengths manually.

FYI, if you use the inline_depth pragma in MSVC with __forceinline, you can push the threshold out a lot. With these, VS2008 is folding the strings up to 108 characters (probably more, but I didn't test further). I just __forceinlined the templated versions and surround the templated function definitions by

#pragma inline_depth(255)

.. and:

#pragma inline_depth() // restore default

But wow, it takes an age to compile this module - on the order of 30 seconds when evaluating a series of 108 hashes on strings of length 1,2,3,..108 in length. This definitely supports the template compile-time = problem argument, but may or may not be workable within your projects scope and may well not be a problem if you structure your code to minimize changes to the module these hashes are included in.

Also, with this in mind, I double checked, and a non-templated recursive version of the function (that uses branches to determine how to call itself recursively) doesn't fold beyond 4 character strings - even with __forceinline and #pragma inline_depth.

Does anyone know the state of support for the "constexpr" (in C++0x) in current (e.g VS2010) compilers? And user-defined literals, for that matter. Those strike me as something that might help in cases such as this.



ReplyDeleteI used to do stuff like this with template meta-programming, but found out (on some larger projects) you'd get some horrible compile times and run into many compiler limits (compiler heap, recursion depth, etc.) and eventually abandoned the whole thing. Now I just use a combination of calculate-by-hand-and-assert-at-runtime, and just-calculate-at-runtime-and-avoid-the-headache methods!

Very instructive blog by the way, specially for someone like me with little experience.

I made a constexpr version:


ReplyDeletehttps://gist.github.com/mattyclarkson/5318077

The article I saw was interesting because of the introduction. As I was looking forward to seeing the count of upcoming posts, showing your plan to continue sharing such great stuff, I'm glad to see you. Visit my latest post on How to Get Better at Using a Mouse. It will be a pleasure to visit Computer Mouse Tips. Thanks for your concern.


ReplyDeleteslot joker


ReplyDeleteสล็อตออนไลน์ ที่เป็นเกมออนไลน์ยอดฮิต อยู่ตอนนี้ และ พันธุ์ทิพย์ เป็นแหล่งข้อมูลที่ คนถามถึง เว็บสล็อต slotjoker นั้นมีสูตรลับสำหรับ เล่นสล็อตแตกบ่อย และ โดยปกติผู้ดูแลเว็บไซต์ จะลบมันออก ทำให้หาข้อมูลเกี่ยวกับ สล็อตค่ายไหนดี pantip ค่อนข้างยาก แต่ก็ไม่ได้ยากขนาดนั้น เราพร้อมแนะนำ ผู้เดิมพันเสมอ ผู้เดิมพันส่วนใหญ่ มักจะมองหาข้อมูล เกี่ยวกับสล็อตออนไลน์ เช่น ปั่นสล็อตค่ายไหนดี slotjoker-spd

มั่นคง และ ปลอดภัย ซึ่งสล็อตนั้นดี โบนัสมักจะใช้ไม่ได้ หรือแคมป์สล็อตนั้นแตกง่าย สิ่งนี้สามารถเพิ่มโอกาส ในการได้รับรายได้ ผู้เล่นบ่อยขึ้น แต่อย่างไรก็ตาม จุดเด่นสล็อตออนไลน์ คือการออกโบนัสจำนวนมาก รางวัลใหญ่ถูกจับฉลาก โดยเฉพาะถ้าคุณรู้วิธีเล่นสล็อต

¡Tu aliento significa mucho! Vea este perfil test de la edad mental para más noticias. Descubre tu edad mental con este intrigante test.

ReplyDeleteBelmont Wears transforms wardrobe essentials into powerful style statements.

ReplyDeleteEffortless sophistication made for today’s trend-conscious generation.