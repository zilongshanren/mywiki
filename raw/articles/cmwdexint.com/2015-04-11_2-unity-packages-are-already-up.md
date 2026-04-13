---
title: 2 Unity Packages are already up
url: https://cmwdexint.com/2015/04/11/2-unity-packages-are-already-up/
author: Ming Wai Chan
published: '2015-04-11'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

As mentioned, the **Lava Flowing Shader** has been released for free on Unity Asset Store!

Link: [https://www.assetstore.unity3d.com/en/#!/content/33635](https://www.assetstore.unity3d.com/en/#!/content/33635)

As my knowledge about shader keeps growing slowly, I found that I can blend more than 2 layers of “UV”…..It is because the 2 texcoords limit only limits on input. Your FBX model can only have 2 UV channels but shader can make instances of the 2 UV texcoords and thus let you have more layers of texture blending. I will try to update the package later.

*************************

Another package **Simple SeeThrough Shader** has been released on Unity Asset Store also. Link: [https://www.assetstore.unity3d.com/en/#!/content/33924](https://www.assetstore.unity3d.com/en/#!/content/33924)


Simple SeeThrough Shader is a simpler option to render objects behind obstacles which works on mobile platforms. It supports both 3D meshes and Unity sprite 2D. The package contains shaders for both character and props, with 2 see-through effects to choose from. Please check the webplayer demo:

WEBPLAYER DEMO

[http://www.dexint.net/unity/20150404_Simple_SeeThrough/](http://www.dexint.net/unity/20150404_Simple_SeeThrough/)

For detailed instructions about using this Simple SeeThrough Shader please read our online google doc here:

GOOGLE DOC

[https://docs.google.com/…/1gUfWCrMTFr2_QX-2e6XXQ0WQH4P…/edit](https://docs.google.com/document/d/1gUfWCrMTFr2_QX-2e6XXQ0WQH4PC7KCgyb49rfxcWIk/edit)

As we have very limited testing devices so if you are not sure whether it really works on your device please try the following apk! Let me know if your device works perfectly on not!

TESTING ANDROID APK BUILD

[https://drive.google.com/…/0B5VH9PozUxl-eWhxYjRMSzQwb…/view…](https://www.facebook.com/l.php?u=https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F0B5VH9PozUxl-eWhxYjRMSzQwbFU%2Fview%3Fusp%3Dsharing&h=gAQHzfcMd&enc=AZOCNBskHFwiCZfkjHOx9Pk3bosyEjI5-_mbh8NiyZ4OVOMvRE2ZJ2kKhvTjtV5oHSYdfapUc7qZrJJ6v0Sd9VYFttxcIw3sZ8XiwqDDoqAvUkH2TwHlfhwRuqd6mFtQAJ_AmY4o7AKfrlbbdr1xzyN__60HosEk9_8UkrQEw01s9buR5qVfhVfzQRS1WAa97mxrLkry8HFI0-zdyiGJPNnJ&s=1)

![](https://i0.wp.com/d2ujflorbtfzji.cloudfront.net/package-screenshot/a9c113f0-9c6d-4b71-8f8e-cfe18556d83a_scaled.jpg)


The biggest challenge of this shader is that I must use the discard pixel function to chop the empty pixels. To let the sprite props cover the player correctly it must writes to the Z buffer so that the **GPU treats it as a real non-transparent** object. But indeed it is a transparent object. So with Zwrite on, the things behind the transparent pixel will not be rendered. It is forced to use discard function.

It’s impressive how you utilized shader techniques like UV instances and texture blending for realistic effects.

LikeLike