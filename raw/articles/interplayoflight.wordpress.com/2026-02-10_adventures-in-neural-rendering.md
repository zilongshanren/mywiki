---
title: Adventures in Neural Rendering
url: https://interplayoflight.wordpress.com/2026/02/10/adventures-in-neural-rendering/
author: Kostas Anagnostou
published: '2026-02-10'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

In recent years, neural networks have started to find their way into many areas of rendering. While antialiasing and upscaling are probably the most well‑known uses, they’re far from the only ones—texture compression, material representation, and indirect lighting are all active areas of research and development.

I recently started tinkering with neural networks, experimenting with small multilayer perceptrons (MLPs) as a way to encode data in the context of rendering. This post outlines the process and shares some of the initial results and observations from a graphics programmer’s perspective (without much previous experience in neural networks).

Before we begin, a quick note that this is not really a tutorial about MLPs, neural networks (NNs), even in their simplest form are a fairly complex topic and there are many good resources out there to start learning about them, I recommend these 2 as an introduction: [Machine Learning for Game Developers](https://www.youtube.com/watch?v=sTAqWRsEiy0) and [Crash Course in Deep Learning](https://gpuopen.com/learn/deep_learning_crash_course/). Instead, I will summarise a few aspects of them for reference.

For a visual reference, this is what a simple MLP looks like:

In this case the network is made up of 3 input nodes, 2 hidden layers of 3 nodes each and one output node (From now on I will use the 3-3-3-1 notation to describe an MLP). The intermediate layers are “hidden” in the sense that we don’t interact with them directly, we only provide the input data and observe the output data. Also, I used this particular number of nodes in this configuration but there is no limit to the number of nodes in each layer, other than memory and processing time. And the number of nodes in a layer matters, because each node processes all the nodes of the preceding layer (i.e. the graph is fully connected), for example focusing on Node 0 in the hidden layer 1:

it will combine the 3 input nodes and produce its output (fed to the next layer) as follows

The output value of node 0 is simply put a biased weighted sum of all the input nodes output. Before we feed that value to the next layer we have to pass it through an “activation” function. This performs an operation on that value, a popular one being removing all negative values, called ReLU:


and a variation of it

for a small alpha value (eg 0.01). This version still keeps some negative outputs and I have found leads to faster learning. There are [many options](https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.html) when it comes to selecting an activation function for a neural network, each having a different impact on the learning rate and convergence, ReLU and LeakyReLU are a good first starts though and LeakyReLU is what I used for the experiments described in this post.

Going back to the reference to storage requirements, to store the weights and biases for the above MLP, assuming a float data type for each, we would need for the first hidden layer 3 floats for the weights of the inputs and one float for the bias per node (3×3+3 floats), for the second the same amount and for the output 1×3+1 floats, so in total 28 floats to store the whole MLP. It easy to see that this can go up significantly, for an MLP with 9 input nodes, 3 hidden layers of 64 nodes and a 3 node output we would need 9155 float numbers to store. This can go down by using smaller data types, like fp16 or even lower for example.

Implementing an MLP to successively combine nodes and produce output like described above is very straightforward. What is tricky is to calculate the weights and biases used and this is where training of the neural network is needed. Going deep into training is outside the scope of this post, like mentioned there are many good tutorials out there. For some context though, at a high level, this is what is happening: We start with some random weights and biases and given an input vector, we calculate the output of the network (forward propagation, aka inference). The output will of course be wrong, so we calculate how much wrong it is (during training we need to know both the input and the expected, correct output of the network), calculating a gradient (difference) using a “loss” function. We then feed that gradient backwards into the network to adjust weights and biases (back propagation). Having adjusted the weights/biases, we try again feeding a new (or the same) input vector and calculating the output, finding the difference/gradient from the correct output and back propagating it through the network. The intention is, after having repeated this process many, many times, for the calculated output will be close to the expected output, i.e. the network will have “learned” the set of input to output mappings.

In terms of implementation, I assumed MLPs of a maximum of 5 layers, including the input and output layers (so a maximum of 3 hidden layers). The weights and biases I stored in 2 ByteAddressBuffers. Both inference and back propagation are loop heavy, to help the compiler a bit, similarly to this [post](https://gpuopen.com/learn/deep_learning_crash_course/), I defined number of layers and nodes per layer statically, avoiding dynamic loops. I won’t be adding too much code to the post, I’d suggest the reader has a look at the mentioned blog post which also includes a good sample but as an example, this is the code that returns the index into the weights and biases buffers based on layer index, node index and element (weight or bias) index:

```
#define MAX_LAYER_COUNT 5
static const uint neuronsPerLayer[MAX_LAYER_COUNT] =
{
LAYER0_NEURON_COUNT, LAYER1_NEURON_COUNT, LAYER2_NEURON_COUNT, LAYER3_NEURON_COUNT, LAYER4_NEURON_COUNT
};
static const uint weightOffsetsPerLayer[MAX_LAYER_COUNT] =
{
LAYER0_WEIGHT_OFFSET, LAYER1_WEIGHT_OFFSET, LAYER2_WEIGHT_OFFSET, LAYER3_WEIGHT_OFFSET, LAYER4_WEIGHT_OFFSET
};
static const uint biasOffsetsPerLayer[MAX_LAYER_COUNT] =
{
LAYER0_BIAS_OFFSET, LAYER1_BIAS_OFFSET, LAYER2_BIAS_OFFSET, LAYER3_BIAS_OFFSET, LAYER4_BIAS_OFFSET
};
static const uint neuronOffsetsPerLayer[MAX_LAYER_COUNT] =
{
LAYER0_NEURON_OFFSET, LAYER1_NEURON_OFFSET, LAYER2_NEURON_OFFSET, LAYER3_NEURON_OFFSET, LAYER4_NEURON_OFFSET
};
uint GetNeuronCount(uint layer)
{
return neuronsPerLayer[layer];
}
uint GetWeightIndex(uint layer, uint neuronIndex, uint weightIndex)
{
return weightOffsetsPerLayer[layer] + neuronIndex * neuronsPerLayer[layer-1] + weightIndex;
}
uint GetBiasIndex(uint layer, uint neuronIndex)
{
return biasOffsetsPerLayer[layer] + neuronIndex;
}
uint GetNeuronIndex(uint layer, uint index)
{
return neuronOffsetsPerLayer[layer] + index;
}
```

The inference code is like I mentioned is quite simple, made up of 3 nested loop as we need to iterate over the layers, the nodes of a layer and the inputs to the nodes.

```
void ForwardPass(inout float inputs[LAYER0_NEURON_COUNT], inout float nodeOutputs[MAX_NOOF_NODES])
{
uint outputIndex = 0;
//input layer
for (uint index = 0; index < GetNeuronCount(0); index++)
{
nodeOutputs[outputIndex++] = inputs[index];
}
//rest of the layers
for (uint layer = 1; layer < LAYER_COUNT; layer++)
{
for (uint index = 0; index < GetNeuronCount(layer); index++)
{
float output = GetBias(layer, index);
for (int i = 0; i < GetNeuronCount(layer-1); i++)
{
float weight = GetWeight(layer, index, i);
float previousLayerOut = nodeOutputs[GetNeuronIndex(layer - 1, i)];
output += weight * previousLayerOut;
}
nodeOutputs[outputIndex++] = ActivationFunction(output);
}
}
}
```

The training phase broadly follows the above [post](https://gpuopen.com/learn/deep_learning_crash_course/) again and I also implemented [Adam optimisation](https://arxiv.org/pdf/1412.6980) to improve convergence.

Once I had the MLP implementation I started wondering where could I use it in the context of graphics. My approach was a bit simplistic, I focused on small MLPs with a low number of layers and nodes, with a single activation function for everything which is likely not the best way to get good results. The MLP output will depend on the number of layers, number of nodes per layer, activation function which could even be different per layer, loss function etc and to get good results one would need to experiment with all these, something that takes time due to the cost of training.

One interesting aspect of MLPs is that they can encode information/signals, in a similar way Spherical Harmonics, octahedral representations can, but in a non-analytical way, “learning” the expected output based on the input. As an example, I tried encoding the radiance from a cubemap along the normal direction. I used a minimal MLP of a 3-node input layer (normal xyz), one hidden layer of 3 nodes and a 3-node output layer (radiance rgb).

I also used an L2 Spherical Harmonics cubemap radiance encoding [(using this great library](https://github.com/TheRealMJP/SHforHLSL)) as a reference:

![](../../assets/679f798c379a8810.png)


![](../../assets/679f798c379a8810.png)

The SH approximation gives a general sense of radiance directionality but it is very coarse. The MLP described above on the other hand produces this output:

![](../../assets/9b9180f8377363f2.png)


![](../../assets/9b9180f8377363f2.png)

The directionality is much improved in this case, the output is like a very low resolution version of the cubemap. What is more interesting is that the L2 SH representation requires 27 floats (9 float3s) to store the coefficients, while that MLP needs 24 for a much improved quality.

Can the MLP be even smaller, what would happen if we reduce the hidden layer to 2 nodes?

![](../../assets/9b330ff2a117a8cb.png)


![](../../assets/9b330ff2a117a8cb.png)

and then to 1 node only?

![](../../assets/11477fe91096cde7.png)


![](../../assets/11477fe91096cde7.png)

With 2 nodes the output maintains the directionality broadly but introduces a colour shift which is undesirable. With one node it approximates the coarseness of the L2 SH representation closer, impressive for a mere 10 float storage requirement but the colour shifts will again make it unusable for radiance encoding applications.

Irradiance is also a directional quantity that can be encoded with an MLP. The output of a single hidden layer with 3 nodes NN looks as follows:

![](../../assets/ba56e6a1a7c650fe.png)


![](../../assets/ba56e6a1a7c650fe.png)

For comparison, this is the L2 Spherical Harmonics version

![](../../assets/548d9f8fb3a5533b.png)


![](../../assets/548d9f8fb3a5533b.png)

And this is the “ground truth” version, performing Monte Carlo integration of the cubemap in the shader.

![](../../assets/2a447eb85a0d2caa.png)


![](../../assets/2a447eb85a0d2caa.png)

Worth mentioning that the MLP is trained using the output of the ground truth irradiance calculation method. The MLP output is fairly close to the ground truth output, but not as close as the SH one, it appears that in the above scenario SH manages to encode irradiance slightly better.

A smaller MLP with a 1 node hidden later doesn’t manage to capture the directionality in the irradiance well.

![](../../assets/774c5abee684f4c3.png)


![](../../assets/774c5abee684f4c3.png)

One should never evaluate lighting techniques only on smooth spheres as this tends to hide issues that will become very obvious when a normal map is applied. For this reason, let’s rerun the above experiment adding a normal map to the sphere and zooming in a bit to see the result of each irradiance encoding approach.

The output of our small (1 hidden layer of 3 nodes) MLP is this

![](../../assets/1ba15c3bc727ffd0.png)


![](../../assets/1ba15c3bc727ffd0.png)

Along with the L2 SH output

![](../../assets/0d2cbba8dd416aaf.png)


![](../../assets/0d2cbba8dd416aaf.png)

And the ground truth output

![](../../assets/2cbd39b5a1f04c21.png)


![](../../assets/2cbd39b5a1f04c21.png)

Again, the Spherical Harmonics and Ground Truth outputs are quite similar, the difference of the MLP encoding become more pronounced though, the tiny MLP can’t encode irradiance directionality as well which can be seen as bounce light from the floor “leaking” on the faces of the bricks.

To cut a long story short, it appears that to get similar to SH response from the MLP, it needs to have 2 hidden layers of 4 nodes each:

![](../../assets/56c2c1e74f0338f7.png)


![](../../assets/56c2c1e74f0338f7.png)

Such an MLP would require 51 (floating point) numbers to store, which is quite a bit more than an L2 SH’s 27. In this context at least, it appears that a similar to an L2 SH, in terms of storage, MLP can encoding radiance better than irradiance.

Another signal I tried encoding is depth for a number of directions over a sphere centered at a world position (something that one could do with a depth cubemap as well), using raytracing to get the ground truth

![](../../assets/10dc31cf9a0d4c63.png)


![](../../assets/10dc31cf9a0d4c63.png)

The output of a 3-3-3-1 MLP, using a vector distributed over a sphere as an input is as follows

![](../../assets/3ecab5b45c51f49e.png)


![](../../assets/3ecab5b45c51f49e.png)

which is very coarse to be useful. Increasing the hidden layers to 3-32-32-32-1 we are beginning to discern features in the output:

![](../../assets/aa01058f41f988db.png)


![](../../assets/aa01058f41f988db.png)

And finally increasing to 3-128-128-128-1:

![](../../assets/f12505711a95d5b8.png)


![](../../assets/f12505711a95d5b8.png)

we can see many more details in the output and it is starting to become usable. An MLP of that size would need about 33,665 fp numbers for storage which is 134KB. For comparison a small, 128x128x6 depth cubemap is ~393KB. The MLP inference is very expensive though to make it useful using a compute shader implementation at least (44ms on an 3080 mobile GPU).

Another experiment I did was to test if an MLP could be used as an RTAO cache. In this case I used the world position and normal as input to a 6-32-32-32-1 NN (40ms)

![](../../assets/3fdc0cbab2aa3891.png)


![](../../assets/3fdc0cbab2aa3891.png)

Also increasing to 6-64-64-64-1 (240ms):

![](../../assets/621adc2a6950ae86.png)


![](../../assets/621adc2a6950ae86.png)

The MLP does a decent job of capturing AO at a world position for that view at a very large inference cost though. Also, didn’t try “teaching” the MLP multiple views due to training time, so it is not clear how suitable it is for learning the whole scene. For example, moving the camera to another view and spending the time to learn the AO, coming back to the original view the MLP struggles to remember the AO.

![](../../assets/3dcf11a0bdf444e2.png)


![](../../assets/3dcf11a0bdf444e2.png)

I am not sure if an MLP is capable of representing the whole scene AO accurately, I am assuming though a lot more training is needed and potentially a much larger network if this is the case. Even then the inference cost makes it less useful, at least for a compute shader implementation.

As a final test, I tried encoding a specular BRDF (Cook-Torrance). For that I went all in providing normal, light direction, view direction, F0 and roughness as inputs (13 in total) to the MLP. Although the inputs were selected randomly, I restricted light direction and view direction on the hemisphere centered on the normal to reduce the number of invalid combinations (eg light directions below the horizon which won’t contribute).

It turns out that the MLP really struggled to approximate the BRDF, even with a relatively large model 13-128-128-128-3

![](../../assets/4313040c0357b5f3.png)


![](../../assets/4313040c0357b5f3.png)

compared to the reference output

![](../../assets/37e8a5cb8baaf9d9.png)


![](../../assets/37e8a5cb8baaf9d9.png)

The same happened when I tried to reduce the inputs, removing F0 and roughness. It appears that the MLP (at least of that size for that amount of training) struggles to capture the specular lobe, especially for low roughness values.

Turns out there is a different parameterisation of a brdf, called the [Rusinkiewicz parameterisation](https://www.cs.princeton.edu/~smr/papers/brdf_change_of_variables/brdf_change_of_variables.pdf), popular in neural brdf implementations, which can reduce dimensional variation and improve specular lobe representation. In short, this approach reparameterises the brdf from the original normal vector reference (the origin of the brdf angles is the normal vector), to a half vector reference.

As a result the specular lobe lies mostly on the theta_h axis, irrespective of the value of theta_d. Also, for isotropic brdfs, like the one I am using, phi_h is zero reducing the input size even more.

Using the Rusinkiewicz parameterisation with 3 angles, theta_h, theta_d and phi_d, as input we manage to represent the specular lobe much better for a much smaller MLP 3-64-64-64-3 (output quality would likely increase with additional training time):

![](../../assets/8d1edeb59be206b4.png)


![](../../assets/8d1edeb59be206b4.png)

Even a smaller one, 3-32-32-3, seems to capture the specular lobe with some degree of accuracy although at a much increased training time and some extra quantisation visible.

![](../../assets/43a90341b6c7061a.png)


![](../../assets/43a90341b6c7061a.png)

Both the above examples assumed a fixed roughness and F0 which makes the MLP suitable for a single material only. Re-introducing F0 and roughness reduces the ability to capture the lobe, at least for the amount of training time I allowed, which was significantly longer than without those extra inputs.

To summarise the findings: neural networks, MLPs at least, are relatively easy to implement but tricky to get to produce useful results. Graphics programmers are used to tweaking parameters to fine tune systems and achieve better results but in this case, being a new area of me, I don’t feel I have a good grasp yet of what the impact of the various MLP parameters are, number of nodes vs numbers of layers and why one activation function is better than another. Training time is another factor, it takes a lot of time to see the outcome of any MLP alteration, especially for larger networks and the inference cost can also be quite high which may restrict real time rendering applications. I find this an interesting area though that shows promise as a way to encode/represent signals and the incoming HLSL support for inference acceleration has the potential to reduce the cost significantly.

This is super interesting, I’m glad you’re exploring this area!

Wrt the AO experiment, I don’t think compressing the whole scene makes the most sense. My intuition is that these models are best at figuring out functions for efficiently processing local data; essentially learning light transport (or a subset thereof), which allows for much better compression and is also more usable because it works for any scene.

I can think of several schemes for feeding local screenspace data into an AO model… but my understanding is that ML systems work better the fewer assumptions are baked into them. As such, I wonder if you can allow the model itself to drive the data sampling; you only feed in pixel coords, depth and normal, and a first-stage network generates a set of UV sample coordinates. You then sample depth/normals (and maybe 3D voxel occupancy) at each of these coordinates and feed the results into a second-stage network to generate the final AO value.

It might be even better to have more stages, each one driving data sampling for the next one. But the general idea is that the only decision you make is the total number of samples – the network makes all the other decisions about what to sample and how to interpret the samples.

Anyway, I hope you do further experiments, this is all fascinating and I bet there’s a ton of low hanging fruit still left here to be discovered.