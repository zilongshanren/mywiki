---
title: Confessions of a Lisp Hater
url: http://hacksoflife.blogspot.com/2012/02/i-hate-to-admit-this-but-sometimes-i.html
author: Benjamin Supnik
published: '2012-02-27'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I hate to admit this, but sometimes I find myself missing python. For example, the other day, I wrote this horrible mess^H^H^H^H^H^Hbeautiful example of templated C++:



What makes the above code particularly ugly isn't just, um, that mess, but the other shoe - the UnlinkedFace_p predicate is several lines of boiler plate for about one expression of useful C++:



What makes this function so verbose is that the "closure" - that is, the act of copying the locally scoped data "into" the predicate object has to be done by hand for every predicate we write, and the predicate can't be located in the function where it really belongs. (At least, if I try to locate my struct inline, GCC becomes quite cross. There may be fine print to get me closer to predicates inline with the code.)


In Python this would be a lot more pleasant. There's no typing, so strip out all of that type-declaring goo, and we have real closures, so the entire function chain can be written as one nested set of calls that contain pretty much only the good bits.


This got me thinking about the difference between coding in C and Python. Here comes another stupid coding quote:



`CollectionVisitor<Pmwx,Face_handle,UnlinkedFace_p> face_collector(&friends, UnlinkedFace_p(&io_faces));`

VisitAdjacentFaces<Pmwx, CollectionVisitor<Pmwx,Face_handle,UnlinkedFace_p> >(*f, face_collector);


Once you start writing really well-factored C++ template functions, eventually you'll reach this point: the verbosity of code is dominated by having to write a ton of function objects because C++ doesn't have closures. (Yes, closures. No one is more [pained to admit envy of a Lisp feature](http://hacksoflife.blogspot.com/2010/12/lisp-isnt-language.html)than me.)What makes the above code particularly ugly isn't just, um, that mess, but the other shoe - the UnlinkedFace_p predicate is several lines of boiler plate for about one expression of useful C++:

`struct UnlinkedFace_p {`

set<Face_handle> * universe_;

UnlinkedFace_p(set<Face_handle> * universe) : universe_(universe) { }

bool operator()(Face_handle who) const {

return universe_->count(who) > 0;

}

};


(Note: I am trying to get the less than and greater than symbols manually converted so Blogger doesn't delete 3/4 of my templated code like it has in the past.)What makes this function so verbose is that the "closure" - that is, the act of copying the locally scoped data "into" the predicate object has to be done by hand for every predicate we write, and the predicate can't be located in the function where it really belongs. (At least, if I try to locate my struct inline, GCC becomes quite cross. There may be fine print to get me closer to predicates inline with the code.)

In Python this would be a lot more pleasant. There's no typing, so strip out all of that type-declaring goo, and we have real closures, so the entire function chain can be written as one nested set of calls that contain pretty much only the good bits.

This got me thinking about the difference between coding in C and Python. Here comes another stupid coding quote:

Coding in C is like going out to dinner with someone who's really cheap and insists on discussing the price of everything on the menu. "You know, that pointer dereference includes a memory access - 12 to 200 cycles. That ? involves conditional code, you might mis-predict the branch. That function is virtual - you're going to have two dependent memory fetches." You know the cost of everything on the menu.

Coding in Python is like going on a shopping spree with your friend's credit card. "Go ahead, iterate through a list of lists, and insert in the middle. If it feels right, just do it. No, it's not expensive, why do you ask?"

Does Boost.Lambda or the Blocks concept help? I suppose not Blocks if you have to build with MSVC++

ReplyDeleteBlocks (or GCC closures) would totally help if they were ubiquitous; we're looking at compiler migration so maybe someday they will be.



ReplyDeleteBoost.lambda I think is a cure worse than the disease...C++ nerds (like myself) like to point out that the language "can" do just about anything a higher level language can via custom data types. But...from a practical productivity standpoint it's not the same.

Here's the test I think:

* I code in C++ all day and program python by googling web examples, and I can get real work done in Python.

* If a professional python programmer googles code snippets, will they be able to rapidly put together useful programs using Boost.Lambda? :-)

C++11 has perfectly good^W^W serviceable^W closures. Much nicer than Boost.Lambda at least.

ReplyDeleteAgreeing with Alex's comment, C++11's support for closures, std::function<>, as well as the 'auto' keyword (and std::shared_ptr<>, for that matter) have drastically changed the code I write for the better. C++11 can still get ugly at times, but it's a major, language-changing step forward. Both gcc and MSVC support all these features (you may need the -std=c++0x flag depending on which version of gcc you're using).

ReplyDelete