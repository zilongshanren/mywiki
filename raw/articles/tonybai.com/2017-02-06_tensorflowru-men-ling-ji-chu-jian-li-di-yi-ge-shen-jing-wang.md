---
title: TensorFlow入门：零基础建立第一个神经网络
url: https://tonybai.com/2017/02/06/build-your-first-neural-network-with-tensorflow/
published: '2017-02-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# TensorFlow入门：零基础建立第一个神经网络

首先，我不得不承认这篇文章有些标题党的味道^0^，但文章还是要继续写下去，备忘也好，能帮助到一些人也好。

在[2016小结](http://tonybai.com/2017/01/03/2016-summary/)的时候，我说过：2017年要了解一些有关[机器学习](https://en.wikipedia.org/wiki/Machine_learning)和[人工智能](https://en.wikipedia.org/wiki/Artificial_intelligence)(以下简称AI)方面的技术。如果有童鞋问：Why？我会告诉你：跟风。作为技术人，关注和紧跟业界最前沿的技术总是没错的。

2016年被业界普遍认为是AI这一波高速发展的元年，当然[DeepMind](https://deepmind.com/)的[AlphaGo](https://en.wikipedia.org/wiki/AlphaGo)在这方面所起到的作用是功不可没的。不过人工智能并未仅仅停留在实验室，目前可以说人工智能已经深入到我们生活中的方方面面，比如：电商的精准个性化商品推荐、手机上安装的[科大讯飞](http://www.iflytek.com/)的中文语音识别引擎以及大名鼎鼎的Apple的[siri](https://en.wikipedia.org/wiki/Siri)等。只是普通老百姓并没有意识到这一点，或者说当前AI的存在和运行形式与大家传统思想中的“AI”还未到形似的地步，再或者当前AI的智能程度还未让人们感觉到AI时代的到来。

人工智能是当前的技术风口，也是投资风口。不过，人工智能技术与普通的IT技术不同的地方在于其背后需要大量且有一定深度的数学理论知识，有门槛，并且门槛较高，这会让普通程序员望而却步的。还好有国际大公司，比如:Google、Facebook等在努力在降低这一门槛，让人工智能技术更加接地气，让更多从事IT领域的人能接触到AI，并思考如何利用AI解决实际问题。Google的[TensorFlow](https://github.com/tensorflow/tensorflow)应该就是在这样的背景下诞生的。

这里并不打算介绍TensorFlow是什么，其原理是什么（因为目前我也不知道），只是利用TensorFlow简简单单地建立起一个神经网络模型，带着大家感性的认知一下什么是AI。本文特别适合那些像我一样，从未接触过AI，但又想感性认识AI的程序员童鞋们。

### 一、由来

和AI门外的程序员童鞋一样，想窥探AI的世界已久，但苦于没有引路人，一直在门外徘徊。直到看到[martin gorner](https://github.com/martin-gorner)的那篇《[TensorFlow and deep learning, without a PhD](https://codelabs.developers.google.com/codelabs/cloud-tensorflow-mnist/#0)》。在这篇文章中，martin已经将利用TensorFlow建立并一步步训练优化一个神经网络的门槛降低到了最简化的程度了。不过即便这样，把martin所使用这个环境搭建起来（文中虽然有详细步骤），可能依旧会遇到一些问题，本文的目的之一就是帮助你迈过这“最后一公里”。

### 二、搭建环境

我所使用的环境是一台think center x86_64物理机，安装的是ubuntu 16.04.1。相关软件版本：

```
$ python
Python 2.7.12 (default, Nov 19 2016, 06:48:10)
$ git version
git version 2.7.4
```


按照[教程](https://github.com/martin-gorner/tensorflow-mnist-tutorial)中INSTALL.txt中的步骤，我们需要安装依赖软件：

```
$ sudo apt-get install python3
正在读取软件包列表... 完成
正在分析软件包的依赖关系树
正在读取状态信息... 完成
python3 已经是最新版 (3.5.1-3)。
升级了 0 个软件包，新安装了 0 个软件包，要卸载 0 个软件包，有 203 个软件包未被升级。
$ sudo apt-get install python3-matplotlib
python3-matplotlib 已经是最新版 (1.5.1-1ubuntu1)。
$sudo apt-get install python3-pip
python3-pip 已经是最新版 (8.1.1-2ubuntu0.4)。
$ pip3 install --upgrade tensorflow
Collecting tensorflow
Downloading tensorflow-0.12.1-cp35-cp35m-manylinux1_x86_64.whl (43.1MB)
... ...
Installing collected packages: numpy, six, wheel, setuptools, protobuf, tensorflow
Successfully installed numpy-1.11.0 protobuf setuptools-20.7.0 six-1.10.0 tensorflow wheel-0.29.0
```


我们看到安装的TensorFlow是[0.12.1版本](https://github.com/tensorflow/tensorflow/releases/tag/0.12.1)，这应该是TensorFlow发布1.0版本前的最后一个Release版了。

下载Martin的教程代码：

```
$ mkdir -p ~/test/tensorflow
$ git clone https://github.com/martin-gorner/tensorflow-mnist-tutorial.git
正克隆到 'tensorflow-mnist-tutorial'...
remote: Counting objects: 271, done.
remote: Total 271 (delta 0), reused 0 (delta 0), pack-reused 271
接收对象中: 100% (271/271), 95.01 KiB | 46.00 KiB/s, 完成.
处理 delta 中: 100% (171/171), 完成.
检查连接... 完成。
```


我使用的tutorial的revision是：commit a9eb2bfcd74df4d7f3891d5403468d87547320e8。

### 三、建立并训练识别手写数字的神经网络

万事俱备，只差执行。

一起来建立我们的第一个神经网络：

```
$cd ~/test/tensorflow/tensorflow-mnist-tutorial
$ ls
cloudml LICENSE mnist_2.2_five_layers_relu_lrdecay_dropout.py mnist_4.1_batchnorm_five_layers_relu.py tensorflowvisu_digits.py
CONTRIBUTING.md mnist_1.0_softmax.py mnist_3.0_convolutional.py mnist_4.2_batchnorm_convolutional.py tensorflowvisu.mplstyle
data mnist_2.0_five_layers_sigmoid.py mnist_3.1_convolutional_bigger_dropout.py __pycache__ tensorflowvisu.py
INSTALL.txt mnist_2.1_five_layers_relu_lrdecay.py mnist_4.0_batchnorm_five_layers_sigmoid.py README.md
$ python3 mnist_1.0_softmax.py
/usr/lib/python3/dist-packages/matplotlib/font_manager.py:273: UserWarning: Matplotlib is building the font cache using fc-list. This may take a moment.
warnings.warn('Matplotlib is building the font cache using fc-list. This may take a moment.')
/usr/lib/python3/dist-packages/matplotlib/font_manager.py:273: UserWarning: Matplotlib is building the font cache using fc-list. This may take a moment.
warnings.warn('Matplotlib is building the font cache using fc-list. This may take a moment.')
Successfully downloaded train-images-idx3-ubyte.gz 9912422 bytes.
Extracting data/train-images-idx3-ubyte.gz
Successfully downloaded train-labels-idx1-ubyte.gz 28881 bytes.
Extracting data/train-labels-idx1-ubyte.gz
Successfully downloaded t10k-images-idx3-ubyte.gz 1648877 bytes.
Extracting data/t10k-images-idx3-ubyte.gz
Successfully downloaded t10k-labels-idx1-ubyte.gz 4542 bytes.
Extracting data/t10k-labels-idx1-ubyte.gz
Traceback (most recent call last):
File "mnist_1.0_softmax.py", line 80, in <module>
datavis = tensorflowvisu.MnistDataVis()
File "/home/tonybai/test/tensorflow/tensorflow-mnist-tutorial/tensorflowvisu.py", line 166, in __init__
self._color4 = self.__get_histogram_cyclecolor(histogram4colornum)
File "/home/tonybai/test/tensorflow/tensorflow-mnist-tutorial/tensorflowvisu.py", line 160, in __get_histogram_cyclecolor
colors = clist.by_key()['color']
AttributeError: 'Cycler' object has no attribute 'by_key'
```


出错了！

这里要注意的是：初次建立时，程序会首先从[MNIST dataset](http://yann.lecun.com/exdb/mnist/)下载训练数据文件，这里需要等待一段时间，千万别认为是程序出现什么hang住的异常情况。

之后的AttributeError才是真正的出错了！直觉告诉我是课程程序依赖的某个第三方库版本的问题，但又不知道是哪个库，于是我用临时处理方案fix it：

```
//tensorflowvisu.py
#self._color4 = self.__get_histogram_cyclecolor(histogram4colornum)
#self._color5 = self.__get_histogram_cyclecolor(histogram5colornum)
self._color4 = '#CFF57F'
self._color5 = '#E6C54A'
```


我把出错的调用注释掉，用hardcoding的方式直接赋值了两个color。

再次运行这个模型，我们终于看到那个展示训练过程的“高大上”的窗口弹了出来：

![img{512x368}](../../assets/2f2aabfca6c82ffa.png)


运行一段时间后，当序号递增到2001时，程序hang住了。最初我以为是程序又出了错，最后[在Martin的解释下](https://github.com/martin-gorner/tensorflow-mnist-tutorial/issues/11)，我才明白原来是训练结束了。在mnist_1.0_softmax.py文件末尾，我们可以看到这样一行注释：

```
# final max test accuracy = 0.9268 (10K iterations). Accuracy should peak above 0.92 in the first 2000 iterations.
```


这里告诉我们对神经网络的训练会进行多少次iterations。mnist_1.0_softmax.py需要2000次。tensorflow-mnist-tutorial下的每个训练程序文件末尾都有iteration次数，只不过有的说明简单些，有些复杂些罢了。

在[另外一个issue](https://github.com/martin-gorner/tensorflow-mnist-tutorial/issues/10)中，Martin也回应了上面的error问题，他的solution是：

```
pip3 install --upgrade matplotlib
```


我实测后，发现问题的确消失了！

### 四、小结

识别手写数字较为简单，采用softmax都可以将识别率训练到92%左右。采用其他几个模型，比如：mnist_4.1_batchnorm_five_layers_relu.py，可以将识别准确率提升到98%，甚至更高。

将这个教程运行起来的第一感觉就是AI真的很“高大上”，看着刷屏的日志和不断变化的UI，真有些科幻大片的赶脚，看起来也让你感觉心旷神怡。

不过目前仅仅停留在感性认知，深入理解TensorFlow背后的运行原理以及训练模型背后的理论才算是真正入门，这里仅仅是在AI领域迈出的一小步罢了^0^。

© 2017, [bigwhite](https://tonybai.com). 版权所有.

No related posts.

不错，坚持哟！