---
title: Reading Math Papers
url: https://mini.gmshaders.com/p/readingmath
author: Xor
published: '2025-04-10'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

Mathematical papers or math-related wiki pages can be challenging for anyone to read. Shaders often do use a lot of math, but concepts are written quite differently. You don’t have to be good at mathematics before becoming a good programmer, but mathematical concepts can certainly help you take things further. There’s often a lot of overlap between physics and computer graphics. Take, for example, the Rendering Equation:

Maybe it’s been a few years since you’ve taken a math class, or you’ve never had a strong educational mathematical foundation to begin with. This article is aimed specifically to serve as a reference point to help get you caught up to speed. I was homeschooled and taught myself after Geometry, so I know firsthand how challenging it can be to approach on your own! I have even learned a bit while writing this. If you get stuck somewhere along the way, don’t worry; that’s perfectly normal! Skip that part, or take a break and revisit it later. Hopefully, this will save you lots of time on your journey and give you new mathematical tools to use!

Basic Notation

At this point, you’re familiar with the concepts of scalars (floats), vectors, and matrices, but they are written differently in mathematics papers, so it’s important to know what to look for. Because countless people developed the field of mathematics over the course of thousands of years, there are many different ways things can be written, making it a little more difficult to interpret. This article will serve as a general guideline, but there are exceptions to watch out for.

Scalars are one-letter variables like “a” or “b”.

Vectors are usually written as a boldface “v” or with a right arrow over top, like so v⃗.

Vector components are written in subscript, starting from 1, 2, 3… (not 0), or often just x, y, z, like in GLSL:

Hats are used for unit vectors (normalized vectors with a length of 1.0): â. Cute right?

Matrices are typically written with capital letters like “A”, and the values are arranged in big square brackets, row by row, with spaces to separate components. Sometimes matrices with one row or one column are used as vectors. I wrote an article about matrices if you’d like to learn more!

Tensors are the extension of the idea of scalars (0th order tensors), vectors (1st order tensors), and matrices (2nd order tensors). A first-order tensor can be thought of as a 1D array or vector, and as you can imagine, a third-order tensor is the same as a 3D array. So you’ve already been using Tensors, whether you knew it or not.

Operations

Multiplication is generally just two or more variables concatenated. “ab” is the same as “a*b”. In arithmetic, scalar multiplication may use “a×b” or “a·b”, but it is not to be confused with vector cross products or dot products. We’ll cover that later!

Summations add an expression with multiple iterations, and Products multiply with multiple iterations.

Exponentiation is written with superscript exponents: 32 = pow(3.0, 2.0).

In Boolean Algebra, you have the logical operations: “a∧b” (AND), “a∨b” (OR), “¬a” (NOT), and “a⊕b” (XOR, yes… that’s where my username comes from). Boolean equivalence can be written with “a≡b” which would be written as “a==b” in most programming languages. Not-equal is written with “a≠b”

The Absolute Value operation is written with vertical bars like “|x|” instead of the “abs(x)” function.

Vector Length is written with double vertical bars like “||v||”. So, for example, you could write a normalized vector “a” like so:

\(\hat{a} = \frac{ \vec a}{\|\vec a\|}\)

Dot Products and Cross Products are written with “⋅” and “×” respectively. Not to be confused with arithmetic scalar multiplication. The dot product may also be written as an Einstein Summation, but it does the same thing:

\(\vec a \cdot \vec b = \sum_i a_i b_i\)

Functions

Functions are typically written like “f(x, y) = x+y” with x and y being the function arguments and “x+y” being the returned value. Sometimes, unambiguous functions are written without parentheses, like “sin x”.

Inverse functions undo the operation of another function. They are typically written like “f-1(y) = x”. For example, if you have “f(x) = x+2”, then the inverse function would be “f-1(x) = x-2”. Not all functions are invertible. For example, with ‘f(x) = x²’, ‘f⁻¹(25)’ could be 5 or -5 because both 5² and (-5)² equal 25. A function needs a unique output for every input (one-to-one) to have a proper inverse.”

Arrow Notation may also be used for “inline” functions. For example, an incrementing function could be written like “x ↦ x+1”. So, if x = 5, the output is 5+1 or 6. Barred arrows “↦” are used for remapping elements, while unbarred arrows “→” are used to describe “sets”, which we will cover next.

Set Theory intuitively has to do with sets of numbers. You have Natural Numbers: 1, 2, 3… and these are just positive whole numbers (so no fractions or decimals). Integers include negative numbers: …-2, -1, 0, 1, 2… and are written as “int” in GLSL. Here’s a quick list of the main relevant sets:

ℕ - Natural numbers, positive whole numbers: 1, 2, 3… In some math contexts, 0 is included (written as ℕ₀), but we’ll stick to excluding 0 (ℕ₁) unless noted, aligning with positive integers. Compare this to uint in GLSL, which starts at 0..

ℤ - Integers, positive, negative or zero, whole numbers: … -1, 0, 1… These are “ints” in GLSL.

ℚ - Rational numbers, include integers, fractions, and decimals like 1/2 or -0.8. They include any number that can be written as a ratio of two integers: x/y. “floats” are generally rational numbers that can be written as a ratio. The exceptions are positive infinity, negative infinity, and the undefined “Not a Number”.

ℝ - Real numbers, include rational numbers and irrational numbers like sqrt(2.0), log(7.0), or π. These numbers cannot be represented with just fractions (decimals), and they have to be rationally approximated with floats. The positive-only real number set is written with a plus: ℝ+.

ℂ - Complex Numbers, include imaginary numbers like “i” and numbers with both real and imaginary components like “2+i”. Most programming languages do not support Complex Number calculations directly, but they can be thought of as 2D vectors with both a real component and an imaginary “i” component. I won’t get into imaginary numbers here, but if you do come across them (e.g., with sqrt or the log of a negative), you will have to calculate the imaginary components manually to avoid errors. All GLSL functions return “undefined” when an imaginary number would occur, so you’ll have to handle these edge cases yourself. A common example might be the Mandelbrot Set or quaternions.

∅ - Empty Sets contain nothing.

{a, b, c} - FiniteSets can contain any number of elements. For example, sign(x) returns values in the set {-1, 0, +1}.

[a, b] - ClosedIntervals include “a”, “b”, and all real numbers between. Parentheses can be used instead of square brackets for “Open Intervals”, which exclude the endpoint numbers. For instance, fract(x) returns a value between 0.0 and 1.0. This is an interval of [0 1). Why? Well, with an input of x=0.0, you get an output of 0.0, but with an input of 1.0, you also get an output of 0.0. You can get close to 1.0, like 0.999, but the interval does not include 1.0. This concept is quite useful to know!

∈ - Element of Set, used to show when a number or variable is an element of a set like: “x ∈ ℝ”. This means that “x” is a real number. “∉” is used when an element is not a member of a set.

Hopefully, that wasn’t too overwhelming. The most important are real numbers, sets, and intervals because they show up the most. Now, let’s put Set Theory together with Arrow Notation and look at an easy example of the sign function:

This tells us that “sgn” takes a real number input (between -∞ and +∞) and remaps it to the set -1, 0, or 1. Thankfully, the if-statement logic is pretty intuitive to us programmers:

//Reconstructed sign function
//"x" is any number between -∞ and +∞
float sgn(float x)
{
if (x >0.0) return +1.0; //Positive numbers
if (x==0.0) return 0.0; //Zero
if (x <0.0) return -1.0; //Negative numbers
}

Now on to function domains and ranges…

Continue reading this post for free, courtesy of Xor.