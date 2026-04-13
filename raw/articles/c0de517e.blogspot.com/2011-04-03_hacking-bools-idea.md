---
title: Hacking bools idea
url: http://c0de517e.blogspot.com/2011/04/hacking-bools-idea.html
published: '2011-04-03'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Little idea. After reading

[this post](http://msinilo.pl/blog/?p=757)about bools, chars and bitfields, I started thinking of an ugly c++ hack.What if we defined our own custom bool (chances are that you already have one around in your engine, if not it's probably not a good idea to add one) that it behaves like a bool (char sized or whatever) always, but it strictly stores only 0 or 1?

With such a thing we could make sure when returning a native bool out of it, that what we store is still either 0 or 1 and thus have a mean to identify some memory stomps in many classes that have boolean members, for free.

Of course this "idea" could be extended, via templates, to have ranged integers and so on, but that would start being really ugly...

## 2 comments:

Something like :






struct sHeavyBool

{

explicit sHeavyBool(const int t_) : t(t_) {};

explicit sHeavyBool(const unsigned int t_) : t(t_) {};

sHeavyBool(const bool t_) : t(t_) {};

explicit sHeavyBool(const char t_) : t(t_) {};

sHeavyBool() {};

sHeavyBool(const sHeavyBool & t_) : t(t_.GetValue()){}

sHeavyBool & operator=(const sHeavyBool & rhs)

{

t = rhs.GetValue();

return *this;

}

sHeavyBool & operator=(const int t_)

{

t = (t_ == 0)?false:true;

return *this;

}

operator const bool & () const { bool t2 = GetValue(); return t; }

operator bool & () { bool t2 = GetValue(); return t; }

bool operator==(const sHeavyBool & rhs) const { return GetValue() == rhs.GetValue(); }

bool operator==(const bool & t_) const { return GetValue() == t_; }

bool operator<(const sHeavyBool & rhs) const { return GetValue() < rhs.GetValue(); }

bool GetValue() const

{

#ifdef _DEBUG

if((t != true)&&(t != false))

{

if( (explicitChar == 0xCD) || (explicitChar == 0xCC) )

{

assert( "Boolean not initialized" && false );

}

else

{

assert( "Boolean initialized strangely" && false );

}

}

#endif

return t;

}

protected:

union

{

bool t;

unsigned char explicitChar;

};

};

and then typedef your own bool to sHeavyBool ?

I'd love to see class injection, replacing bool and int as you say. These would be handy:



int8_t x = 255 + 1; // Assert int8_t has overflowed!

void* p = GetPointer();

if (p) // Assert, pointer is not convertable to bool (Have to use p != nullptr)

Post a Comment