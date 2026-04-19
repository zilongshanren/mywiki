---
title: Temporal Reprojection and SAO
url: https://bitsquid.blogspot.com/2015/09/temporal-reprojection-and-sao.html
author: Upplagd av Jp
published: '2015-09-10'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

We've recently re-visited our AO solution with the goal of improving its performance on consoles. We currently use the




If we add an offset to a single AO sample we can see that after 2π it repeats (as expected)




So we use 8 samples ranging from [0, 2π] distributed by using the first 8 terms of a base 3 Halton sequence: {1/3, 2/3, 1/9, 4/9, 7/9, 2/9, 5/9, 8/9} x 2π




And this is the result using 6 AO samples.




Notice that there is some banding that can appear. By adding a dithered offset to the current sample's radius we can remove this quite nicely. We use a 4x4 pattern based on the




And here are our samples distributed through time. If anyone has a better way of distributing these I would be very interested to know.






This is a simple term which identifies depth differences and classifies previous pixels as disoccluded. We use the relative depth difference described by Huw Bowles in







To try and invalidate samples associated with fast moving object, the Dangerous Samples term is accumulated through time. An idea described quite well by Oliver Mattausch in his




Here's the kind of ghosting we get without identifying 'dangerous' samples.




With this term as part of the reprojection function we can eliminate most of the ghosting that arises from the temporal reprojection:





Well, that's it! Nothing too ground breaking but I thought I'd share. If anyone has ideas or suggestions on how to improve any of this please let us know!

[Scalable Ambient Obscurance](http://graphics.cs.williams.edu/papers/SAOHPG12/)algorithm presented by Morgan McGuire. Out target was to bring down the cost of the entire effect to something between 1-1.5ms on Xbox One. To achieve this it was clear that we needed to reduce the number of taps we were taking for each AO sample. An important part of this work went towards improving the efficiency of the temporal reprojection of our AO buffer. I thought I'd share a few observations we've made along the way.## Distributing AO Samples

When reprojecting data the key to success is to make sure your samples are well distributed through time. The[Halton sequence](https://en.wikipedia.org/wiki/Halton_sequence)was made popular for reprojection methods after Brian Karis presented his[High Quality Temporal Supersampling](http://advances.realtimerendering.com/s2014/index.html#_HIGH-QUALITY_TEMPORAL_SUPERSAMPLING). It is a sequence that gives well distributed samples in space as well as in time.If we add an offset to a single AO sample we can see that after 2π it repeats (as expected)

So we use 8 samples ranging from [0, 2π] distributed by using the first 8 terms of a base 3 Halton sequence: {1/3, 2/3, 1/9, 4/9, 7/9, 2/9, 5/9, 8/9} x 2π

And this is the result using 6 AO samples.

Notice that there is some banding that can appear. By adding a dithered offset to the current sample's radius we can remove this quite nicely. We use a 4x4 pattern based on the

[Bayer matrix](https://en.wikipedia.org/wiki/Ordered_dithering).And here are our samples distributed through time. If anyone has a better way of distributing these I would be very interested to know.

## Reprojection function

When doing any temporal reprojection it is crucial to have a good reprojection function. I like to refer to this as a similarity function. Its purpose is to identify how likely it is that the reprojected samples correspond to the samples of the current pixel. When writing this function it's quite important to have a convenient way to visualize it. If the function gets complicated, it's a good idea to isolate the different terms of the function so that you can reason and debug them individually. The reprojection function we use is a combination of three main terms.### Disocclusion Term

[Iterative Image Warping](http://www.disneyresearch.com/wp-content/uploads/Iterative-Image-Warping-Paper.pdf).`depth_similarity = saturate(pow(prev_depth/current_depth, 4) + DEPTH_MIN_SIMILARITY);`


### Velocity Term

The second term is also very straight forward and consists simply of reducing the similarity for fast moving pixels. A moving pixel has less chance of reprojecting successfully than a still one.`velocity_similarity = saturate(velocity * VELOCITY_SCALAR);`


### Dangerous Samples Term

The idea is to identify if the AO samples we are gathering are touching moving objects. To do this efficiently, we encode a moving bit as part of the depth buffer info passed in to the SAO algorithm. If you use the mip chain described by the SAO paper, make sure that you forward that 'moving bit' to the lower levels of the mip chain. This idea was presented by Anton Michels during the[Labs R&D: Rendering Techniques in Rise of the Tomb Raider](http://s2015.siggraph.org/attendees/talks/sessions/labs-rd-rendering-techniques-deus-ex-mankind-divided-and-rise-tomb-raider)presentation earlier this year. Since each AO sample will need to read the depth information we get the 'moving bit' read for free.```
samples_similarity = saturate(num_moving_samples * MOVING_SAMPLES_SCALAR);
samples_similarity *= (LOW_VELOCITY_SIMILARITY - MOVING_SAMPLES_MIN_SIMILARITY);
samples_similarity = lerp(samples_similarity, prev_samples_similarity, 0.9);
samples_similarity = min(samples_similarity, current_samples_similarity);
```


To try and invalidate samples associated with fast moving object, the Dangerous Samples term is accumulated through time. An idea described quite well by Oliver Mattausch in his

[TSSAO Gpu-Pro2 article](https://www.cg.tuwien.ac.at/research/publications/2011/matt2011/)which he called 'smooth invalidation'.Here's the kind of ghosting we get without identifying 'dangerous' samples.

With this term as part of the reprojection function we can eliminate most of the ghosting that arises from the temporal reprojection:

## Putting it all together

The final similarity term is calculated by combining all terms together.```
similarity = depth_similarity * LOW_VELOCITY_SIMILARITY - velocity_similarity;
similarity *= (LOW_VELOCITY_SIMILARITY - HIGH_VELOCITY_SIMILARITY);
similarity = saturate(similarity - samples_similarity);
```


Well, that's it! Nothing too ground breaking but I thought I'd share. If anyone has ideas or suggestions on how to improve any of this please let us know!

None of these images are working for me :/

ReplyDeleteThey're hotlinked to dropbox which returns HTTP 429 (Too Many Requests) for excessive use.

DeleteShould work now (I uploaded the images to blogger directly). Thanks for letting me know!

DeleteHi,


ReplyDeleteis your code available somewhere? I'm struggling with exponential smoothing of GTAO and I could use some reference implementations.

Could you please elaborate on the "moving bit" from the Dangerous Samples part?



ReplyDeleteThe TSSAO paper mentions that we should compare all depth samples with their equivalents from the previous frame so this pretty much doubles our texture tap count! Is this right? You've mentioned that we'll have this "moving bit" for free, how exactly did you accomplish that?

The Tomb Raider paper is nowhere to be found (even the paid ones are incorrect!) so I can't even check what Anton had to say about it.

Thanks!

Catering Piknik

ReplyDeleteistanbul catering

kokteyl catering

Mevlüt Yemekleri fiyatları

Mevlüt yemek Menüleri

kokteyl catering fiyatları

istanbul kokteyl catering

catering kokteyl menüleri

fuar yemek organizasyon

fuar yemek organizasyo firmaları

fuar için yemek firmaları

düğün yemek organizasyonu

düğün yemek organizasyonu yapan firmalar

istanbul kokteyl catering

istanbul kokteyl catering firmaları

Kokteyl catering fiyatları

kokteyl prolounge menu

kokteyl prolounge düğün

Paketli Mevlüt yemekleri

Düğün ve Mevlüt Yemekleri

Kokteyl Prolounge Menu

Mevlüt yemeği nedir

Pideli Mevlüt menüsü

Cenaze Yemek Organizasyonu

300 kişilik yemek Fiyatları

istanbul fuar yemek organizasyonn

istanbul fuar yemek organizasyo firmaları

istanbul fuar için yemek firmaları

istanbul düğün yemek organizasyonu

istanbul düğün yemek organizasyonu yapan firmalar

istanbul kokteyl prolounge menu

istanbul kokteyl prolounge düğün

istanbul Paketli Mevlüt yemekleri

istanbul Düğün ve Mevlüt Yemekleri

istanbul Kokteyl Prolounge Menu

istanbul Mevlüt yemeği nedir

istanbul Pideli Mevlüt menüsü

Your work is great. Yellowstone Coat

ReplyDeleteWOW! I Love it...


ReplyDeleteand i thing thats good for you >>

MOVIE TRAILER Slot Machine The Third Eye Opening Experience

Thank you!

google 3071

ReplyDeletegoogle 3072

google 3073

google 3074

google 3075

google 3076






ReplyDeleteufafc

Webroot SecureAnywhere on webroot.com/secure.Webroot.com/secure antivirus gives internet security and offline security to your devices for

Hello Sir I saw your blog, It was very nice blog, and your blog content is awesome, i read it and i am impressed of your blog, i read your more blogs, thanks for share this summary.

ReplyDeleteFacebook Not Working Properly

Good Post! Thank you so much for sharing this pretty post, it was so good to read and useful to improve my knowledge as updated one, keep blogging.


ReplyDeletecheck here

Iwas more than happy to find this site. I want





ReplyDeleteto to thank you ffor your time for this particularly

wonderful read!! I definitely savored every little bit of it and i also have yyou saved

aas a favorite to check out new stuff in your website.

카지노사이트

온라인카지노

카지노사이트추천

Have you ever considered writing an e-book or guest authoring on other sites? I have a blog centered on the same information you discuss and would love to have you share some stories/information. I know my audience would enjoy your work. If you are even remotely interested, feel free to send me an e-mail





ReplyDelete카지노사이트

바카라사이트

카지노사이트홈

Airtel tower installation and complain office

ReplyDeleteRegistration open for Airtel mobile tower installation 2022

Submit Airtel tower complaint online & get solved in 24hours

Airtel tower rent per month (Rural and Urban area in 2022)

Documents require for Airtel mobile tower installation

Airtel tower installation complaints or its complaint number

Airtel tower installation customer care number & contact no

Airtel tower agreement letter & Airtel tower approval letter

Airtel Tower Office - Airtel tower installation and complain

ReplyDeleteSubmit Airtel tower complaint online & get solved in 24hours

Registration open for Airtel mobile tower installation 2022

Airtel tower head office contact number and helpline number

Airtel tower rent per month (Rural and Urban area in 2022)

How to Bharti airtel tower installation apply online?

Airtel tower agreement letter & Airtel tower approval letter

Airtel tower installation complaints or its complaint number

Airtel tower installation customer care number & contact no

best golf clubs for beginners,best golf clubs for men,best golf clubs for women,best golf clubs for the money,best golf clubs for starters,golf galaxy,best golf clubs for intermediate player

ReplyDeletegood spoa spa near me body to body ameerpet


ReplyDeleteSuch an insightful read, thank you!

ReplyDelete