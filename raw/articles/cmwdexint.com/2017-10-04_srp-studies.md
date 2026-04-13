---
title: SRP studies
url: https://cmwdexint.com/2017/10/04/srp-studies/
author: Ming Wai Chan
published: '2017-10-04'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

**Overview**

Unity C++ code |
C#/shader code (MIT open source) |
| Culling Render set of objects with filter/sort/params/batch Internal graphics platform abstraction |
Camera setup Light setup Shadows setup Frame render pass structure & logicShader/compute code |


**API**

![SRP api](../../assets/2177ffbeecda684b.png)


**Existing**

![001](../../assets/6df0ba2a98e3398f.png)


![002](../../assets/50a39bc6bdab01b3.png)


![003](../../assets/20c2acde2d730d32.png)


//BeforeGBuffer

//AfterGBuffer – 0

//AfterGBuffer – 1

//AfterGBuffer – 2

//AfterGBuffer – 3

//AfterGBuffer

//BeforeReflections

//AfterReflections

//BeforeLighting

//-(for each light)-

//Lighting – BeforeShadowMapPass

//Lighting – BeforeShadowMap

//Lighting – AfterShadowMap

//Lighting – AfterShadowMapPass

//Lighting – BeforeScreenspaceMask

//Lighting – AfterScreenspaceMask

//AfterLighting

//BeforeFinalPass

//AfterFinalPass

//BeforeDepthTexture

//AfterDepthTexture

//BeforeDepthNormalsTexture

//AfterDepthNormalsTexture

//BeforeForwardOpaque

//AfterForwardOpaque

//BeforeSkybox

//AfterSkybox

//BeforeImageEffectsOpaque

//AfterImageEffectsOpaque

//BeforeForwardAlpha

//AfterForwardAlpha

//BeforeImageEffects

//AfterImageEffects

//BeforeHaloAndLensFlares

//AfterHaloAndLensFlares

//AfterEverything

LikeLike