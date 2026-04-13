---
title: 'Burnt Paper plugin for GIMP :: nklein software'
url: http://nklein.com/2010/02/burnt-paper-plugin-for-gimp/
author: Pat
published: '2010-02-16'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

Yesterday, I decided to make the images in [my article](http://nklein.com/2010/02/finding-the-perfect-hyperbola/) look like they were on old, burnt paper. I did this manually in [the GIMP](http://gimp.org/).

I liked the effect, but I didn’t want the tedium of having to do all n steps manually next time I go to use it. So, I wrote a GIMP plugin script to do it.

Here is an example of the plugin script in action. As you can see, I started with a text layer and a selection that was bigger than the text layer. The plugin uses the selection size as original edge of the paper (original, as in before the paper was burned).


![original-image](../../assets/08aec131ebf2b993.png)


![original-image](../../assets/08aec131ebf2b993.png)

And, here is the resulting image:


![final-image](../../assets/3f5d95a28e69e0b7.png)


![final-image](../../assets/3f5d95a28e69e0b7.png)

Here is the [Burnt Paper plugin script](http://nklein.com/wp-content/uploads/2010/02/burnt-paper.scm). Plop this in a directory that’s in your script search path and refresh GIMP’s scripting and then you’ll find it in the Filters > Decor

menu. [You can see the script search path by going to Edit > Preferences

and selecting Scripts

under Folders

in the left sidebar. And, you can refresh the scripts by going to Filters > Script-Fu > Refresh Scripts

.]

Sweet! Love the script. But you need to add the source file back at the registry.gimp.org. (It’s missing) 🙂

I had included a link, but the link got stripped on me. Oops. I’ve attached it over there now.

Patrick,

I left a comment on the Registry about the script. Basically (I’m not a coder, btw) it would be cool if we could opt to add a different texture or choose to not have a texture at all. For instance, check out my “pirate map” here: http://www.mahvin.com/?p=1720. It would be nice to just use the burnt paper effect without any texture or text.

Thanks for any consideration in advance. 🙂

mahvin

I really like your wrinkle work there. Awesome. Yes, I had planned on making the texture optional. I will add that… and, I may add your wrinkle effect as an option, too.

Thanks,Patrick. Your work is appreciated. 🙂

Hi Patrick:

Just checking in to see how things are going. Have you been busy? Still looking forward to the future updates of this burnt paper script, but no pressure. 🙂

mahvin

I have been busy, but I did upload a new version of the script, I think. I at least wrote a new version, and think I updated the GIMP registry. Erf. I won’t get a chance to check today.

The link on this page seems to be the newer version.