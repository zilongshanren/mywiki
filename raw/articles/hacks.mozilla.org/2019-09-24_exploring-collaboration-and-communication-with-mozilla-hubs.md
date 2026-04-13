---
title: Exploring Collaboration and Communication with Mozilla Hubs – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2019/09/exploring-collaboration-and-communication-with-mozilla-hubs/
author: Liv Erickson
published: '2019-09-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[In April last year](https://blog.mozilla.org/blog/2018/04/26/enabling-social-experiences-using-mixed-reality-and-the-open-web/), Mozilla introduced Hubs, an immersive social experience that brings users together in shared 3D spaces. Hubs runs in the browser on mobile, desktop, and [virtual reality devices.](https://blog.mozvr.com/hubs-on-oculus-quest-social-vr/) Since its initial release, the platform has undergone extensive development work to better enable communities and creators to embrace the opportunities that online collaborative environments have to offer. As a result, we’ve seen increased adoption of Hubs and new use cases have emerged.

The ability to connect to anyone around the world is a powerful tool available to us through the internet. As we look at advancements in mixed reality [like the WebXR API](https://developer.mozilla.org/en-US/docs/Web/API/WebXR_Device_API), we are able to explore ways to feel more present with others through technology. One area where virtual reality shows considerable promise is in supporting distributed teams.

Mozilla is no stranger to remote collaboration. [46% of our employees work from home](https://blog.mozilla.org/careers/working-on-distributed-teams/) and the ten company offices span seven countries across six time zones. Because of this, we’re excited about finding opportunities to improve the ways we connect with our [community of contributors and volunteers](https://www.mozilla.org/en-US/contribute/). Remote work and collaboration is a core part of how we connect to each other through the web.

## Communication and Identity

Hubs is built on top of [ WebRTC ](https://developer.mozilla.org/en-US/docs/Glossary/WebRTC) and supports real-time conversations between users in a shared environment. Users embody 3D models in the [glTF format](https://www.khronos.org/gltf/) called avatars, which they can control via WASD keys or through the application’s teleportation controls. Because these avatars ground users in a shared space, people can interact naturally. Spatial audio means that you can break off into small groups and have conversations that broadcast your voice based on your position near others in the room. Similarly, supporting both spoken and text chat between users allows for multiple forms of communication. This can provide more equitable participation compared to other online conferencing platforms.

Video conversations can be powerful forms of communication between trusted parties, but there are some times that you don’t want to share a video stream to a group of people. Establishing trust with other people online takes time. With Hubs, [preserving privacy](https://blog.mozvr.com/creating-privacy-centric-virtual-spaces/) is integral to the platform’s shared 3D spaces. This applies to how you look in Hubs, too. Over the past few months, the Hubs team has released a set of customization capabilities for avatars. These allow creators and users to find more ways to represent themselves within the rooms they participate in. Avatars can be [easily modified and customized by users](https://blog.mozvr.com/new-avatar-features-in-hubs/) on the Hubs website or with 3D modeling tools. Offering flexible options for a user’s identity within an online social platform is a core component of online safety, which you can read more about in the [Mozilla Reality blog post here](https://blog.mozvr.com/virtual-identities-in-hubs/).

## Customization and Collaboration

In addition to new avatar features, we also launched an [online 3D editor called Spoke](http://hubs.mozilla.com/spoke). Spoke can be used to create scenes for Hubs rooms. This allows users to compose spaces using 3D models and traditional web content like videos, images, gifs, and PDFs. Spoke environments can truly transform a space and make it a unique place for communities and organizations to meet. Scenes can also be listed as *remixable*. Other Hubs users can then use these scenes as templates for their own content. In the coming weeks, we’ll also add the ability to create themed kits for Spoke.

Different web content providers power the Create menu in Hubs so users can bring in their own media to share. This can include images, models, and videos found on the web or their own files. Through the Create menu, anyone can create and share documents and objects in an easy, collaborative manner. Users can also share their webcam or share their computer screen with their rooms.

## Supporting Communities and Organizations

Throughout the past year, we’ve heard some [inspiring stories](https://blog.mozilla.org/blog/2019/07/17/qa-igniting-imaginations-and-putting-vr-in-the-hands-of-students-with-kai-frazier/) about how individuals, communities, and organizations are using Hubs to strengthen their missions and stay connected. Communities are powerful ecosystems, and we did a sprint this past year to [build out additional integrations](https://blog.mozvr.com/hubs-discord-beta/) and keep users connected with their friends more easily. We have recently also built new community management tools for events.

In addition to new community management tools, we’ve begun work on a new set of tools that takes the core infrastructure powering hubs.mozilla.com. This will allow anyone to stand up their own self-hosted version of the platform for their own use, and will include the ability to add custom branding and host rooms through a company-provided domain.

## Join the Hubs Community

If you’re interested in Hubs and bringing 3D content to the web, try it out and share your feedback! The code powering Hubs is available online on GitHub under the MPL ([Mozilla Public License](https://www.mozilla.org/en-US/MPL/)) and we welcome contributions from the community. Join the [Hubs Discord Server](https://discord.gg/wHmY4nd) or follow [Hubs on Twitter](http://twitter.com/byhubs) to connect with the team. You can also participate in our virtual events to learn more.

## Links

[https://hubs.mozilla.com/](https://hubs.mozilla.com/)[https://hubs.mozilla.com/spoke/](https://hubs.mozilla.com/spoke/)[https://github.com/mozilla/hubs/](https://github.com/mozilla/hubs/)[https://github.com/mozilla/spoke/](https://github.com/mozilla/spoke/)