---
title: AdversarialSuperposition
url: https://circle-group.github.io/research/AdversarialSuperposition/
author: Edward Stevinson · Lucas Prieto · Melih Barsbey · Tolga Birdal
published: '2025-01-01'
source_blog: CIRCLE Group
source_site: https://circle-group.github.io/
category: graphics
fetched: '2026-04-19'
---

Fundamental questions remain about when and why adversarial examples arise in neural networks,
with competing views characterising them either as artifacts of the irregularities in the decision
landscape or as products of sensitivity to non-robust input features. In this paper, we instead argue
that adversarial vulnerability can stem from *efficient* information encoding in neural networks.
Specifically, we show how superposition -- where networks represent more features than they have
dimensions -- creates arrangements of latent representations that adversaries can exploit. We
demonstrate that adversarial perturbations leverage interference between superposed features,
making attack patterns predictable from feature arrangements. Our framework provides a mechanistic explanation for two known phenomena: adversarial attack transferability between models with similar training regimes and class-specific vulnerability patterns. In synthetic settings with precisely controlled superposition, we establish that superposition *suffices* to create adversarial vulnerability. We then demonstrate that these findings persist in a ViT trained on CIFAR-10. These findings reveal adversarial vulnerability can be a byproduct of networks' representational compression, rather than flaws in the learning process or non-robust inputs.

If you found the paper useful, please consider citing:

```
@article{stevinson2025adversarialsuperposition,
title={Adversarial Attacks Leverage Interference Between Features in Superposition},
author={Stevinson, Edward and Prieto, Lucas and Barsbey, Melih and Birdal, Tolga},
year={2025},
archivePrefix={arXiv},
primaryClass={cs.CV}
}
```