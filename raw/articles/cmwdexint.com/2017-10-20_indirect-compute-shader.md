---
title: Indirect Compute Shader
url: https://cmwdexint.com/2017/10/20/indirect-compute-shader/
author: Ming Wai Chan
published: '2017-10-20'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

Direct means CPU tells GPU to execute work, amount of work is given by CPU


Indirectmeans CPU tells GPU to execute work, amount of work is calculated in GPU


Scenario:

I have a maximum no. of cats (say 10000 cats).

Since they all get hungry at different times so I should only feed the cats that are hungry.

Steps:

![Compute Buffer and Compute Shader (20170703)](../../assets/45289576617364da.png)


- CPU creates 2 compute buffers.
**Data buffer**knows it can takes up to 10000 data.- Data buffer : no. of cats = 0

- CPU pass the number 10000 to GPU to run the direct dispatch, which will add the hungry cats to
**data buffer**.**Data buffer**: no. of cats = no. of hungry cats

- So now we have hungry cats filtered out!
- Pass the no. of hungry cats from
**data buffer**to**args buffer**. So that we know we have to feed how many cats. - Run indirect dispatch according to no. of hungry cats from
**args buffer**. That is, too feed them!


From the arrows in the diagram you can see there is no read or write data back to CPU (which wastes time and resources) during the whole cat filtering and feeding process. It’s very good isn’t it :D?


Download [unity package](https://drive.google.com/open?id=0BwLgUykgFtANaFBmT1JaTi14NXM) to try it out 🙂 or visit [https://github.com/cinight/MinimalCompute](https://github.com/cinight/MinimalCompute)


## One thought on “Indirect Compute Shader”