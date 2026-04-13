---
title: 'Fun with Vimgolf 1: Alphabetize the Directory'
url: https://www.masteringemacs.org/article/fun-with-vimgolf-1-alphabetize-directory
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I’ve been having a lot of fun with [vimgolf](http://www.vimgolf.com), a site where vim users try to complete certain tasks (sort this, format that, scrub this data, etc.) in as few keys as possible. It’s an interesting site and the problem set is varied and a good source of inspiration for Emacs blog posts. I learned about this site from [Jon’s Emacs blog](http://irreal.org/blog/) and I’ve been having a fun time solving the problems in Emacs.

It’s obvious to most of us that to attempt a “fewest possible keystrokes” exercise in Emacs will invariably end in tears, as we can’t compete against vim in that regard; but with that said, we do have a lot of tricks up our sleeve.

In reading – or attempting to, more like – the “solutions” I’ve made a few observations about most of them: they are tailored to the input, and that input only; thus, it wouldn’t necessarily scale to larger problem sets or even smaller ones. I’m going to try to solve these problems so they’re *technically correct* – the best *kind* of correct – and thus work with larger or smaller input.

## Alphabetize the Directory

Put the contacts and their information in alphabetical order.


So the task is simple. We need to sort by a key (the name heading), preserving the details associated with each contact.

The easiest way to solve this is to imagine the input below as an `org-mode`

file, so that’s what we’ll do:

`M-x org-mode`

and org mode immediately picks up on the file contents and collapses the headings.

Next, we need to sort the items, whilst we preserve the order of the subitems, and this is done by *first* moving to the heading level you want to sort by (in this case it’s the `Smith, George`

heading) and invoking `M-x org-sort`

and selecting `a`

for alphabetic sort.

Org mode will sort the file and the output should match the expected vim golf output. And that’s it.

### Input

```
## Directory
* Smith, George
- 1234 Avenue, New York, NY
* Bailey, Stephen
- 4545 Harbor Ln, Atlanta, GA
- Phone: (412) 291-1238
* Thomas, Brent
- 1482 Mystic Oaks, Anaheim, CA
* Grant, Jenny
- 198 Circle Dr, Houston, TX
- Phone: (213) 198-9842
- Email: jenny.grant@gmail.com
* Percy, Adam
- 221 Jaguar Pkwy, Missoula, MT
* Garfield, Misty
- 5988 Apple Tree Ln, Memphis, TN
* Parsons, Betty
- Phone: (235) 523-2378
- Email: bettyboop123@gmail.com
* Sanders, Terry
- Email: sanderst@yahoo.com
* Smith, Pete
- Phone: (294) 984-2938
* Frost, Jennifer
- 2498 Temple Terrace, Miami, FL
* Matthews, Frank
- 418 Happy Trail, Phoenix, AZ
- Phone: (985) 129-2394
- Email: frank@phoenixrealtors.net
* Allen, Taylor
- Email: allen.taylor@hotmail.com
* McCullen, Sarah
- 247 Hidden Elm, Seattle, WA
- Phone: (288) 283-4568
* Perkins, Mike
- 992 Peartree Ln, Bowling Green, KY
```


### Expected Output

```
## Directory
* Allen, Taylor
- Email: allen.taylor@hotmail.com
* Bailey, Stephen
- 4545 Harbor Ln, Atlanta, GA
- Phone: (412) 291-1238
* Frost, Jennifer
- 2498 Temple Terrace, Miami, FL
* Garfield, Misty
- 5988 Apple Tree Ln, Memphis, TN
* Grant, Jenny
- 198 Circle Dr, Houston, TX
- Phone: (213) 198-9842
- Email: jenny.grant@gmail.com
* Matthews, Frank
- 418 Happy Trail, Phoenix, AZ
- Phone: (985) 129-2394
- Email: frank@phoenixrealtors.net
* McCullen, Sarah
- 247 Hidden Elm, Seattle, WA
- Phone: (288) 283-4568
* Parsons, Betty
- Phone: (235) 523-2378
- Email: bettyboop123@gmail.com
* Percy, Adam
- 221 Jaguar Pkwy, Missoula, MT
* Perkins, Mike
- 992 Peartree Ln, Bowling Green, KY
* Sanders, Terry
- Email: sanderst@yahoo.com
* Smith, George
- 1234 Avenue, New York, NY
* Smith, Pete
- Phone: (294) 984-2938
* Thomas, Brent
- 1482 Mystic Oaks, Anaheim, CA
```