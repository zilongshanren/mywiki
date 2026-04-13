---
title: Featured Blog | Leveraging Emotional Design Features to Enhance Character Perception
  in Pixel Art
url: https://www.gamedeveloper.com/art/inefficient-or-unexplored-insights-from-a-year-long-study-on-2d-normal-map-generators
author: Amine El Bouhattaoui
published: '2024-06-21'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Inefficient or Unexplored: Insights from a Year-Long Study on 2D-Normal Map Generators

This article is a reflection on a year spent researching 2D-Normal map generators and artist tools as well as an educational resource for those interested in the field.

![Image from Death Machine by Philip Froelich, an example of a 2D-dynamically lit game using 2D-Normal maps releasing in 2024. Image from Death Machine by Philip Froelich, an example of a 2D-dynamically lit game using 2D-Normal maps releasing in 2024.](../../assets/3e60adb85e801ca1.png)

Over the past three decades, the gaming industry has seen major advances, transitioning from predominantly 2D games utilizing traditional pixel-art graphics to a more 3D-focused industry. However, 2D was never abandoned. Instead of the AAA industry, indies have since seen major success with titles such as Cuphead and Celeste proving the potential for 2D games. One niche technology used to enhance 2D games is dynamic lighting, which adds depth and realism to 2D visuals by simulating various light interactions as seen most recently in Sabotage Games’ Sea of Stars.

Despite its potential, there are several major challenges involved with the implementation of 2D dynamic lighting. While there are sophisticated methods that involve 3D graphics, the traditional method utilizes 2D-Normal maps, which simulate depth and texture by encoding surface normals. While the AAA gaming industry has established and well-proven workflows for generating normal maps in 3D, similar tools for 2D game development remain underutilized. This led to my year-long research project, culminating in a thesis titled “Setting Standards for 2D-Normal Map Generators.”

## Understanding Normal Maps in 2D Game Development

Unlike 3D models, which inherently possess depth information, 2D art relies on normal maps to create the illusion of three-dimensionality vital for dynamic lighting. However, the process of creating 2D normal maps is labor-intensive, typically forcing artists to manually draw them for each asset. This manual process adds not just development time but also significant cost, making dynamic lighting an overly expensive feature for the smaller studios often involved with 2D.

## The Quest for Automation

To address these challenges, several tools have been developed to automate the generation of these 2D normal maps. Software such as Sprite Lamp, SpriteDLight, and Laighter have attempted to streamline this process, but they have yet to gain major industry adoption. Many of these tools operate as black boxes, with proprietary algorithms and limited customization options, making it more challenging to integrate into a development workflow. Thus, I set out to research my own set of standards, to figure out what it takes to create a more attractive 2D-Normal map generation tool.

## Research Methodology: Q-Sort and Expert Interviews

My research focused on two questions. Firstly, what makes a good normal map and how can we rate the output of tools? Additionally, I wanted to find out what features or qualities artists value most when utilizing such tools. My research employed a combination of an exploratory Q-Sort methodology and expert interviews. The Q-Sort methodology helped assess the needs and preferences of artists working with 2D-normal maps. Participants were asked to rank various features and aspects of normal map generators, providing a structured way to identify the most critical requirements. This was complemented by interviews with experienced 2D-Normal map artists and developers to gain deeper insights into the technical and practical aspects of normal map generation.

## Key Findings and Guidelines

The research revealed several key insights for the development of current and future 2D-normal map generators:

Quality of output: Artists prioritize high-quality normal map generation that closely mimics hand-drawn maps. Tools should focus on improving the accuracy of automatically generated maps. Notable also is that the speed of the workflow was significantly less valued here, the artists involved made it clear that they don’t mind the output needing modification and/or minor fixes. As long as the bulk of the work is saved.

Trial and Error Workflow: An effective tool should support an iterative workflow, allowing artists to easily tweak and refine normal maps. This includes features for real-time preview and adjustment. Additionally, artists tend to like tools that resemble their own, so any great normal map generator should include staples such as a color picker, animation, and Undo/Redo features.

Objective Evaluation Metrics: The most disappointing conclusion was that there are currently no standardized metrics for evaluating the quality of 2D-normal maps. This means developers will have to work closely with actual 2D-normal mapping artists when evaluating the quality of their tools.

Integration with Existing Tools: Seamless integration with popular 2D art software and game engines is crucial. Often artists seemed far more interested in utilizing such technology within their established tools such as Aseprite rather than in a separate tool.

Public Learning Resources: The availability of comprehensive documentation and tutorials can help increase the accessibility of the field. The field is currently quite thin, and the hope is that an increase in public learning resources will generate more interest in young indie artists to learn these skills.


## Conclusion

The generation of 2D-normal maps holds great potential, especially within the 2D-Indie scene. Great artists are already working on beautiful games such as @Philtacular and his upcoming Death Machine. By further streamlining the generation tools we should be able to make dynamic lighting in 2D games far more accessible and cost-effective to indie developers. I believe that it’s important that as a tiny community, we do all we can to spread the knowledge needed to pave the way for more innovative tools and techniques ultimately resulting in even more beautiful 2D games. I hope this research can be a great resource for tools developers interested in 2D-Normal maps and for researchers interested in continued exploration of this niche, but wonderful field.

My full thesis “Setting Standards for 2D-Normal Map Generators” will soon be available through the Breda University of Applied Sciences for those interested in delving deeper into my process and methodology.