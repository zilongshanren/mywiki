---
title: Java and Vector Math
url: https://www.elopezr.com/java-and-vector-math/
author: Redorav
published: '2014-06-15'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

Some time ago, I had to develop a 3D vector utility class for Java. Because the Android platform only uses Java, this is a must if you’re developing for it (unless you’re directly using the NDK or some middleware such as Unity. I’ll get back to this later).

Java, like all programming languages, has its virtues and weaknesses. I found trying to develop a solid Vector3 class to be one such weakness, because Java lacks two main features that I consider core to what I was trying to achieve: **stack-allocated objects** and **operator overloading**. These missing features make operating with vectors in Java an annoyance beyond measure.

As much as some people seem to dislike operator overloading, **vector/matrix math** is one domain where I consider they excel, and the lack of it is going to force me to always go through functions for even the simplest of operations, such as adding/subtracting two vectors or multiplying/dividing by a scalar.

Compare the following lines of code:

1 2 3 | Vector3 vTest1 = new Vector3(1, 1, 1); // First vector Vector3 v1 = 3 * vTest1; Vector3 v2 = vTest1.mul(3); |

Doesn’t seem too bad, does it? Let’s try something different, like obtaining a direction from two points, normalizing, scaling by a factor, and adding it to a point (a relatively frequent operation)

1 2 3 4 5 6 7 | Vector3 pOrigin = new Vector3(1, 2, 3); // Random origin point Vector3 pTest1 = new Vector3(3, 3, 3); // Point 1 Vector3 pTest2 = new Vector3(5, 5, 5); // Point 2 sp // v2 clearly a lot harder to read Vector3 v1 = pOrigin + (pTest2 – pTest1).norm() * factor; [1] Vector3 v2 = pOrigin.add(pTest2.subtract(pTest1).norm().mul(factor)); [2] |

It’s either that or separating into several lines so it becomes clearer and a bit more readable. This is clearly an undesirable way of working with vectors, but the only at our disposal when using Java.

There’s another caveat, though, one that is implicit in the way we have used the equal operator until now. We have been assigning the Vector3 **by reference** all this time, invalidating the erroneous assumption that we get a new Vector3 out of the operation. What we want is a copy of the resulting Vector3, which means create a new Vector3 using the new operator, and copy the values into the new Vector3. Therefore, line [2] would become something along the lines of:

1 | Vector3 v2 = new Vector3(pOrigin.add(pTest2.subtract(pTest1).norm().multiply(factor))); |

or

1 2 | Vector3 v2 = new Vector3(); v2.copy(pOrigin.add(pTest2.subtract(pTest1).norm().multiply(factor))); |

In any case it is a very confusing way of working with vectors.

There is yet another annoyance to be wary of when working with instantiations on the heap in a garbage collected language such as Java which is, precisely, **the dreaded Garbage Collector**. Vector3 operations typically go inside long loops where interesting calculations take place for many objects in the virtual world, and creating all those new objects in the heap is asking for trouble when the GC comes to inspect your pile of vector rubbish and tries to clean up the mess. This is due to the fact that **there are no stack-allocated objects in Java**, leaving us with one option – creating temporary Vector3’s and reusing them. This has its fair share of problems too – mainly readability, the ability to use several temporary vectors for intermediate calculations, and having to pass the Vector3 reference as a parameter instead of returning it as a normal function return value. Let’s go back to our example.

1 2 3 4 5 6 7 | Vector3 mTempVector = new Vector3(); // Declare as member variable // […] Several hundred lines down the code tempVector.copy(pOrigin.add(pTest2.subtract(pTest1).norm().multiply(factor))); interestingMathFunction(param1, param2, tempVector); // Here tempVector is an output! interestingMathFunction2(tempVector, tempVector2, tempVector3); // Need more temp vectors! Some can be inputs, some other outputs, // no way of knowing without looking at the function declaration. |

Definitely not ideal. In contrast, and for all its similarity with Java, C# has both these features, which makes it a language of choice for these kinds of applications, and I wonder if it was one among the multiple reasons why Unity chose it as their main development language.