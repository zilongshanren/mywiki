---
title: Protect Prefab Fields from "Apply"
url: http://www.roboryantron.com/2017/10/protect-prefab-fields-from-apply.html
author: Get link Facebook X Pinterest Email Other Apps
published: '2017-10-30'
source_blog: roboryantron
source_site: http://www.roboryantron.com/
category: game programming
fetched: '2026-04-13'
---

### Prefab Apply

Ever have a prefab in a scene with overrides? Ever have some jerk press "Apply" and push those changes to every other instance? I hate that jerk.
You can implement ISerializationCallbackReceiver on a MonoBehaviour to define how it saves (or loads). This means that you can use it to prevent certain fields from saving, which is kind of useless on its own... but using some PrefabUtility functions you can let it save in a scene, but not in a prefab.



All you need to do is implement OnBeforeSerialize to intercept the save and check if the object is a prefab with PrefabUtility.GetPrefabType. If it is PrefabType.Prefab, that means that it is saving to the prefab definition in the project as opposed to the prefab instance in the scene. At that point, you can set your protected field to null or whatever value you expect the prefab to have.



### Sample Project

I have a sample scene posted to my[QuickTips](https://github.com/roboryantron/UnityQuickTips/tree/master/Assets/PrefabApplyProtection)repo on GitHub. In the future, this project will have lots of other simple tip examples so keep an eye on it.

In the sample, I have a prefab for a portal that loads a scene when a player collides with it. The portal is a prefab since it will be used all over the place and we want it to look the same. However, it is not often the case that we would want all of our portals to go to the same destination. This is where we can protect against a prefab-apply problem by preventing the destination scene from being saved to the prefab which could erroneously push it out to other portals that have not yet set a destination.

This way, any portals that were placed in a scene but not set up completely will have a null destination scene instead of whatever scene was last pushed with Apply. Identifying broken instances should be easier to do with invalid data rather than valid but wrong data.

This is awesome! Thank you


ReplyDelete