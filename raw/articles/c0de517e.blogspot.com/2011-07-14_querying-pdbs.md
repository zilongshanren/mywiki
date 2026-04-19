---
title: Querying PDBs
url: https://c0de517e.blogspot.com/2011/07/querying-pdbs.html
published: '2011-07-14'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

We're in the final stages of our game and this means that almost everyone is chasing and fixing crashes, often debugging retail builds from core dumps, having to deal with nasty problems most times without much aid from the debugger.

Sometimes you're just looking at the memory, trying to identify structures: executable regions, virtual tables, floats and so on. From there you might hope to recover the type of the variable you're looking in memory and today we got an email from people trying to do exactly that, chasing a structure from some sparse hints.

So I thought, how cool would it be if we could execute queries on the debug symbols to find such things!

Well it turns out it's really, really easy. One great tool that does something similar is

Well it turns out it's really, really easy. One great tool that does something similar is

[SymbolSort](http://gameangst.com/?p=320), and it's written in C#, and it comes with sourcecode! Cool!SymbolSort queries the PDB for global data symbols, here we are interested in global user defined types and their subtypes, it's a pretty similar thing. Also, Microsoft provides a

[Debugging Interface](http://msdn.microsoft.com/en-us/library/x93ctkx8.aspx)wrapped in a COM dll that does pretty much all you need, and it's trivial to call from C# or similar.Of course debugging is only a small fraction of what you can do with PDBs, so this is really just an example to show how easy it is, from here you can do many nifty things like code-generating reflection,



Disclaimer: I wrote this in half an hour. It's probably

In fact the test program I did is a bit more complex and complete than the one I posted here, that is a stripped down version that fits the blog better and IMHO is a better starting point. Also if you really plan to chase structures with this, keep in mind that this version does not recursively search into member structures and inherited stuff.



P.S. It turned out that this particular bug was caused by bad memory (the actual memory in the hardware - it happens quite often) so this exercise was ultimately useless :)

*cross-referencing with profile captures to do coverage analysis*or serialization modules and so on.Disclaimer: I wrote this in half an hour. It's probably

*wrong*and surely ugly. Play with it but don't trust it! It's just meant as an example of how easy it is to query PDBs via msdia.In fact the test program I did is a bit more complex and complete than the one I posted here, that is a stripped down version that fits the blog better and IMHO is a better starting point. Also if you really plan to chase structures with this, keep in mind that this version does not recursively search into member structures and inherited stuff.

P.S. It turned out that this particular bug was caused by bad memory (the actual memory in the hardware - it happens quite often) so this exercise was ultimately useless :)

using System;

using System.Collections.Generic;

using Dia2Lib; // we need a reference to msdia90.dll in the project

namespace Test

{

class Program

{

private static void GetSymbols(IDiaSymbol root, List< IDiaSymbol> symbols, SymTagEnum symTag)

{

{

IDiaEnumSymbols enumSymbols;

root.findChildren(symTag, null, 0, out enumSymbols);

uint numSymbols = (uint)enumSymbols.count;

for (;;)

{

uint numFetched = 1;

IDiaSymbol diaSymbol;

enumSymbols.Next(numFetched, out diaSymbol, out numFetched);

if (diaSymbol == null || numFetched < 1)

break;

symbols.Add(diaSymbol);

}

}

}

private static bool IsMemberPointer(IDiaSymbol s) // Quick'n'dirty based on observation of 1 (one) pointer, I'm sure there are better ways

{

return ((s.type != null) &&

(s.type.name == null) &&

(s.type.type != null) &&

(s.type.type.name != null)

);

}

private static bool IsMemberPrimitive(IDiaSymbol s, ulong length) // I'm not entirely sure about this one too :)

{

return ((s.type == null) && s.length == length);

}

private static bool SymbolPredicate(IDiaSymbol s)

{ // see the IDiaSymbol documentation here: http://msdn.microsoft.com/en-us/library/w0edf0x4.aspx

// It's around this size...

if (!((s.length > 62) && (s.length < 67)))

return false;

List< IDiaSymbol> childSymbols = new List< IDiaSymbol>(); // Note: from what I've seen the symbols are arranges in the order they appear in the class/structure

GetSymbols(s, childSymbols, Dia2Lib.SymTagEnum.SymTagData); // TagData will get us all the member variables, TagNull will get us everything

// It has to have sub-symbols (fields)

if (childSymbols.Count == 0)

return false;

// One has to be a matrix

bool hasMatrix = false;

foreach (IDiaSymbol subS in childSymbols)

if ((subS.offset < 8) && // It should be one of the first members in memory

(subS.type != null) && // It's not a primitive type, so its type has to be a symbol

(subS.type.name != null) &&

(subS.type.name.ToLower().Contains("matrix4"))

)

hasMatrix = true;

if (!hasMatrix) return false;

// Another one is a pointer to a matrix...

bool hasPointer = false;

for (Int32 i = 0; i < childSymbols.Count; i++)

{

IDiaSymbol subS = childSymbols[i];

if (IsMemberPointer(subS)

&& (subS.type.type.name.ToLower().Contains("matrix4"))

)

{ //...followed by a 4 bytes integer

if (i < childSymbols.Count - 2)

if (IsMemberPrimitive(childSymbols[i + 1], 4))

hasPointer = true;

}

}

if (!hasPointer) return false;

return true;

}

static void Main(string[] args)

{

DiaSourceClass diaSource = new DiaSourceClass();

diaSource.loadDataFromPdb("game360_release.pdb");

//diaSource.loadDataForExe(filename, searchPath, null);

IDiaSession diaSession;

diaSource.openSession(out diaSession);

IDiaSymbol globalScope = diaSession.globalScope;

List< IDiaSymbol> globalSymbols = new List< IDiaSymbol>();

GetSymbols(globalScope, globalSymbols, Dia2Lib.SymTagEnum.SymTagUDT /* user defined type! */);

List< IDiaSymbol> matchingSymbols = globalSymbols.FindAll(SymbolPredicate);

foreach (IDiaSymbol s in matchingSymbols)

{

if(s.name!=null)

System.Console.WriteLine(s.name);

}

}

}

}

## 5 comments:

It's funny - I did this exact thing ~half a year ago, but with good results (i.e. I found the bug this way).


http://hg.zeuxcg.org/misc/src/0882342219e2/tools/pdbscan.fs

(my solution is more verbose because it flattens everything to primitive types to get all possible results for the stomp pattern, making no assumptions (i.e. three consecutive floats I was looking for could be a vector, but could be just floats; the int32 could be a enum or an int, and int8 could be an int8 or a bool. The effort paid off :))

F#, cool! I actually wanted to experiment with wrapping the PDB to be usable in Linq expressions. Maybe in the future I will. I also want to make it more C++ friendly (in terms of understanding how C++ types are encoded in the PDB). I'll have a look at your code more in detail later. Thanks for posting it!

Does PDB stands for Parameter Database?

Thank you man :-D! You are my here; exactly what I was looking for!! God bless ya :)

Post a Comment