---
title: Enhance this!
url: https://c0de517e.blogspot.com/2013/12/enhance-this.html
published: '2013-12-08'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Don't you hate when people have strong critiques towards a thing, but it happens that it's just that they don't know enough about it? Well, I don't, because then I think of how many times in my youth (and let's say only then) I did the same...

Regardless, today I happen to have a bit of time and I saw yet another post laughing at how stupid the "image enhance"

[trick used in movies and TV series](https://www.youtube.com/watch?v=LhF_56SxrGk)is, and so you get this nerdrage against nerdrage...
Now think a second about this. Who do you think it's right? C.S.I., which is a huge TV series using arguably some of the best writers and consultants, or the random dude on the net? Do you think they don't know how realistic any of the techniques they use is?


Do you think they don't actually and very carefully thread between real science and fiction to deliver a mix that is comprehensible and entertains their audience, telling a story while keeping it grounded in actual techniques used in the field? Don't you think -they- know better, and the result was very consciously constructed?


Do you think they don't actually and very carefully thread between real science and fiction to deliver a mix that is comprehensible and entertains their audience, telling a story while keeping it grounded in actual techniques used in the field? Don't you think -they- know better, and the result was very consciously constructed?

*Well, ok sometimes producers just don't care, they want to tell a story, not write a documentary, but more often than not that's not the case.*
The same goes of course for anything, really, especially when something is successful, makes a lot of money, has a lot of money behind, you should always bias yourself towards being humble and assuming the professionals making said thing -know better-.




Now, back to the "image enhance" trick. It turns out it is real science. It's called "super-resolution" and it's a deep field with a lot (really, a lot!) of research and techniques behind it.

It's actually common nowadays as well, chances are that if your TV has some sort of SD2HD conversion, well that is super-resolution in action (and even more surprising are all the techniques that can

[reconstruct depth from a single image](http://download.springer.com/static/pdf/739/art%253A10.1007%252Fs11263-007-0071-y.pdf?auth66=1386713453_fa1fa6f241bd34d34816eb73db514168&ext=.pdf), which also ship in many TVs, the kind of models they came up with for that are crazy!).
The scenarios presented in movies are actually -quite- realistic even if the details are fictionalized. True, the interface to these programs won't look like that, maybe they won't be real-time and surely they won't be able to "zoom" in "hundreds" of times, but they surely can help and surely are used.


That is to me a reasonable compromise between fiction and reality, as certainly you can and will use computers to get a legible nameplate for a video that is too low-resolution for the naked eye, or match an otherwise unreadable face against a database of suspects and so on, probably not in quite as glamorous and simple way as the movies show, but fundamentally the idea is sound (and I'm quite sure, used in the real world).


It is a non-realistic representation of a very realistic scenario, which is the best that good fiction should try to achieve, going further is silly. Or are you going to argue that a movie is crap because at night for example you can't really see as clearly as they show, or because they don't let a DNA test take weeks and an investigation several years?





When it comes to videos we can use techniques known as "multiple image" super-resolution, registering (aligning) multiple images (frames in this case, i.e. optical flow), and merging the results, which do work quite well. Also, most fictionalized super-resolution enhances focus on faces or nameplates, which are both much easier to super-resolve because we can "hint" the algorithm with a statistical model (a-priori) which helps tremendously to guide the "hallucination".

That is to me a reasonable compromise between fiction and reality, as certainly you can and will use computers to get a legible nameplate for a video that is too low-resolution for the naked eye, or match an otherwise unreadable face against a database of suspects and so on, probably not in quite as glamorous and simple way as the movies show, but fundamentally the idea is sound (and I'm quite sure, used in the real world).

It is a non-realistic representation of a very realistic scenario, which is the best that good fiction should try to achieve, going further is silly. Or are you going to argue that a movie is crap because at night for example you can't really see as clearly as they show, or because they don't let a DNA test take weeks and an investigation several years?

When it comes to videos we can use techniques known as "multiple image" super-resolution, registering (aligning) multiple images (frames in this case, i.e. optical flow), and merging the results, which do work quite well. Also, most fictionalized super-resolution enhances focus on faces or nameplates, which are both much easier to super-resolve because we can "hint" the algorithm with a statistical model (a-priori) which helps tremendously to guide the "hallucination".

And even if hallucinating detail might not hold in a court (the stronger the a-priori model, the more it will generate plausible results but by no means always reliable), it might be very well be used as a hint to direct the investigations (I've never seen a case where it was used in courts, always to try to identify a potential suspect or a nameplate, both cases where having a strong probability, even if it's far from certainty, are realistic).

So, bottom line is, if you think these guys are "stuuuuupid", well then you might want to think twice. Here are some random-ish links (starting points... google scholar for references and so on if you're interested... I couldn't even find many of my favorite ones right now) to the science of super-resolution:

[An example with nameplates, showing extreme reconstructions](http://www.nec.com/en/global/techrep/journal/g12/n02/pdf/120217.pdf)[Another blind deconvolution paper, seems great on car plates](http://arxiv.org/pdf/1209.2082v3.pdf)[Hallucinating faces](http://people.csail.mit.edu/celiu/FaceHallucination/fh.html)[An opensource implementation of video-based SR](http://mentat.za.net/supreme/)and a[commercial multiple-image SR implementation](http://www.photoacute.com/studio/examples/mac_hdd/index.html)[Video to video SR](http://research.microsoft.com/en-us/um/people/celiu/cvpr2011/), and[another one](http://www.vincentcheung.ca/research/videoepitome.html)...[Classic paper of single-image super-resolution](http://www.wisdom.weizmann.ac.il/~vision/SingleImageSR.html), trying to find similarities in the same image (to a degree, similar to fractal methods for image compression, which can indeed be used also for SR). Less strong results as the algorithm makes no prior assumptions.[Multiple cameras (i.e. surveilance)](http://spie.org/x14680.xml?pf=true&ArticleID=x14680)[More](http://asp.eurasipjournals.com/series/SUPER)and[more](http://www.ijcaonline.com/volume15/number2/pxc3872568.pdf)...[An overview of commercial software used in forensics](http://www.mecs-press.net/ijmecs/ijmecs-v5-n11/IJMECS-V5-N11-6.pdf)

It would take many pages only to survey the general ideas in the field. Don't limit your imagination... Computer science is more amazing than you might think... We





And by the way, don't bitch about

[reconstruct environments from multiple cameras](http://photosynth.net/preview/view/802c386c-110f-4bcf-bf7b-a4a18a4cc236), or even[sweeping video](http://csvision.swan.ac.uk/uploads/Main/ComputerVisionAndMedicalImageAnalysis/CGF2012RB.pdf)...[can capture](http://web.mit.edu/newsoffice/2011/trillion-fps-camera-1213.html)[light in flight](http://www.cs.ubc.ca/labs/imager/tr/2013/TransientPMD/), we can[r](http://www.youtube.com/watch?v=ONZcjs1Pjmk), fucking use[lasers to see around corners](http://www.popsci.com/technology/article/2012-03/video-how-mits-femtosecond-laser-camera-can-see-around-corners)and yes, even take some hints about an[environment from corneas](http://ii.ist.i.kyoto-u.ac.jp/~nitschke/Site/Research_files/CVA5-2013_CRAA_Paper.pdf)...And by the way, don't bitch about

## 15 comments:

I don't think that the researchers/technical consultants of those shows care anything about representing a shred of actual science. And even if they did, the writers and directors sure don't.





Most of the work you posted works using multiple images from the (almost) same viewpoint. Images in those shows usually come from single image cameras. That's quite a difference I would say.

There are gray areas of course, but when I see stuff like "rotate 22 deg around the x-axis" well...

And the worst part is (like so often) that simply showing the actual possibilities would be just as effective. Right now, computer science in popular media is used mostly as a gimmick. It would be nice if the viewer could assume realistic restrictions, so the writer would need to come up with something else than magic performed by the clichéd computer geek.

Anyways...It's alsways nice to see some enthusiasm :o)

"Now think a second about this. Who do you think it's right? C.S.I., which is a huge TV series using arguably some of the best writers and consultants, or the random dude on the net?"



http://www.youtube.com/watch?v=O2rGTXHvPCQ

I'm gonna go with "guy on the net", Alex

I will comment once and only once about this and then if you guys don't get it, whatever, let's agree to disagree and go be nerds and annoy everyone with silly "corrections".





Is it true that you can take stuff that is not visible to the naked eye and enhance it? Reconstruct a nameplate? Find the most probable guy out of a library of suspects with only a few pixels?

Then what? Are you going to argue that the process doesn't -exactly- look like that? That it requires twenty pixels instead of two or that they don't show that it's from video or whatever?

Then you would not enjoy any second of -any- work of fiction in -any- media, because it's all fictionalized, everything, you can find ten "wrong" things every frame by that logic. Feel free, if that's how you masturbate and feel smart.

The point is, image and video enhancement are fundamentally real and used by law enforcement. The actual details are fictionalized, yes, it's not quite exactly true that you can reconstruct a face out of three pixels from an iris of a guy, but you could out of a few more, its inspired by real technology used in the field...

So well, that's it.

Anonymous: I wouldn't extend this to mean that -all- TV series are grounded in real science. I don't like Numb3rs either, it hinges on the fact that nobody knows math and so they can go wild on it.




There is a difference between things presented as real, but that don't have a chance in hell to be related to real science, and things that are actually based in real science, really used, but just fictionalized in their depiction.

Again. Does law enforcement use super-resolution? Yes. Can it take something unrecognizable and identify it to surprising effects, far from what humans can do? Yes. These are facts and science. How they are then transposed to the screen is up to them...

I'd say there are reasons to approach things humbly if you're not an expert, research them, you might be surprised...

I think you've talked yourself into being too trusting of Hollywood TV shows. Just because a show has consultants doesn't mean it's accurate, or even somewhat accurate. I know people in the field of forensics and crime scene investigation and they say most of the techniques/science in these shows is hopeless nonsense, and that the shows almost always ignore what little input they request from their consultants.


Re: enhancing images: it's definitely interesting that some of the stuff in these TV shows is possible, but that doesn't make everything immune from criticism. I'm still going to be annoyed when a TV show has a computer predict e.g. the color and style of somebody's hair based on an image where his head is covered, etc.

No, I don't mean to say that because there are consultants everything is right.



I just mean to say that if it's not your field of expertise (and all these people bitching about image enhancement clearly are not really experts in superresolution and forensics) you'd better be humble and do some research.

Because they have consultants, there is input, and it turns out they might be more right than you might think.

You might be giving the general public too little credit. The way "image enhancement" is usually faked on TV shows is obviously to start out with a nice, high-resolution image and then pixelate it in Photoshop to create the "unenhanced" version. When the lead actor barks "enhance!" they just switch it to the original, pixel-perfect image. The layperson is not wrong to roll their eyes at this obvious bulls***.

First of all, the general public and the layperson doesn't give a shit and that's why these shows can not care about the nerd being nerds.





That said, so now the issue is something like this: "hah, man, that's ridiculous, you know, even if police does use computers to do surprising image enhancements they don't look anything like that! I mean com'on, give me a break, that's clearly a photoshop pixelate inverted, they are not even using the actual forensic software! Faaaaaaake!"

If this sounds right to you (or to anybody else) then let's agree to disagree and keep up the good fight.

I'd suggest to add to your repertoire classics such as "man, people don't wake up with such tidy hair" or "hey, at night you can't see so clearly!", or why not noticing how people falling from buildings splat in more graphic ways, gun wounds are not accurate, oh, oh, wait, the UI of any computer ever! They are all wrong! And why people are always so attractive in these series huh!

Wow, your eyes will be rolling at a million RPM!

>> I'd suggest to add to your repertoire classics such as "man, people don't wake up with such tidy hair"



Point taken. (Although I often do roll my eyes at the sorts of things you mention; maybe that's why I avoid CSI and its ilk.) From another angle, though, you're saying that a large number of people are being unjustifiably arrogant when they call BS on something that actually is BS. Do you think that's deserved?

I would have enjoyed your post very much and not taken issue with it at all if it was framed as "hey, some of this stuff actually IS possible!" rather than "most people (other than me) need to be more humble and here's why."

I'm not known to frame my posts in the least irritating way possible :)








But bottom line what I'm saying is that certain times we "jump" to the BS scream without really knowing better.

It really happens all the times, I don't know if you are a gamedev, but if you are chances are that you see all kind of people saying of things you made or anyhow really know some shit about, extremely strong, entitled opinions that are wrong, wrong in a way that they were even maybe tried and discarded and so on...

In general we are too entitled and too ignorant. Can make an example, first that comes to mind, COD:Ghosts space scene, people saying "duh, dumb, pistols don't fire in space, there's no air", like they have a PhD, when it's clearly just having a tiny bit of information (combustion needs air) but quite not enough... Now, of course that scene is fictionalized (you would spin like crazy!) but still...

It's just a plead to start in a "default" state of thinking -this is not my job, so maybe they are into something- and googling, instead of thinking -oh bullshit-. Then maybe 99 times it is BS, and once you'll be surprised that it's actually quite inspired by real stuff you didn't know...

On top of this, there is a discussion about how much freedom people should deserve when making fiction and how much we should rest and enjoy instead of actively trying to poke holes.

Now, these holes might be in your face (like with numb3rs) but a lot of times I would say they are not, they are "forgivable" and not worth bitching because they actually make for a better story. The "image enhance" is a good example of this, there is some real science and then yes, the writers take some liberties...

Which is fine. Would you think that if they accurately portrayed that or dunno, DNA tests and so forth, it would be more entertaining, or less? I doubt that DNA matches show in a cute interface with waveforms or whatever shit it's commonly employed, but, it is a show, it has to look nice and be easy to understand and "wow" people, cut them some slack...

Another example of this that comes to mind is Matrix and how it's impossible to create energy from humans... Now, this is a Sci-Fi movie, so people should really shut up, but still you see them saying "oh, this is so duuuumb". I've even read somewhere that initially they thought of breeding humans as computing resources, using their neurons to augment the machine AI and stuff... which would have been more credible... and they dropped it why? Because they saw that most people would not understand a shit of that and that the human-feeding-human thing was much more emotionally strong...

Same dunno, with Gravity... yes, it's impossible to fly out with a fire extinguisher and yes astronauts aren't sexy and what about the magical pull-force on Clooney? Well, it is telling a story, they are devices to signify something else, it's not really about astronauts right? It's a personal journey... Plus, if people are really smart they should use their smarts to try to figure maybe ways to "fix" stuff instead of breaking or bitching, for example, and I didn't go back to verify it, but I've heard people saying maybe the pull was because the station was spinning and the camera is just following the spin...

So now I've written way much more than I should have, but I hope it's clearer. It's not really to say "nerds are dumb" even if certain ways can be -really- -fucking- -annoying-. It's more to say, maybe next time think twice because you will be surprised at what you can learn (what the heck, even I didn't know the latest in research about corneal imaging before I saw a CSI snippet on youtube talking about it!) and think if they're taking some liberties to make a good story and a better exposition, or it's just lazy and bad entertainment...

"Which is fine. Would you think that if they accurately portrayed that or dunno, DNA tests and so forth, it would be more entertaining, or less?"



I think you meant this question as rhetorical but the answer isn't obvious to me at all. There are TV shows that are very realistic and I find them MUCH more entertaining, interesting, and insightful than the glossy overproduced bulls*** that the networks make for prime time. The Wire, for example, is excellent, as is the original Law and Order (not the spinoffs), if you are looking for crime dramas.

BTW, according to my friends in forensics and law enforcement, CSI and similar shows have made their jobs much more difficult because juries have extremely unrealistic expectations of fingerprints, DNA evidence, etc. because of these make-believe TV shows.

Now we're drilling it down to a matter of taste... Which is fine, their testament to how "tuned" they are to taste, as for any product, is success, so I guess they are not bad in knowing their audience, but taste is personal and everything is fine there...




But see, this is a different, thing, from "bullshit" to "taste". To a degree I would say that all fiction is exaggerated depictions, I mean, if you think "this is quite a stretch" then it's probably ok, because really most real reality is boring! But you might prefer more documentary stile, it's fine, that's not my point.

About CSI making forensics "harder", that's funny, I wonder if House made the same impact on doctors or Suits on lawyers... Anyhow, I surely love House and enjoy Suits!

Even there is the same, I've heard from medical students (I know squat about that) that the stuff shown in House is quite based on actual science and even the sequence of tests and hypothesis are all quite plausible, even if it's quite implausible in all the details, in how fast things go and of course in fact that he gets all kind of coincidences and weird cases that would have an incidence of one in a billion...

"But see, this is a different, thing, from "bullshit" to "taste". To a degree I would say that all fiction is exaggerated depictions, I mean, if you think "this is quite a stretch" then it's probably ok, because really most real reality is boring! But you might prefer more documentary stile, it's fine, that's not my point."


Just because a show doesn't have instantaneous DNA analysis and unrealistic image enhancement doesn't mean it's boring. There are other issues to consider: characters, plot, stuff like that. I would suggest you watch The Wire if you haven't already. It's hardly a documentary.

Agreed, it doesn't have to, but it's entirely a stylistic choice and a taste choice and so on.



I haven't seen the wire, but I understand that you can have a show where you don't oversimplify technological aspects.

Maybe they do exaggerate other stuff, or maybe they don't, you can have entertainment even with a very very realistic depiction of things, I agree.

But all this is about style and so on, it's all very fine. We're miles from what I wanted to say in the article. It's fine to not -like- a stylistic choice, but that's it, it's not bitching about how "stupid" these writers are and how "impossible" these techniques are (which aren't).

Like people can prefer Arma and Operation Flashpoint or other simulators to Call of Duty, but I hope it's clear the difference between a preference and writing on youtube "weapons don't fire in space, you dumb mofos!!!" thinking of being a scientist...

Meanwhile: "Identifiable Images of Bystanders Extracted from Corneal Reflections"

http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0083325

Post a Comment