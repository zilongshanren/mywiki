---
title: 'The best animator’s experience possible: an approach to rigging'
url: https://www.gamedeveloper.com/art/the-best-animator-s-experience-possible-an-approach-to-rigging
author: Dave Reuling
published: '2018-01-24'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# The best animator’s experience possible: an approach to rigging

while only animators have to work with rigs not every rig is build for the best animator experience possible. In this article I will discuss my approach to rigging. With the goal in mind to create the best animator's exprience possible.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Tutorials on how to rig a character are spread all over the internet with various levels of quality and price. What most of these tutorials do not teach is the reasoning behind choices, which can be problematic for artists new to rigging because anyone can follow a tutorial on how to rig a character, but not everyone can rig a character. In this article, I discuss my views on how to approach rigging with the aim to help new riggers not only know how to build a rig, but also understand for what reason they are rigging.

The goal:

The goal of rigging is to create a good rig. This sounds pretty straightforward, but what does a good rig mean. One could argue that it means a functional rig; however, I do not think that is the right mindset. The goal of rigging for me is to create a rig that allows the animators work as fast as possible and with the best experience. This is because a rig will most likely only be used by animators. For that reason, the relationship between a rigger and an animator should be seen as a client based relationship, where the animator is the client of the rigger. Though this goal might be simple and easy to understand, not all riggers achieve this goal.

Animator and the animation:

To create a good rig, the rigger has knowledge of two elements of the animation process. The first is the animation the character has to perform. When a rigger has this knowledge, the rigger then can build a rig to better suit that purpose. For example, a character has to swing their body while their knees are stuck behind an object. In most standard rigs this is hard to do because there is no way to keep the knees in place. However,when the rigger is aware that the character will need to perform these type of movements, the rigger can build this functionality into the rig, making the animator’s job a lot easier and faster. Though this gives the animator a lot of flexibility, it is not always needed in a rig, therefore is unnecessary and thus can be left out in most cases. So, by knowing the animation, the rigger can save time on the project by either spending time to make the animator’s job faster and easier or by leaving out unnecessary functionality.

As every animation is different, every animator will have their own workflow with their own preferences of the rig. These preferences could be anything that has to do with the functionality of the rig or even the visuals of the rig. They always need to be taken into account when rigging a character. An example of this: an animator might like big control shapes so they are easier to select, while a different animator would like them small because the controls cloud the character too much. Here it is the job of the rigger to make sure these preferences are met or, in the case of multiple animators, a balance is found. Though these preferences might not seem that important, they play into the experience of the animator when animating.

Think lazy and give the animators what they don’t expect:

When encountering new features to rig, a lot of riggers choose to use FK(Forward Kinematics) for those situations. An example of this could be a tail. A tail can be rigged by creating 12 FK controls that will give the animator enough control. However, if you were to animate a tail, would you like to have to deal with 12 controls? Probably not, and probably your animator does not want to animate with them either. So there is probably a better solution for this. This solution, however, still needs to be versatile. So imagine how your animator likes to work, think lazy. In the case of the tail example, the rigger should keep the 12 controls as a base level and build a more efficient tail on top. An example for this is the finger controls most rigs have. Where the rig has FK controls on the finger itself and a separate controller that controls the fingers with an attribute. In this situation the animator has the option to use the FK controls either for posing and tweaking or use the attributes to get to a pose much faster. This principle can also be applied to the tail. To apply this principle efficiently, the rigger does need to know or have an idea of the type of animations the rig has to do.

A rig that was built by using all the previous principles can be seen as a good rig, but it probably still can be improved. Because an animator’s workflow might not be the fastest way of working and thus can be improved. To find these improvements, the rigger and the animator have to work together and look for repeated actions or actions that take too long in the animator’s workflow. This will result in information that the rigger can use to add functionality to the rig to improve the animator’s workflow. For example, an animator is posing a character that is reaching out a hand. Most commonly the animator will first move the IK(Inverse Kinematics) controller of the arm to the desired destination. After that, the animator will pose the clavicle controller in the right place. This action most often will be repeated, so there is probably a way to optimize this process. A way to solve this is to give the clavicle some influence from the arm IK controller to make the arm move similar to that of a human. The downside of these type of additions is that they take time to create, they need to be able to be turned off as they are not always required, and need to influence the controller as the animator will still need to be able to comfortably use the graph editor. When these conditions are met the animator will have a more pleasant way of animating.

Conclusion:

Currently in the industry there are a lot of good tutorials out there that explain how to build a character rig. However, most of them miss the point of teaching new riggers the methodology a rigger should be aware of when approaching a rig. The most important task of a rigger is to create a rig that gives the animator a better experience and make their workflow faster. This is achieved by optimizing the rig for the animation of the character. For this, the rigger will need to know the exact animations the character needs to perform and the animators preference’s. With this information the rigger can than build a rig that is optimized for the animator by reducing the amount of controllers and actions needed to pose the character.