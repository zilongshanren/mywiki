---
title: Procedural texturing for hand-painted stylized character pipelines
url: https://www.gamedeveloper.com/art/procedural-texturing-for-hand-painted-stylized-character-pipelines
author: Marit Cornelisse
published: '2019-12-18'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Procedural texturing for hand-painted stylized character pipelines

This article is about my research into procedural texturing pipelines that can achieve a hand-painted look, compared to the typical application of proceduralism for texturing that focuses on creating realistic effects.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

This article is about my research into procedural texturing pipelines that can achieve a hand-painted look, compared to the typical application of proceduralism for texturing that focuses on creating realistic effects. Is it even a good idea yet to use procedural effects when seeking a hand-painted finish? If it is a good idea, what is preventing this being the common approach across our industry?

The use of procedural texturing has become more popular for characters in recent years, and this is most apparent for realistic characters. It’s still not so common for hand-painted stylized characters. As I really like the benefits of procedural texturing, I kept wondering if it could be translated properly to a more hand-painted look. As such I decided to focus my thesis on procedural tools for hand-painted stylized character pipelines. My research question ended up being: “What barriers prevent the common adoption of procedural tools in hand-painted stylized character texture pipelines?”

During my literature review it became apparent that there is not a lot of academic writing on the subject and I had to rely on non-academic writing. Existing academic writing is often focused on computer sciences, not so much 3D game art. Game art also has very poor terminology, so even if the academic writing exists, it’s incredibly hard to find, as art styles rarely have well known, established, and specific names. The closest definition I came to the art-style used by games such as World of Warcraft, League of Legends, Battlerite, Darksiders, Torchlight, Heroes of the Storm and to a lesser degree Dota 2, Smite, Warhammer 40k and Diablo 3 was ‘hand-painted stylized’. The style is commonly used with albedo/diffuse maps only, often lacking specular maps, normal maps or PBR shaders, however it is not impossible to use these maps within this style.


The benefits

One of the major benefits of procedural texturing is that it’s driven by mathematical equations or algorithms. This means that the image can be of infinite resolution while being minimal in file size. Unfortunately this benefit is nullified for games, as game engines generally only accept bitmap images as textures.

However there are more benefits to procedural texturing. Because the formula is a ‘record’ of the process or procedure, significant changes can easily be made and immediately updated. Adjusting the formula is also non-destructive, as you are not un-doing or erasing hours of manual painting, you simply change parameters for different results.

Finally, once a formula has been made it can be easily reused for different assets, significantly speeding up the texturing process. Particularly the last benefit is why I’m interested in using procedural texturing for non-realistic characters. The term ‘hand-painted stylized’ may imply that it must always be painted by hand, but an alternative method may emulate the look and feel of hand-painted while offering different benefits. These benefits may be ideal for different projects.


How much is procedural texturing being used?

Procedural texturing software is currently primarily being used for realistic characters and rarely for hand-painted stylized characters. In October 2018, I searched through Substance Share, which is the user-submitted library of the industry standard procedural texturing software ‘Substance Designer’. I used the search term ‘stylized’, and only 78 files showed up out of several thousand.

While ‘realism’ only results in 18 files, it is important to note that under the category ‘materials’ and ‘smart materials’ the majority were visually aiming for realism. It appeared that ‘realism’ was the implied purpose of using procedural techniques in the first place.

Secondly, when searching for “substance designer texture” on the Google search engine, most of the results aim for realism, despite the key words not implying a bias to either realism or stylisation. Additionally, among the list of clients of Allegorithmic, Blizzard Entertainment (developers of World of Warcraft), Riot Games (developers of League of Legends), Valve (developers of DOTA 2) and Stunlock Studios (developers of Battlerite) were all absent. Three of these companies (Blizzard Entertainment, Riot Games & Stunlock Studios) are listed as clients for the 3DCoat software instead. While 3DCoat does have increasing support for Smart Materials, its workflow is ideally suited to creating hand-painted effects.

'Substance designer texture' search results example |


Research methods

After I gathered the previous information, I established my research methods and I settled on 3 research methods: using procedural texturing, an online survey, and interviews. The creation of an artefact was required for my degree, and so I decided to texture one character using procedural tools. This practical test served multiple purposes: it verified the available information from others regarding the use of procedural texturing for hand-painted stylized characters, and information acquired from the texturing process was used to ask more in-depth questions during interviews. If the process was successful, the documentation could be used by the industry as a step by step guide to create more assets using procedural texturing in the future. The documentation of an unsuccessful result could be used as evidence where the method possibly lacks or is too difficult to use for character artists.

As there is a distinct lack of academic research on this topic, it seems necessary to confirm the available data. Therefore, an online survey was used to acquire quantitative data. Additionally this data could help further improve the interviews by providing results that may be of interest and require further investigation. The primary question of this survey was to ask participants what software they have used to create characters with realistic textures, stylized textures and hand-painted textures respectively. Having a separate question for each art style showed whether the participants use different software depending on the art style.

To help find out why they use certain software and who was using it, additional questions were asked to establish their background. They were asked their age bracket, what game development roles they have fulfilled, whether they are a student or work for a company and what size company, how many years of experience they have creating textures for characters and how many years of experience they have in the game development industry.

I found that there is also a distinct lack of in-depth information available on workflows. Only character artists from Riot Games and Stunlock have shared their workflow, I was not able to find workflows from companies such as Blizzard, though these workflows were mostly shared for a practical purpose. There is no explanation as to why they have chosen their specific workflows or if they have tested procedural alternatives. Interviews were used to fill this gap and find out the reasons why. The interview consisted of several questions divided into several sections. The first section established the perspective of the participant, the next section focused on the preferred workflow of the participant and their reasoning, and the final section focused on the use of procedural tools. The resulting answers were then analysed and compared to each other.


The results

Using procedural tools for hand-painted stylized character textures is in many cases not the optimal method of texturing, but can be used in different situations.

There currently is no good method to generate a proper flow map which stores directional information in a texture, so creating custom brushstrokes that follow the shape of the mesh is difficult. If in the future proper flow maps can be generated based on the geometry, then faking the brushstroke effect would be significantly easier. Another problem is that some materials must be painted physically incorrectly to enhance the overall look and feel of the texture, which is currently not possible to generate. Lastly, complex things such as faces are difficult to texture procedurally, although may be possible with complex ID maps. However these ID maps would have to be painted by hand.

Artefact final result - Substance Designer only - Art by me |

With the current method of the online survey there is an indication that artists are less likely to use procedural tools for hand-painted stylized character textures. However Substance Painter can be used either procedurally or manually, so further studies could provide a more accurate, in-depth look at the use of procedural tools for texturing. The number of responses was also quite low, so a bigger study may be necessary to either confirm or contest the results.

Technical art roles were uncommon among the respondents to the survey, which might explain why proceduralism, a comparatively technical texturing method, is used less than manual approaches. The current number of respondents was not enough to sufficiently test if age, company size, years of experience in the industry, or years of experience texturing characters has any influence on the use of procedural tools. Future studies with a larger number of respondents could provide better and more in-depth insight regarding the effect of these variables.

What emerged from the results of the online survey was further reinforced by the responses during the interviews, as many interviewees did not have much experience with technical art roles. They also had a variety of years of experience which seems to suggest it does not have an influence on whether they use procedural tools or not.

Interviewees’ preferred workflows were extremely similar and, with the exception of one interviewee, none of them used procedural texturing. They learn these workflows and software from those around them and because they are industry standard, which could create a negative vicious circle. If they were creating characters for a significant amount of time, all interviewees except for one changed their workflow over time, based on the proven efficiency of other software. They also don’t create many realistic characters, where procedural tools would be more common, further indicating a lack of interest in procedural texturing for people working with hand-painted stylized effects.

One interviewee mentioned that procedural tools speed up parts of their pipeline. This speed may not be a concern for hand-painted stylized characters, where artists may instead prefer to focus on quality first and foremost. Many interviewees also did not think that procedural tools produce textures with the required personal, handcrafted look and feel. Procedural tools may therefore not be optimal for primary characters, but may still have a place for minor characters.

Interviewees argued that story-telling, immersion, and personality created through deliberate, context-aware detailing is currently not possible with procedural texturing, which may look dull and repetitive due to the random nature. Since only hand-painted stylized character artists were interviewed, it may be worth investigating and interviewing those who are more accustomed to procedural texturing and gather their views on the usefulness of the tools for this specific artstyle.

Final texturing result lacking context aware manual detailing - Art by me |


Conclusion

So, to answer my research question “What barriers prevent the common adoption of procedural tools in hand-painted stylized character texture pipelines?”:

The tools are currently not able to generate textures that are of a similar quality as manually painting the textures by hand. These tools are therefore not preferred when quality is more important than quantity.

It was not conclusively proven that procedural tools could not generate hand-painted styles, although some challenges have not yet been tackled, but industry artists appear to only slowly change their production pipeline. This means that adoption of new techniques may be hindered by a lack of inertia rather than only the lack of potential. Procedural hand-painted stylization is not currently reaching the level of quality that manual labour produces, in terms of storytelling and context-sensitivity, but this does not mean that procedural tools are irrelevant. As new developers experiment with the techniques, proceduralism may form the basis of hand-painted work in the future, taking the repetitive tasks away from artists so that they can focus on bringing the human touch of life to their worlds.