---
title: Sprite Encoding / Decoding Using Literals
url: https://www.4rknova.com/blog/2017/01/01/sprite-encoding
author: Nikolaos Papadopoulos
published: '2017-01-01'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

The following is a simple, comprehensive guide that explains in plain terms how literals can be used to encode / decode sprites within a fragment shader.

# The Bigger Picture

For the time being we will limit our efforts to encoding monochrome sprites. A pixel in a monochrome bitmap can be either on or off (black or white) which means that we only require a single bit of memory to store each pixel’s value. The size of an signed integer in glsl 1.3 or later is 32-bits [1] which in theory means that we can use a single integer to store 31 pixels in the form of a literal. In practice since we are going to be using floats and due to the nature of the mathematical operations involved, we can only use 24 bits

.

[[3]](https://www.4rknova.com#REF-3)# Encoding

Our goal here is to break the sprite down into small blocks of 24 pixels and then encode each block with an integral value. There are a few options regarding the exact dimensions of the blocks. Consider the following 4x6 bitmap which contains the character ‘l’ and is part of a very simple font sprite.

![01](../../assets/bad125de8f1ba3f3.png)


```
0100
0100
0100
0100
0100
0110
```


The equivalent literal in binary is 010001000100010001000110 which is equal to the value 4473926 in decimal. An alternative way to deal with encoding is do it on the fly. The following macro will encode a 1x16 block with 2 bits per pixel.

```
Q(i,a,b,c,d,e,f,g,h) if(y==i)m=(a+4.*(b+4.*(c+4.*(d+4.*(e+4.*(f+4.*(g+h*4.)))))));
```


The first argument (i) is the row index which selects the row to sample from when using multiple blocks, ‘y’ is the current row index and ‘m’ contains the muxed row data. For each pixel with index n we multiply by 4 (n times) to shift the pixel data 2 bits to the left at a time and then blit the value in place by summation.

# Decoding

Now that we know how to encode the sprite blocks, we need to figure out how to decode them as well. Normally we would do this by shifting the bits to the right and then using a bitwise AND operation along with a mask to extract a single bit or a group of bits. In c that would look something like:

```
int b = (v >> k) & 1;
```


where v contains the literal that encodes the block data and k is the index of the single bit we wish to extract. The problem with the above is that bitwise operators are not available in GLSL, so we need to find another way of extracting the bit values. We’ll break the problem down to two steps.

Shifting This is easy to solve as all we have to do is divide by 2 to shift once to the right, or the nth power of 2 to shift by n bits.

Masking For positive values of x, the following is true [2]:

```
x % (2^n) == x & ((2^n) - 1)
```


Therefore for n = 1, we get:

```
x % 2 == x & 1
```


which will extract the first bit.

Combining the two together, we can retrieve the nth bit from the encoded data using the following formula:

```
(v/(2^n))%2
```


# The Grid

The only thing that remains to be solved is how to determine which bit needs to be extracted for the pixel that is being shaded. The solution to this problem is simple. We quantize the screen space to a scalable grid and then use the cell coordinates to determine the index of the bit to extract.

As we are potentially dealing with multidimensional arrays, the correct index should be calculated.

## Interactive demo

# The Block Size

As mentioned above, there are a few options regarding the dimensions of the sprite blocks. We could use 1x24, 4x6 or 6x4 blocks or even add a 3rd dimension in a 4x3x2 arrangement to store a second frame as well for animation purposes. Equally, we could use a 4x5 block and reserve the remaining 4 bits to store some sort of metadata.

# Adding Color

In order to add colors we can use multiple bits per pixel to store a palette index or a threshold value. The process is exactly the same with the only difference that we now need to extract 2 or more bits instead of a single one [4]. Keep in mind that we can only use powers of 2 with modulo when masking.

# Other Tricks

For sprites that are symmetric, we can mirror the pixels and reduce the memory footprint [7].

![02](../../assets/87afdd9f45e6468d.png)