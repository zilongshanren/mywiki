---
title: Wolfram's Mathematica 101
url: http://c0de517e.blogspot.com/2013/10/wolframs-mathematica-101.html
published: '2013-10-06'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

After a lengthy preamble, I'll try to explain the language in the


This will appear in a shorter form also on

[http://learnxinyminutes.com/](http://learnxinyminutes.com/)style, so you might prefer to skip down to the last section.This will appear in a shorter form also on

[AltDevBlogADay](http://www.altdevblogaday.com/2013/10/07/wolframs-mathematica-101/)


**- Introduction**

I've been using Wolfram's Mathematica since my days in university. I wasn't immediately sold as initially I saw it as a computer algebra system and preferred Maple's more math-friendly syntax for that, but with time it became a great tool in my arsenal of languages.

The way I see Mathematica fit in today's rendering engineer (or game developer in general) work is that of a data analysis tool, mostly. We increasingly have to deal with data, either acquired (e.g. measured BRDFs) or simulated (e.g. integrals of the rendering equation), get "a sense" of it, compare it with our realtime rendering models, and try to derive the right approximations for the sea of things we still can't directly solve.

What makes Mathematica good for this job, a better tool than say C++, are a few key features: it's an interactive, exploratory environment, it has strong visualization and manipulation abilities, it has a rich library providing almost everything you could think of, it's a concise language, and it has a great community (see

[http://mathematica.stackexchange.com/](http://mathematica.stackexchange.com/)and[http://www.wolfram.com/broadcast/video.php?channel=311](http://www.wolfram.com/broadcast/video.php?channel=311)) and great documentation.
Two notes, before looking at the language. First, you might notice that on the technical level there are alternatives that can compete. We want a prototyping language, with lots of libraries, an interactive shell, solid visualization abilities…

[Python](https://store.continuum.io/cshop/anaconda/)fits the bill as well, most probably[Matlab](http://www.mathworks.com/products/matlab/)and a number of its clones ([Scilab](http://www.scilab.org/),[Octave](http://www.gnu.org/software/octave/)),[Maple](http://www.maplesoft.com/)and a number of others.
So why should you be interested in even learning Mathematica, if you can do most of the same things in Python, which is free? In my view, the money you pay for Wolfram's system is well spent because of the packaging. Many of the functions might be exactly the same you get in other systems (e.g. Lapack for linear algebra), but Mathematica packages them in a consistent syntax, with astonishingly good documentation, great support, testing and so on.

The second remark is, as might have noticed, that didn't mention the CAS aspects. Perhaps surprisingly, computer algebra is not the most important part for my job, as more often than not you're dealing with integrals that can't be analytically solved, or with directly with raw data. Nonetheless, Mathematica being a CAS is a great perk, as being able to easily manipulate your expressions makes also the numerical experiments more flexible, and Wolfram's is undoubtedly the best CAS out there (Sage, Maxima and so on can help, but aren't close).

Also, don't think that CAS can magically solve maths if you don't know it. It's true that it gan greatly help, as you might have forgotten all the myriads of formulas used to solve limits, derivatives, integrals or to transform trigonometric expressions and so on. But you still have to know what you're doing, sometimes even "better" than doing it yourself in a way that often we solve equations under some mental assumptions that don't hold true in general (i.e. range of the variables, domains, periodicity), and if you don't realize that, and tell the system, Mathematica won't be able to solve sometimes even "obvious" equations.


I've always encouraged my companies to get a few distributed seats of Mathematica, but remember, if you just need the occasional solution of an analytic expression,

I've always encouraged my companies to get a few distributed seats of Mathematica, but remember, if you just need the occasional solution of an analytic expression,

[Sage](http://www.sagemath.org/),[Maxima](http://maxima.sourceforge.net/)(both can be tried online) or even[Wolfram Alpha](http://www.wolframalpha.com/)can work wel. On iOS I use[MathStudio](https://itunes.apple.com/ca/app/mathstudio/id439121011?mt=8)but[PocketCAS](http://pocketcas.com/)and[iCAS](http://alsoftiphone.com/iCAS/)(based on[Reduce](http://reduce-algebra.com/)) look promising as well.**- Mathematica's language**

It stands to reason that a CAS is built on top of a symbolic language that supports programmatic manipulation of its own programs (code as data, a.k.a. homoiconicity), and indeed this is the case here. The most famous homoiconic language is Lisp, and indeed you're familiar with the Lisp family of languages, Mathematica won't be too far off, but there are a few notable differences.

While in Lisp everything is a list, in Mathematica, everything is an expression tree. Also, expressions in mathematica can have different forms, that is, input (or display) versions of the same internal expression node. This allows you for example to have equations entered in the standard mathematical notation (TraditionalForm) via equation editors or in a textual form that can be typed without auxiliary graphical symbols (InputForm) and so on. Mathematica's environment, the notebook, is not a purely textual one, but supports graphics, so even images and graphs can be displayed as output or input, inside equations, while still maintaining the same internal representation.

Mathematica is an interactive environment, but it's not a standard REPL (read-eval-print loop), instead it relies on the concept of "notebooks" which are a collection of "cells". Each cell can be evaluated (shift-enter) and it will yield an output cell underneath them, thus allowing for changes and re-evaluation of cells in any order. Cells can also be marked as not containing Mathematica code but just text, thus the notebook is a mix of code and documentation which enables a sort of "literary programming" style.

For completeness it's worth noticing that Mathematica also has a traditional text-only interface that can be invoked by running the Kernel outside the notebook environment, which has only textual input and output and has only the standard REPL you would expect, but there's little reason to use it. There is also a more "programming" oriented environment called the Workbench, an optional product that can make your life easier if you write lots of Mathematica code and need to profile, debug and so on.



**- By example crash course. In a notebook, put each group in a separate cell and evaluate.**

[is an OpenSource implementation based on SciPy and Sage. It also has an online interface so you can try I expect most of the code below!](http://www.mathics.org/)

Note: Mathics

Note: Mathics

(* This is a comment, if you're entering this in a notebook remember that to evaluate the content of a cell you need to use shift-enter or the numeric pad enter *)

(* Basic math is as expected, but it's kept at arbitrary precision unless you use machine numbers *)

(1+2)*3/4

(1.+2.)*3./4.

(* % refers to the last computed value *)

%+2

(* Functions are invoked passing parameters in square braces, all built-in functions start with capitals*)

Sin[Pi/3]

(* N[] forces evaluation to machine numbers, using machine numbers makes evaluation faster, but will defeat many CAS functions *)

N[Sin[Pi/3]]

(* Infix and postfix operators all have a functional form, use FullForm to show *)

FullForm[Hold[(1+2)*3/4]]

(* Each expression in a cell will yield an output in a separate output cell. Expressions can be terminated with ; if we don't want them to emit output, which is useful when doing intermediate assignments that would yield large outputs otherwise *)

1+2;

(* Assigning a symbol to a value *)

x = 10

(* If a symbol is not yet defined, it will be kept in its symbolic version as the evaluation can't proceed further. y will be assigned to the expression 10*w *)

y = x*w

(* We can see that even more clearly by peeking at the internal representation *)

y // TreeForm

(* In Mathematica, symbols are immediate values, or terminals, just like numbers are in most languages. a,b,c are the same as 1,2,3... The difference is that we can, optionally, assign values to symbols, and if that's done the evaluator will replace the symbol with its value when it encounters it... *)

(* This will recursively expand z until it reaches expansion limit and errors out: *)

(* We can see that even more clearly by peeking at the internal representation *)

y // TreeForm

(* In Mathematica, symbols are immediate values, or terminals, just like numbers are in most languages. a,b,c are the same as 1,2,3... The difference is that we can, optionally, assign values to symbols, and if that's done the evaluator will replace the symbol with its value when it encounters it... *)

(* This will recursively expand z until it reaches expansion limit and errors out: *)

z = z+1

(* Clears the previous assignments. It's not wise to assign as globals such common symbols, we use these here for brevity and will clear as needed *)

Clear[x,y,z]

(* Whenever evaluation happens immediately or not is controlled by symbols attributes. = for example, immediately evaluates *)

x = 5*2

(* y will be equal to "x*2", not 20 as := is the infix version of the function SetDelayed, which doesn't evaluate the right hand...*)

y := x*2

(* …that's because SetDelayed has attribute HoldAll, which tells the evaluator to not evaluate any of its arguments. HoldAll and HoldFirst attributes are one of the "tricky" parts, and a big difference from Lisp where you should explicitly quote to stop evaluation *)

Attributes[SetDelayed]

(* As many functions in Mathematica are supposed to deal with symbolic expressions and not their evaluated version, you'll find that many of them have HoldAll or HoldFirst, for example Plot has HoldFirst to not evaluate its first argument, that is the expression that we want to graph *)

Plot[Sin[x], {x, 0, 6*Pi}]

(* The Hold function can be used to stop evaluation, and the Evaluate function can be used to counter-act HoldFirst or HoldAll *)

Hold[x*2]

y:=Evaluate[x*2]

y

(* A neat usage of SetDelayed is for memoization of computations, the following pi2, the first time it will be evaluated, will set itself to the numerical value of Pi*Pi to 50 decimal points *)

pi2:=pi2=N[Pi*Pi,50]

pi2

(* Defining functions can be done with the Function function, which has attributes HoldAll *)

fn=Function[{x,y}, x*y];

fn[10,20]

(* As many Mathematica built-ins, Function has multiple input forms, the following is a shorthand with unnamed parameters #1 and #2, ended with the & postfix *)

fn2=#1*#2&

fn2[10,20]

(* Third version, infix notation. Note that \[Function] is a textual representation of a graphical symbol that can be more easily entered in Mathematica with the key presses: esc f n esc, many symbols can be similarly entered, try for example esc theta esc *)

fn3={x,y}\[Function]x*y

fn3[10,20]

(* A second, very common way of defining functions is to use pattern matching and delayed evaluation, the following defines the fn4 symbol to evaluate the expression x*y when it's encountered with two arguments that will matched to the symbols x and y *)

fn4[x_,y_]:=x*y

fn4[10,20]

(* _ or Blank[] can match any Mathematica expression, _h matches only expressions with the Head[] h *)

fn5[x_Integer,y_Integer]:=x+y

fn5[10,20]

fn5[10,20.]

(* A symbol can have multiple matching rules *)

fn6[0] = 1;

fn6[x_Integer] := x*fn6[x - 1]

fn6[3]

(* In general pattern matching is more powerful than Function as it's really an evaluation rule, but it's slower to evaluate, thus not the best if a function has to be applied over large datasets *)

(* Note that pattern matching can be used also with =, not only :=, but beware that = evaluates RHS, in the following fnWrong will multiply y by 3, not by the value matching test at "call" site, as test*y gets fully evaluated and test doesn't "stay" a symbol, it evaluates to its global value *)

test = 3;

fnWrong[test_, y_] = test*y

(* Lists are defined with {} *)

a={1,2,3,{4,5},{aa,bb}}

(* Elements are accessed with [[index]], indices are one-based, negative wrap-around *)

a[[1]]

a[[-1]]

(* Note! Mathematica thinks of symbols and pattern-matching as more fundamental than arrays, [] is about patterns, [[]] is about arrays. So x[1]=0 defines the symbol x to be 0 when the first variable slot has value 1. This can be used to define recurrences as well, see RSolve. *) (* x[[1]]=0 instead evaluates symbol x first, if it is a list then [[]] makes sense as it's a postfix operator on lists... If you need ten different symbols, Array[x,10] will do the trick... *)

(* Note! Mathematica thinks of symbols and pattern-matching as more fundamental than arrays, [] is about patterns, [[]] is about arrays. So x[1]=0 defines the symbol x to be 0 when the first variable slot has value 1. This can be used to define recurrences as well, see RSolve. *) (* x[[1]]=0 instead evaluates symbol x first, if it is a list then [[]] makes sense as it's a postfix operator on lists... If you need ten different symbols, Array[x,10] will do the trick... *)

(* Ranges are expressed with ;; or Span *)

a[[2;;4]]

(* From the beginning to the second last *)

a[[;;-2]]

(* Vectors and matrices are just appropriately sized lists and lists of lists *)

b={1,2,3}

m={{1,0,0},{0,1,0},{0,0,1}}

(* . is the product for vector, matrices, and tensors *)

m.b

(* Expression manipulation and CAS. ReplaceAll or /. applies rules to an expression *)

(x+y)/.{x->2,y->Sin[Pi]}

(* Rules can contain patterns, the following will match only the x symbols that appear to a power, match the expression of the power and replace it *)

Clear[x];

1+x+x^2 +x^(t+n)/.{x^p_->f[p]}

(* In a way, replacing a symbol with a value in an expression is similar to defining functions using := or = and pattern-matching, but we have to manually replace the right symbol... *)

expr = x*10

expr/.x->5

(* Mathematica has lots of functions that deal with expressions, Integrate, Limit, D, Series, Minimize, Reduce, Refine, Factor, Expand and so on. We'll show only some basic examples. Solve finds solution to systems of equations or inequalities *)

Clear[a];

Solve[x^2+a*x+1==0, x]

(* It returns results as list of replacement rules that we can replace into the original equation *)

eq=x^2+a*x+1

sol=Solve[eq==0, x]

neweq=eq/.sol[[1]]

(* Simplifying neweq yields true as the equation is satisfied *)

Simplify[neweq]

(* Assumptions on the variables can be made *)

Simplify[Sqrt[x^2], Assumptions -> x < 0]

(* fn7 will compute the Integral and Derivative every time it's evaluated, as Function is HoldAll, fn8, using Evaluate, will force the definition to be equal to the simplified version which yields correctly back the original equation *)

fn7[x_]:=Function[x,D[Integrate[x^3,x],x]]

fn8[x_]:=Function[x,Evaluate[Simplify[D[Integrate[x^3,x],x]]]]

(* Many procedural programming primitives are supported *)

If[3>2,10,20]

For[i = 0,i < 4,i++,Print[i]]

n=1; While[n < 4,Print[n];n++]

Do[Print[n^2],{n,4}]

(* Boolean operators are C-like for the most, only Xor is not ^ which means Power instead *)

!((1>2)||(4>3))&&((1==1)&&(5<=6))

(* Equality tests can be chained *)

(5>4>3)&&(1!=2!=3)

(* == compares the result of the evaluation on both sides, === is true only if the expression are identical *)

v1=1;v2=1;

v1==v2

v1===v2

(* Boolean values are False and True. No output is Null *)

(* With, Block and Module can be used to set symbols to temporary values in an expression *)

With[{x = Sin[y]}, x*y]

Block[{x = Sin[y]}, x*y]

Module[{x = Sin[y]}, x*y]

(* The difference is subtle. With acts as a replacement rule. Block temporarily assigns the value to a symbol and the restores the previous definition. Module creates an unique, temporary symbol, which affects only the occurrences in the inner scope. *)

m=i^2

Block[{i = a}, i + m]

Module[{i = a}, i + m]

(* In general prefer Block or With, which are faster than Module. Module implements lexical scoping, Block does dynamic scoping *)

(* Block and Module don't require to specify values for the declared locals, With does. The following is fine with Block, not with With*)

Block[{i},i=10;i+m]

(* Data operations. Table generates data from expressions *)

Table[i^2,{i,1,10}]

(* Table can generate multi-dimensional arrays, i.e. matrices *)

Table[10*i+j,{i,1,4},{j,1,3}]

MatrixForm[%]

(* List elements can be manipulated using functional programming primitives, like Map which applies a function over a list *)

squareListElements[list_]:=Map[#^2&,list]

(* Short-hand, infix notation of Map[] is /@ *)

squareListElements2[list_]:=(#^2&)/@list

(* You can use MapIndexed to operate in parallel across two lists, it passes to the mapped function *)

addLists[list1_,list2_]:=MapIndexed[Function[{element,indexList},element + list2[[indexList[[1]]]] ], list1]

addLists[{1,2,3},{3,4,5}]

(* A more complete version of the above that is defined only on lists and asserts if the two lists are not equal size. Note the usage of ; to compound two expressions and the need of parenthesis *)

On[Assert]

addListsAssert[list1_List,list2_List]:=(Assert[Length[list1]==Length[list2]]; MapIndexed[Function[{element,indexList},element + list2[[indexList[[1]]]] ], list1])

(* Or Thread can be used, which "zips" two or more lists together *)

addLists2[list1_,list2_]:=MapThread[#1+#2&,{list1,list2}]

(* There are many functional list manipulation primitives, in general, using these is faster than trying to use procedural style programming. Extract from a list of the first 100 integers, the ones divisible by five *)

Select[Range[100],Mod[#,5]==0&]

(* Group together all integers from 1...100 in the same equivalence class modulo 5 *)

Gather[Range[100],Mod[#1,5]==Mod[#2,5]&]

(* Fold repeatedly applies a function to each element of a list and the result of the previous fold *)

myTotal[list_]:=Fold[#1+#2&,0,list]

(* Another way of redefining Total is to use Apply, which calls a function with as arguments, the elements of a list. The infix shorthand of Apply is @@ *)

myTotal2[list_]:=Apply[Plus,list]

(* Mathematica's CAS abilities also help with numerical algorithms, as Mathematica is able to infer some information from the equations passed in order to select or optimize the numerical methods *)

(* NMinimize does constrained and unconstrained minimization, linear and nonlinear, selecting among different algorithms as needed *)

Clear[x,y]

NMinimize[{x^2-(y-1)^2, x^2+y^2<=4}, {x,y}]

(* NIntegrate does numerical definite integrals. Uses Monte Carlo methods for many-dimensional integrands *)

NIntegrate[Sin[Sin[x]], {x,0,2}]


(* NSum approximates discrete summations, even to infinites *)

NSum[(-5)^i/i!,{i,0,Infinity}]

(* Many other analytic operators have numerical counterparts, like NLimit, ND and so on... *)

NLimit[Sin[x]/x,x->0]

ND[Exp[x],x,1]

(* Mathematica's plots produce Graphics and Graphics3D outputs, which the notebook shows in a graphical interface *)

Plot[Sin[x],{x,0,2*Pi}]

(* Graphics are objects that can be further manipulated, Show combines different graphics together into a single one *)

g1=Plot[Sin[x],{x,0,2*Pi}];

g2=Plot[Cos[x],{x,0,2*Pi}];

Show[g1,g2]

(* GraphicsGrid on the other hand takes a 2d matrix of Graphics objects and displays them on a grid *)

GraphicsGrid[{{g1,g2}}]

(* Graphics and Graphics3D can also be used directly to create primitives *)

Graphics[{Thick,Green,Rectangle[{0,-1},{2,1}],Red,Disk[],Blue,Circle[{2,0}]}]

(* Most Mathematica functions accept a list of options as the last argument. For Plots an useful one is to override the automatic range. Show by default uses the range of the first Graphics so it will cut the second plot here: *)

Show[Plot[x^2,{x,0,1}],Plot[x^3,{x,1,2}]]

(* Forcing to show all the plotted data *)

Show[Plot[x^2,{x,0,1}],Plot[x^3,{x,1,2}], PlotRange->All]

(* Very handy for explorations is the ability of having parametric graphs that can manipulated. Manipulate allows for a range of widgets to be displayed next to the output of an expression *)

Manipulate[Plot[x^p,{x,0,1}],{{p,1},1,10}]

Manipulate[Plot3D[x^p[[1]]+y^p[[2]],{x,0,1},{y,0,1}],{{p,{1,1}},{1,1},{5,5}}]

(* Manipulate output is a Dynamic cell, which is special as it get automatically re-evaluated if any of the symbols it capture changes. That's why you can see Manipulate output behaving "weirdly" if you change symbols that are used to compute its output. This allows for all kind of "spreadsheet-like" computations and interactive applications. *)

(* Debugging functional programs can be daunting. Mathematica offers a number of primitives that to a degree help. Monitor generates a temporary output that shows the computation in progress. Here the temporary output is a ProgressIndicator graphical object. Evaluations can be aborted with Alt+. *)

Monitor[Table[FactorInteger[2^(2*n)+1],{n,1,100}], ProgressIndicator[n, {1,100}]]

(* Another example, we assign the value of the function to be minimized to a local symbol, so we can display how it changes as the algorithm progresses *)

complexFn=Function[{x,y},(Mod[Mod[x,1],Mod[y,1]+0.1])*Abs[x+y]]

Plot3D[complexFn[x,y],{x,-2,2},{y,-2,2}]

Block[{temp},Monitor[NMinimize[{temp=complexFn[x,y],x+y==1},{x,y}],N[temp]]]

(* Print forces an output from intermediate computations *)

Do[Print[Prime[n]],{n,5}]

(* Mathematica also supports reflection, via Names, Definition, Information and more *)

(* Performance tuning. A first common step is to reduce the number of results Mathematica will keep around for % *)

$HistoryLength=2

(* Evaluate current memory usage *)

MemoryInUse[]

(* Share[] can sometimes shrink the memory usage by making Mathematica realize that certain subexpressions can be shared, it prints the amount of bytes saved *)

Share[]

(* Reflection can be used to know which symbols are taking the most memory *)

Reverse@Sort[{ByteCount[Symbol[#]],#}&/@Names["`*"]]

(* Timing operations is simple with AbsoluteTiming *)

AbsoluteTiming[Pause[3]]

(* Mathematica's symbolic evaluation is relatively slow. Machine numbers operations are faster, but slow compared to other languages. In general Mathematica is not made for high-performance, and if that's needed it's best to directly go to one of the ways it supports external compilation: LibraryLink, CudaLink, and OpenCLLink *)

(* On the upside, many list-based operations are trivially parallelizable via Parallelize *)

Parallelize[Table[Length[FactorInteger[10^50+n]],{n,20}]]

(* The downside is that only a few functions seems to be natively parallelized, mostly image-related, and many others require manual parallelization via domain-splitting. E.G. integrals *)

sixDimensionalFunction=Function[{a,b,c,d,e,f},Re[(a*b+c)^d/e+f]];

Total[ParallelTable[NIntegrate[sixDimensionalFunction[a,b,c,d,e,f],{a,-1,1},{b,-1,1},{c,-1,1},{d,-1,1},{e,-1,1},{f,-1+i/4,-1+(i+1)/4}],{i,0,7}]]

(* Even plotting ca be parallelized, see http://mathematica.stackexchange.com/questions/30391/parallelize-plotting. Intra-thread communication is expensive, beware of the amount of data you move! *)

(* There is a Compile functionality that can translate -some- Mathematica expressions into bytecode or C code, even parallelizing, but it's quite erratic and requires planning from the get-go of your code. See http://mathematica.stackexchange.com/questions/1803/how-to-compile-effectively/ http://mathematica.stackexchange.com/questions/1096/list-of-compilable-functions*)

**- Parting thoughts**

Clearly, it's impossible to cover all the library functionality that Mathematica offers. But for that the documentation is great, and usually a bit of search there and if it fails, on the stackexchange forums, will yield a very elegant solution for most issues.

Performance can be tricky, and can require more effort than using directly native CPU and GPU languages, on the other hand, support for external CPU and GPU functions is great and Mathematica is capable of invoking external compilers from strings of sourcecode, and you can use Mathematica as a template metaprogramming language, even with a bit of effort converting its expressions into other language equivalents (a good starting point is CForm[]). Being a very strong pattern-matching engine, quite some magic is possible.

Next time I might write something that shows in practice how Mathematica, via it's numerical and visualization abilities enables exploration of possible approximations of expensive rendering formulas... Stay tuned.

Further reading:

[http://mathematica.stackexchange.com/questions/18393/what-are-the-most-common-pitfalls-awaiting-new-users](http://mathematica.stackexchange.com/questions/18393/what-are-the-most-common-pitfalls-awaiting-new-users)[http://mathematica.stackexchange.com/questions/18/where-can-i-find-examples-of-good-mathematica-programming-practice](http://mathematica.stackexchange.com/questions/18/where-can-i-find-examples-of-good-mathematica-programming-practice)[http://reference.wolfram.com/mathematica/tutorial/Evaluation.html](http://reference.wolfram.com/mathematica/tutorial/Evaluation.html)[http://mathematica.stackexchange.com/questions/148/get-a-step-by-step-evaluation-in-mathematica](http://mathematica.stackexchange.com/questions/148/get-a-step-by-step-evaluation-in-mathematica)[http://mathematica.stackexchange.com/questions/20718/keep-function-range-as-a-variable](http://mathematica.stackexchange.com/questions/20718/keep-function-range-as-a-variable)[http://files.meetup.com/1764148/Mathematica%20%2B%20GPU.pdf](http://files.meetup.com/1764148/Mathematica%20%2B%20GPU.pdf)[http://library.wolfram.com/conferences/devconf99/villegas/UnevaluatedExpressions/](http://library.wolfram.com/conferences/devconf99/villegas/UnevaluatedExpressions/)

## 1 comment:

Hey!




Thanks for the tutorial. I've been using Mathematica for a bit now and learned a few new things from this post.

Appreciate it.

-= Dave

Post a Comment