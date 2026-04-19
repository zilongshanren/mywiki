---
title: BitSquid C++ Coding Style
url: https://bitsquid.blogspot.com/2010/12/bitsquid-c-coding-style.html
author: Niklas
published: '2010-12-16'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

I agree with everything but the underscores for variable and function names. I find camel case easier to read than underscores.

That said, I definitely feel it IS something that I feel should be specified. I'd rather read and code underscores than have a mix anywhere in the code.

Lastly, the one place I feel a piece of "hungarian-esq" notation works is notating an argument to a function: my_func(int a_argument1, int a_argument2) { // code body }

Though this might harm the type of readability you're looking for, it differentiates arguments from local variables and can help someone scanning the code figure out where the variable came from easily, especially in longer functions (e.g. whether it's a calculated value local to the function or passed in).

I haven't felt the need to distinguish arguments, to me they don't seem "special enough" and I like to keep the functions short. Actually I'm not so sure on the hungarian notation on member variables either. It might be clearer to just write this-> everywhere... it's a bit more typing though... and harder to enforce. But all of this is a matter of taste anyway.

When I sit and code in visual studio, i think its nice for example to write m_ and then press ctrl-space to get all member variables. Or for example to write class.get and press ctrl-space to get all the getters from the class. Thats one big reason I think to write m_ before members and get before get functions.

I was refering to this excellent post from time to time, but unfortunately, the link pointing to the coding style stopped working. Is it available anywhere else?

This is a great article, with lots of information in it, These types of articles interest users in your site. Please continue to share more interesting articles! Quickbooks contact helps you with everything regarding QuickBooks software. If you are stuck in some general issues related to QuickBooks like installation error or payroll issues then we are here to help you anytime you want.

yes c++ is a language. it is used to create a programs. it's most common application used in nowadays. windows spotlight quiz is also made by this language

I was surfing net and fortunately came across this site and found very interesting stuff here. Its really fun to read. I enjoyed a lot. Thanks for sharing this wonderful information. norton.com/setup norton.com/setup

Microsoft excel is very widely used application by small or large organizations. XLSX viewer tool is the best rated free Excel file reader to open, edit various different types of spreadsheets files. It is a type of xls file extension that used to various mathematical models. For more information, you may visit.

I am Jackson Levi From Australia . I am So Glad to see your post. You did a great job in this post. It was very helpful for me. Thank you for sharing this Blog. Netflix Phone Number Australia +61480-020-996 is the one-stop solution to all your Netflix-related problems. If Netflix itself can’t resolve your problem, our exclusive services are the most reliable toll-free number in the industry. Where certified experts make things easier and resolve problems instantly our technical team resolves all problems related to Netflix. It happens due to a wide variety of reasons. You can take help from technical support on the support team to resolve buffering issues.It affects your work and business which totally depends on the internet. We are open 24*7 to assist you regarding streaming problems and non-technical issues after fixing the problem watch your favourite channels on Netflix .

Almost the same as the Google C++ style guide (http://google-styleguide.googlecode.com/svn/trunk/cppguide.xml),which I use and love ;).

ReplyDeleteI agree with everything but the underscores for variable and function names. I find camel case easier to read than underscores.




ReplyDeleteThat said, I definitely feel it IS something that I feel should be specified. I'd rather read and code underscores than have a mix anywhere in the code.

Lastly, the one place I feel a piece of "hungarian-esq" notation works is notating an argument to a function:

my_func(int a_argument1, int a_argument2)

{

// code body

}

Though this might harm the type of readability you're looking for, it differentiates arguments from local variables and can help someone scanning the code figure out where the variable came from easily, especially in longer functions (e.g. whether it's a calculated value local to the function or passed in).

I-actually-like-dashes-best,-but-unfortunately-that's-not-valid-C++. Underscores_are_the_next_best_thing_because_what_you_write_is_still_quite_readable. CamelCaseIFindNotVeryReadableAtAll,ButIGuessYouCanGetUsedToIt.


ReplyDeleteI haven't felt the need to distinguish arguments, to me they don't seem "special enough" and I like to keep the functions short. Actually I'm not so sure on the hungarian notation on member variables either. It might be clearer to just write this-> everywhere... it's a bit more typing though... and harder to enforce. But all of this is a matter of taste anyway.

When I sit and code in visual studio, i think its nice for example to write m_ and then press ctrl-space to get all member variables. Or for example to write class.get and press ctrl-space to get all the getters from the class. Thats one big reason I think to write m_ before members and get before get functions.

ReplyDeleteI was refering to this excellent post from time to time, but unfortunately, the link pointing to the coding style stopped working. Is it available anywhere else?

ReplyDeleteThanks for noticing, I've found a new home here:


Deletehttps://github.com/niklasfrykholm/blog/blob/master/reference/coding-style.md

شركة مكافحة حشرات بالمدينة المنورة


ReplyDeleteشركة تنظيف بالمدينة المنورة

This is a great article, with lots of information in it, These types of articles interest users in your site. Please continue to share more interesting articles!


ReplyDeleteQuickbooks contact helps you with everything regarding QuickBooks software. If you are stuck in some general issues related to QuickBooks like installation error or payroll issues then we are here to help you anytime you want.

yes c++ is a language. it is used to create a programs. it's most common application used in nowadays.

ReplyDeletewindows spotlight quiz is also made by this language

I was surfing net and fortunately came across this site and found very interesting stuff here. Its really fun to read. I enjoyed a lot. Thanks for sharing this wonderful information.


ReplyDeletenorton.com/setup

norton.com/setup

I will be looking forward to your next post. Thank you

ReplyDeleteเมย์ พิชญ์นาฏ สวยแซ่บบบเวอร์ จนน้ำทะเลจืด อวดหุ่นเอวบาง

Great to see your blog.. https://odindownloads.net

ReplyDeleteSamsung odin

ReplyDeleteGreat efforts to collect the information.


ReplyDeleteonline game

office setup

fun games

Microsoft excel is very widely used application by small or large organizations. XLSX viewer tool is the best rated free Excel file reader to open, edit various different types of spreadsheets files. It is a type of xls file extension that used to various mathematical models. For more information, you may visit.

ReplyDeleteI am Jackson Levi From Australia . I am So Glad to see your post. You did a great job in this post. It was very helpful for me. Thank you for sharing this Blog. Netflix Phone Number Australia +61480-020-996 is the one-stop solution to all your Netflix-related problems. If Netflix itself can’t resolve your problem, our exclusive services are the most reliable toll-free number in the industry. Where certified experts make things easier and resolve problems instantly our technical team resolves all problems related to Netflix. It happens due to a wide variety of reasons. You can take help from technical support on the support team to resolve buffering issues.It affects your work and business which totally depends on the internet. We are open 24*7 to assist you regarding streaming problems and non-technical issues after fixing the problem watch your favourite channels on Netflix .


ReplyDeleteThis was so informative, thank you for sharing!

ReplyDelete