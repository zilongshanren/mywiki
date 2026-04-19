---
title: 'PoseD-Flow: Versatile and Guided Flow Matching Model of Human Pose'
url: https://circle-group.github.io/research/PoseD-Flow/
author: CVPR
published: '2026-01-01'
source_blog: CIRCLE Group
source_site: https://circle-group.github.io/
category: graphics
fetched: '2026-04-19'
---

## Overview

Generative pose priors have recently emerged as a powerful tool for inference under occlusion or noise. Yet today's strongest generative paradigm, flow matching, remains unused for human pose due to two fundamental barriers: the absence of a pre-trained flow prior and the non-Euclidean nature of articulated poses. We overcome both by introducing **PoseD-Flow**, a novel framework to unify Riemannian Flow Matching (RFM) with training-free guidance for 3D human pose recovery. PoseD-Flow is composed of two contributions: (i) **PoseRFM**, the first RFM model of human pose, defined directly on the product manifold of joint rotations, and (ii) **Riemannian D-Flow**, a principled guidance mechanism that, by differentiating through its ODE sampling dynamics, conditions PoseRFM at inference without any task-specific training. Our theoretical analysis shows that the induced dynamics are shaped by data covariance and manifold curvature, yielding a bias toward realistic poses. Across pose completion, denoising, and inverse kinematics, PoseD-Flow establishes new state of the art, particularly under noise, occlusion, and partial observations.


**PoseD-Flow** framework: (top) **PoseRFM**, a robust human pose prior defined on the product manifold of joints using *Riemannian Flow Matching;* (bottom): **Riemannian D-Flow**, a flexible, geometry-aware inversion technique for flow models. Together, they provide a novel approach to solving inverse problems in human pose, achieving results competitive with SotA diffusion models.