---
title: FMTT, GLSL Edition
url: http://hacksoflife.blogspot.com/2010/12/fmtt-glsl-edition.html
author: Benjamin Supnik
published: '2010-12-09'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[I Hate C](http://hacksoflife.blogspot.com/2010/11/i-hate-c-part-492.html)-- all of its derivatives are contaminated with its brain damage.

`gl_FragData[0] = vec4(tex_color.rgb * gl_Color.rgb*tex_color.a,clamp(tex_color.a + lit_color.a,0.0,1.0)); `

gl_FragData[1] = vec4(shiny_ao * cut_pos, cut_pos*position_eye.z/-1024.0, 0.0, cut_pos);

gl_FragData[2] = vec4(normal_eye_use.xyz*cut_pos, cut_pos);

gl_FragData[3] = vec4(lit_color.rgb + tex_color.rgb * gl_FrontLightModelProduct.sceneColor.rgb, (tex_color.a + lit_color.a,0.0,1.0));


## No comments:

## Post a Comment