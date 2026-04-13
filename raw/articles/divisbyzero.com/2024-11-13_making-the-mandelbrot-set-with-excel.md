---
title: Making the Mandelbrot Set with Excel
url: https://divisbyzero.com/2024/11/13/making-the-mandelbrot-set-with-excel/
author: Dave Richeson
published: '2024-11-13'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

The Mandelbrot set is one of the most stunning geometric objects in all of mathematics. In this blog post, I will show how to generate the Mandelbrot set below using Excel. It is also an example of how you can use AI (I used ChatGPT) to help with a task like this. (Here is [the Excel file](https://divisbyzero.com/wp-content/uploads/2024/11/mandelbrotexcel.xlsx) I created if you want to play with it.)

![](../../assets/cd380540a4404944.png)


![](../../assets/cd380540a4404944.png)

## An introduction to the Mandelbrot set

First, let’s explain what the Mandelbrot set is. We begin with a family of functions with complex numbers as inputs and outputs. Let be a complex number (a parameter). Define the function

by



Given a starting value, a complex number (called the

*seed*), we plug it into the function to get Then, plug the output back in

the new output back in

and so on, to get a sequence of complex numbers,

called the

*orbit* of


For instance, suppose our parameter is and we begin with the seed

Then, the orbit is



What you’ll find if you play with this function for a while is that some orbits go off to infinity while others remain bounded. A bounded orbit might be periodic, might get closer to some periodic orbit, or might behave chaotically.

The *Mandelbrot set* is a subset of the set of parameter values. Some parameter values are in the Mandelbrot set, and some are not. To test whether a parameter is in the Mandelbrot set, we focus on the orbit of 0. If the orbit of 0 remains bounded, our parameter is in the Mandelbrot set. If the orbit of 0 goes off to infinity,

is not in the Mandelbrot set.


In our example with parameter the orbit of of 0 is

This orbit eventually lands on a period-2 orbit. So, the orbit is bounded, and

is in the Mandelbrot set. On the other hand, with the parameter

the orbit of 0 is

This orbit goes to infinity, so 1 is not in the Mandelbrot set.


If you want to draw the Mandelbrot set on a computer, you can think of your display screen as the complex plane. Each pixel represents a complex number The

value corresponds to a column and the

value corresponds to a row. We view

as the parameter for the function

Compute the first

terms in the orbit of 0 (you will have to decide on a good

). If the orbit gets farther than

units away from the origin (you will have to decide on a good

), then

is not in the Mandelbrot set; color it white. If it does not go that far away, it is likely in the Mandelbrot set; color it black.


That’s it!

If you want those stunning pictures in which the black Mandelbrot is surrounded by a beautiful, colorful gradient, you have to do a little more work, although not much more. For the points not in the Mandelbrot set, keep track of when the orbit gets farther than units away from the origin. Does it get that far away after 5 steps? 10 steps? 50 steps? Color the pixel based on that exit time.


## The Mandelbrot set in Excel

Yesterday, I had the idea of creating the Mandelbrot set using Excel. I could treat each cell as a complex number (the parameter ). In that cell, I could check whether the complex number is or is not in the Mandelbrot set. I could mark it with a 0 or 1 to indicate its status.


I’m handy with Excel, but I’m not a power user. I did not want to figure out how to come up with the code for this. I decided to ask ChatGPT for help. I began by placing the sequence in the first row and the sequnce

in the first column. These values represented the

and

coordinates for the complex numbers

in the square region of the spreadsheet.


After a little back-and-forth with ChatGPT, I got the following code, which uses and

(I told ChatGPT exactly what I wanted it to do. It took a few tries because it was using variable names like z1, z2, etc., which Excel thought were references to cells in the spreadsheet.) This code goes in the cell B2, and similar code goes into the rest of the cells.


`=LET(`


c, COMPLEX(B$1, $A2),

a, COMPLEX(0, 0),

b, IMSUM(IMPOWER(a, 2), c),

d, IMSUM(IMPOWER(b, 2), c),

e, IMSUM(IMPOWER(d, 2), c),

f, IMSUM(IMPOWER(e, 2), c),

g, IMSUM(IMPOWER(f, 2), c),

h, IMSUM(IMPOWER(g, 2), c),

i, IMSUM(IMPOWER(h, 2), c),

j, IMSUM(IMPOWER(i, 2), c),

k, IMSUM(IMPOWER(j, 2), c), `IF(IMABS(k) > 10,0,1)`


)

Even if you don’t know Excel, you may be able to read and understand this code. It creates the complex number from the entries in the left-most column and the top row, starts with the complex value 0, iterates it to get an orbit of length 10, checks to see if the last term is greater than 10, and then spits out a 0 (yes) or 1 (no). Below, you see the resulting output (I adjusted the row and column sizes so the cells were approximately square). Pretty good!


![](../../assets/0ff02481ecdbba88.png)


![](../../assets/0ff02481ecdbba88.png)

Once I saw that this proof of concept was successful, I started improving the design. For instance, I did the following. (I did some of this myself, as I’m familiar with some of Excel’s commands, and I asked ChatGPT for help with other parts.)

- I increased the size of my canvas (so the difference between the values was much smaller).
- I stopped the computation once the output value was larger (in modulus) than the chosen
value.

- I had the algorithm look at predetermined cells to find the
and

values. This allowed me to change them globally by changing a single value.

- Rather than putting a 0 or 1 in the cell, I had it put a period (.) for points in the Mandelbrot set and the number of steps required to become larger than
in modulus for points outside the Mandelbrot set.

- This last choice allowed me to add some color. If the cell had a period in it, I colored it black. If the cell contained a number, I had Excel’s conditional formatting color it. My settings are shown below.

![](../../assets/5e96396bc4d6707d.png)


![](../../assets/5e96396bc4d6707d.png)

Below, you’ll see the resulting Mandelbrot sets in a 30×30, 60×60, and 250×250 grid. For the largest one, I had to zoom out very far. Pretty amazing, right?

![](../../assets/b6aa6fe6cd746e0c.png)


![](../../assets/b6aa6fe6cd746e0c.png)

![](../../assets/20549341071febf4.png)


![](../../assets/20549341071febf4.png)

![](../../assets/dee7f55545a04de5.png)


![](../../assets/dee7f55545a04de5.png)

In the end, the code was pretty short. Here is the final code for cell B2 (the other cells are very similar). There was a lot of back and forth with ChatGPT to get it to do what I wanted it to do. I don’t think it could have worked if I wasn’t both familiar with the mathematics behind the Mandelbrot set and comfortable working with Excel. Still, I did not write this code. I was done largely by ChatGPT.

`=LET(`

`c, COMPLEX(B$1, $A2),`

`threshold, Parameters!$B$5,`

`maxIterations, Parameters!$B$6,`

`zArray, SCAN(`

`COMPLEX(0, 0),`

`SEQUENCE(maxIterations),`

`LAMBDA(prevZ,i,`

`IF(IMABS(prevZ) > threshold,`

`prevZ, IMSUM(IMPOWER(prevZ, 2), c)))`

`),`

`exceedIndex, XMATCH(TRUE, IMABS(zArray) > threshold, 0),`

`IF(ISNUMBER(exceedIndex), exceedIndex, ".")`

`)`


The last thing I did was to create a way to zoom in on specific areas of the Mandelbrot set. To do so, I created the following additional parameters:

- Center point (real part)
- Center point (imaginary part)
- Width of the region (this is also the height of the region)

I used these to compute the minimum real value, the maximum imaginary value, and the step size between rows and columns. I used this information to generate the numbering along the top and left of the spreadsheet.

Here are a few of the resulting images. Remember, these are all in Excel! (If you look closely, you can see some black dots—those are the numbers in the cells.)

![](../../assets/1e2692ad9c6f0079.png)


![](../../assets/1e2692ad9c6f0079.png)

![](../../assets/b1a655f800d73fb2.png)


![](../../assets/b1a655f800d73fb2.png)

![](../../assets/8598fc8ea937416d.png)


![](../../assets/8598fc8ea937416d.png)

![](../../assets/ccabf13a02200eb1.png)


![](../../assets/ccabf13a02200eb1.png)

![](../../assets/d3ce90c734291f0e.png)


![](../../assets/d3ce90c734291f0e.png)

![](../../assets/4b9647eba2b80dae.png)


![](../../assets/4b9647eba2b80dae.png)

If you want to play with this, download [the Excel file](https://divisbyzero.com/wp-content/uploads/2024/11/mandelbrotexcel.xlsx). Enter the parameters in the colored cells on the first tab. Then, view the resulting images in the other three tabs. Below are the parameters for the full Mandelbrot set. On the first tab of the spreadsheet, I’ve also included the parameters for the images shown above. Enjoy!

![](../../assets/6fc8264898896a2c.png)


![](../../assets/6fc8264898896a2c.png)

Nice example! One formatting trick that you might not know is that if you format a cell as ;;; (three semi-colons) then the contents of the cell become the same color as the background, i.e. the text becomes invisible.

Awesome! Thanks. I was wishing there was some feature like that. I’ll give it a try.