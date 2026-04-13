---
title: DagNN - a "deeper" fully connected network
url: https://www.jonolick.com/home/dagnn-a-deeper-fully-connected-network
author: Won
published: '2017-03-04'
source_blog: Jon Olick - Home
source_site: https://www.jonolick.com/home
category: graphics
fetched: '2026-04-13'
---

|
I had an idea the other day while reading a paper about how they passed residuals around layers to keep the gradient going for really deep networks - to help alleviate the vanishing gradient issue. Then it occurred to me, perhaps that this splitting of networks into layers is not the best way to go about it. After all, the brain isn't organized into strict layers of convolution, pooling, etc... So perhaps this is us humans trying to force structure onto an unstructured task. Thus the DagNN was born over last weekend.
First, a quick description of why/how many Deep Neural Networks are trained today as I understand it. The vanishing gradient problem is a problem to neural networks that arise because of how back-propagation works. You take the difference between the output of a network and the desired output of a network and then take the derivative of that node and pass that back through the network weighted by the connections. Then repeat for those connections on the next layer up. So you are passing a derivative of a derivative for 1 hidden layer networks and a derivative of a derivative of a derivative for 2 layer networks and so on. These numbers get "vanishingly" small very quickly - so much so that typically you tend to get *worse* results with a network with 3 or more layers vs just 1 or 2. So, how do you train "deep" networks with many layers? Typically with unsupervised pre-training, typically with an auto-encoder. An auto-encoder is when you train a network, 1 layer at a time stacking on top of each other with no specific training goal other than to reproduce the input. Each time you add a layer you lock the weights of the prior layer. This means your training a generic many layer network to just "understand" images in general as a combination of layered patterns rather than to solve any particular task. Which is better than nothing, but certainly not as good as if you could actually train the *entire* network to solve a specific task (intuitively). The solution: If you could somehow pass the gradient further down into the network, then you can train it "deeper" to solve specific tasks. Back to DagNNs. The basic premise follows the idea that if you pass the gradient further down the network, then you can train deeper networks to solve specific tasks. Win! But how? Simple, remove the whole concept of layers and just connect every node with every prior node allowing any computation to build on any other prior computation to solve the output. This means that the gradient filters through the entire network from the output in fewer hops. The way I like to think about DagNNs is the small world phenomenon. Or the
Pro tip: if you want to bound computational complexity, limit it to a random N number of prior connections per node. I'm trying out this idea now and at least initially it is showing promise. I can now train far bigger fully connected networks than I could before. Will release source when I have more proof in the pudding. By proof that means proof for me too! I need to train it on MNist and compare results.
|
## Archives
## Categories |