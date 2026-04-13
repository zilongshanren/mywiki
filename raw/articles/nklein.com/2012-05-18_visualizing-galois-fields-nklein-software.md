---
title: 'Visualizing Galois Fields :: nklein software'
url: http://nklein.com/2012/05/visualizing-galois-fields/
author: Pat
published: '2012-05-18'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

[Galois](http://www.lipwalklyrics.com/lyrics/728310-thekleinfour-stefanietheballadofgalois.html) fields are used in a number of different ways. For example, the AES encryption standard uses them.

### Arithmetic in Galois Fields

The Galois fields of size for various

are convenient in computer applications because of how nicely they fit into bytes or words on the machine. The Galois field

has

elements. These elements are represented as polynomials of degree less than

with all coefficients either 0 or 1. So, to encode an element of

as a number, you need an

-bit binary number.


For example, let us consider the Galois field . It has

elements. They are (as binary integers)

,

,

,

,

,

,

, and

. The element

, for example, stands for the polynomial

. The element

stands for the polynomial

.


The coefficients add together just like the integers-modulo-2 add. In group theory terms, the coefficients are from . That means that

,

,

, and

. In computer terms,

is simply

XOR

. That means, to get the integer representation of the sum of two elements, we simply have to do the bitwise-XOR of their integer representations. Every processor that I’ve ever seen has built-in instructions to do this. Most computer languages support bitwise-XOR operations. In Lisp, the bitwise-XOR of

and

is

`(logxor a b)`

.

Multiplication is somewhat trickier. Here, we have to multiply the polynomials together. For example, . But, if we did

, we’d end up with

. We wanted everything to be polynomials of degree less than

and our

is 3. So, what do we do?


What we do, is we take some polynomial of degree that cannot be written as the product of two polynomials of less than degree

. For our example, let’s use

(which is

in our binary scheme). Now, we need to take our products modulo this polynomial.


You may not have divided polynomials by other polynomials before. It’s a perfectly possible thing to do. When we divide a positive integer by another positive integer

(with

bigger than 1), we get some answer strictly smaller than

with a remainder strictly smaller than

. When we divide a polynomial of degree

by a polynomial of degree

(with

greater than zero), we get an answer that is a polynomial of degree strictly less than

and a remainder that is a polynomial of degree strictly less than

.


Dividing proceeds much as long division of integers does. For example, if we take the polynomial (with integer coefficients) and divide it by the polynomial

, we start by writing it as:


[Finite Field Arithmetic and Reed Solomon Codes](http://research.swtch.com/field). In (tail-call style) Lisp, that algorithm for

(ash a -1))

(next-b (b)

(let ((overflow (plusp (logand b #x80))))

(if overflow

(mod (logxor (ash b 1) m) #x100)

(ash b 1)))))

(labels ((mult (a b r)

(cond

((zerop a) r)

((oddp a) (mult (next-a a) (next-b b) (logxor r b)))

(t (mult (next-a a) (next-b b) r)))))

(mult a b 0)))

### How is the Galois field structured?

The additive structure is simple. Using our 8-bit representations of elements of , we can create an image where the pixel in the

-th row and

-th column is the sum (in the Galois field) of

and

(written as binary numbers). That looks like this:


![gf256](../../assets/c825fba318f8ac16.png)


![gf256](../../assets/c825fba318f8ac16.png)

[above-mentioned article](http://research.swtch.com/field)hit

Remember way back at the beginning of multiplication, I said that the modulus polynomial had to be one which couldn’t be written as the product of two polynomials of smaller degree? If you allow that, then you have two non-zero polynomials that when multiplied together will equal your modulus polynomial. Just like with integers, if you’ve got an exact multiple of the modulus, the remainder is zero. We don’t want to be able to multiply together two non-zero elements to get zero. Such elements would be called zero divisors.

Zero divisors would make these just be Galois rings instead of Galois fields. Another way of saying this is that in a field, the non-zero elements form a [group under multiplication](http://en.wikipedia.org/wiki/Group_(mathematics)). If they don’t, but multiplication is still associative and distributes over addition, we call it a ring instead of a field.

Galois rings might be interesting in their own right, but they’re not good for AES-type encryption. In AES-type encryption, we’re trying to mix around the bits of the message. If our mixing takes us to zero, we can never undo that mixingâthere is nothing we can multiply or divide by to get back what we mixed in.

So, we need a polynomial that cannot be factored into two smaller polynomials. Such a polynomial is said to be irreducible. We can just start building an image for the multiplication for a given modulus and bail out if it has two non-zero elements that multiply together to get zero. So, I did this for all elements which when written in our binary notation form odd numbers between (and including) 100000001 and 111111111 (shown as binary). These are the only numbers which could possibly represent irreducible polynomials of degree 8. The even numbers are easy to throw out because they can be written as times a degree 7 polynomial.


The ones that worked were: 100011011, 100011101, 100101011, 100101101, 100111001, 100111111, 101001101, 101011111, 101100011, 101100101, 101101001, 101110001, 101110111, 101111011, 110000111, 110001011, 110001101, 110011111, 110100011, 110101001, 110110001, 110111101, 111000011, 111001111, 111010111, 111011101, 111100111, 111110011, 111110101, and 111111001. That first one that worked (100011011) is the one used in AES. Its multiplication table looks like:

![gf256-x11B](../../assets/f22cb08f8d406708.png)


![gf256-x11B](../../assets/f22cb08f8d406708.png)

[Â](http://nklein.com/wp-content/uploads/2012/05/gf256-x11B.png)![gf256-x11B](../../assets/f22cb08f8d406708.png)


![gf256-x11B](../../assets/f22cb08f8d406708.png)

![gf256-x19F](../../assets/7c413626f85920c3.png)


![gf256-x19F](../../assets/7c413626f85920c3.png)

To say two of the multiplication tables have the same structure, means there is some way to map back and forth between them so that the multiplication still works. If we have table and table

, then we need an invertible function

such that

for all

and

in the table

.


### What’s next?

If there is an invertible map between two multiplication tables and there is some element in the first table, you can take successive powers of it:

,

,

,

. There are only

elements in

no matter which polynomial we pick. So, somewhere in there, you have to start repeating. In fact, you have to get back to

. There is some smallest, positive integer

so that

in

. If we pick

, then we simply have that

. For non-zero

, we are even better off because

.


So, what if I took the powers of each element of in turn? For each number, I would get a sequence of its powers. If I throw away the order of that sequence and just consider it a set, then I would end up with a subset of

for each

in

. How many different subsets will I end up with? Will there be a different subset for each

?


I mentioned earlier that the non-zero elements of form what’s called a group. The subset created by the powers of any fixed

forms what’s called a subgroup. A subgroup is a subset of a group such that given any two members of that subset, their product (in the whole group) is also a member of the subset. As it turns out, for groups with a finite number of elements, the number of items in a subgroup has to divide evenly into the number of elements in the whole group.


The element zero in forms the subset containing only zero. The non-zero elements of

form a group of

elements. The number

is odd (for all

). So, immediately, we know that all of the subsets we generate are going to have an odd number of items in them. For

, there are 255 non-zero elements. The numbers that divide 255 are: 1, 3, 5, 15, 17, 51, 85, and 255.


It turns out that the non-zero elements of form what’s called a cyclic group. That means that there is at least one element

whose subset is all

of the non-zero elements. If take one of those

‘s in

whose subset is all 255 of the elements, we can quickly see that the powers of

form a subset containing 85 elements, the powers of

form a subset containing 51 elements, …, the powers of

form a subset containing 3 elements, and the powers of

form a subset containing 1 element. Further, if both

and

have all 255 elements in their subset, then

and

will have the same number of elements in their subsets for all

. We would still have to check to make sure that if

that

to verify the whole field structure is the same.


This means there are only 8 different subset of ‘s non-zero elements which form subgroups. Pictorially, if we placed the powers of

around a circle so that

was at the top and the powers progressed around the circle and then drew a polygon connecting consecutive points, then consecutive points in the

sequence and consecutive points in the

sequence, etc…. we’d end up with this:


![z255c](../../assets/a4634fa5d4e8fd73.png)


![z255c](../../assets/a4634fa5d4e8fd73.png)

[Â](http://nklein.com/wp-content/uploads/2012/05/gf256-x11Bc.png)![gf256-x11Bc](../../assets/039ef1ef143ca593.png)


![gf256-x11Bc](../../assets/039ef1ef143ca593.png)

![gf256-x19Fc](../../assets/7b43d4bfda1a7265.png)


![gf256-x19Fc](../../assets/7b43d4bfda1a7265.png)

[Vecto](http://www.xach.com/lisp/vecto/)and

[ZPNG](http://www.xach.com/lisp/zpng/):

[group.lisp](http://nklein.com/wp-content/uploads/2012/05/group.lisp)

I suspect that if you use the ordering 0, a^0, a^1, … the multiplication table looks simpler since

a^i a^j = a^(i+j).

No idea what the addition table then looks like.

PS: typos: “logior”, “something like something like”

Indeed, I should re-render the multiplication table with the cyclic ordering. And fixed the typos. Thanks.

Well explained, thanks.âBy the way, DEC’s PDP-8 minicomputer didn’t have an

exclusive-orinstruction, or a plainorinstruction come to that.â(It did haveandandnotand fromnandflows everything else.)Very cool!

I learned about GF(q^n) when I was studying network coding, but I never thought about drawing out the + and * tables.

I recommend that you set “vertical-align:middle” to the math equation in your post.

In fact, you might as well use MathJax which is the best way since sliced bread and handles all kinds of LaTeX through javascript, UTF8 and STIX fonts.

Yes, I do need to work on the alignment of the equations. I’m not a fan of MathJax though. It takes tons of time to get all of the equations rendered on my iPhone and even on some desktop browser (do not recall which, right now) where I thought the browser had crashed because I couldn’t scroll for minutes at a time.

[…] my previous article, I should have finished by remapping the multiplication and addition tables so that the […]