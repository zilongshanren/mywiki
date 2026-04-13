---
title: Cocos2d-x内存管理-绕不过去的坎
url: https://tonybai.com/2014/03/18/cocos2dx-memory-management/
published: '2014-03-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Cocos2d-x内存管理-绕不过去的坎

[Cocos2d-x](http://cocos2d-x.org/)引擎的核心是用C++编写的，那对于所有使用该引擎的游戏开发人员来说，内存管理是一道绕不过去的坎。

关于Cocos2d-x内存管理，网上已经有了许多参考资料，有些资料写的颇为详实，因为在内存管理这块我不想多费笔墨，只是更多的将思路描述清 楚。

**一、对象内存引用计数**

Cocos2d-x内存管理的基本原理就是对象内存引用计数，Cocos2d-x将内存引用计数的实现放在了顶层父类CCObject中，这里将涉及引用计数的CCObject的成员和方法摘录出来：

class CC_DLL CCObject : public CCCopying

{

public:

… …

protected:

// count of references

unsigned int m_uReference;

// count of autorelease

unsigned int m_uAutoReleaseCount;

public:

void release(void);

void retain(void);

CCObject* autorelease(void);

… ….

}

CCObject::CCObject(void)

: m_nLuaID(0)

, m_uReference(1) // when the object is created, the reference count of it is 1

, m_uAutoReleaseCount(0)

{

… …

}

void CCObject::release(void)

{

CCAssert(m_uReference > 0, "reference count should greater than 0");

–m_uReference;

if (m_uReference == 0)

{

delete this;

}

}

void CCObject::retain(void)

{

CCAssert(m_uReference > 0, "reference count should greater than 0");

++m_uReference;

}

CCObject* CCObject::autorelease(void)

{

CCPoolManager::sharedPoolManager()->addObject(this);

return this;

}

先不考虑autorelease与m_uAutoReleaseCount（后续细说）。计数的核心字段是m_uReference，可以看到：

* 当一个Object初始化（被new出来时），m_uReference = 1；

* 当调用该Object的retain方法时，m_uReference++；

* 当调用该Object的release方法时，m_uReference–，若m_uReference减后为0，则delete该Object。

二、**手工对象内存管理**

在上述对象内存引用计数的原理下，我们得出以下Cocos2d-x下手工对象内存管理的基本模式：

CCObject *obj = new CCObject();

obj->init();

…. …

obj->release();

在Cocos2d-x中CCDirector就是一个手工内存管理的典型：

CCDirector* CCDirector::sharedDirector(void)

{

if (!s_SharedDirector)

{

**s_SharedDirector = new CCDisplayLinkDirector();
s_SharedDirector->init();**

}

return s_SharedDirector;

}

void CCDirector::purgeDirector()

{

… …

// delete CCDirector

**release();**

}

**三、自动对象内存管理**

所谓的“自动对象内存管理”，指的就是哪些不再需要的object将由Cocos2d-x引擎替你释放掉，而无需你手工再调用Release方法。

自动对象内存管理显然也要遵循内存引用计数规则，只有当object的计数变为0时，才会释放掉对象的内存。

自动对象内存管理的典型模式如下：

CCYourClass *CCYourClass::create()

{

CCYourClass*pRet = new CCYourClass();

if (pRet && pRet->init())

{

pRet->autorelease();

return pRet;

}

else

{

CC_SAFE_DELETE(pRet);

return NULL;

}

}

一般我们通过一个单例模式创建对象，与手工模式不同的地方在于init后多了一个autorelease调用。这里再把autorelease调用的实现摘录一遍：

CCObject* CCObject::autorelease(void)

{

CCPoolManager::sharedPoolManager()->addObject(this);

return this;

}

追溯addObject方法：

// cocoa/CCAutoreleasePool.cpp

void CCPoolManager::addObject(CCObject* pObject)

{

getCurReleasePool()->addObject(pObject);

}

void CCAutoreleasePool::addObject(CCObject* pObject)

{

m_pManagedObjectArray->addObject(pObject);

CCAssert(pObject->m_uReference > 1, "reference count should be greater than 1");

**++(pObject->m_uAutoReleaseCount);**

**pObject->release();** // no ref count, in this case autorelease pool added.

}

// cocoa/CCArray.cpp

void CCArray::addObject(CCObject* object)

{

ccArrayAppendObjectWithResize(data, object);

}

// support/data_support/ccCArray.cpp

void ccArrayAppendObjectWithResize(ccArray *arr, CCObject* object)

{

ccArrayEnsureExtraCapacity(arr, 1);

ccArrayAppendObject(arr, object);

}

void ccArrayAppendObject(ccArray *arr, CCObject* object)

{

CCAssert(object != NULL, "Invalid parameter!");

**object->retain();**

arr->arr[arr->num] = object;

arr->num++;

}

调用层次挺深，涉及的类也众多，这里归纳总结一下。

Cocos2d-x的自动对象内存管理基于对象引用计数以及CCAutoreleasePool（自动释放池）。引用计数前面已经说过了，这里单说自动释放池。Cocos2d-x关于自动对象内存管理的基本类层次结构如下：

CCPoolManager类 (自动释放池管理器)

– CCArray* m_pReleasePoolStack; （自动释放池栈，存放CCAutoreleasePool类实例）


CCAutoreleasePool类

– CCArray* m_pManagedObjectArray; （受管对象数组）

CCObject关于内存计数以及自动管理有两个字段：m_uReference和m_uAutoReleaseCount。前面在手工管理模式下，我只提及了m_uReference，是m_uAutoReleaseCount该亮相的时候了。我们沿着自动释放对象的创建步骤来看看不同阶段，这两个重要字段的值都是啥，代表的是啥含义：

CCYourClass*pRet = new CCYourClass(); m_uReference = 1； m_uAutoReleaseCount = 0；

pRet->init()； m_uReference = 1； m_uAutoReleaseCount = 0；

pRet->autorelease();

m_pManagedObjectArray->addObject(pObject); m_uReference = 2； m_uAutoReleaseCount = 0；

++(pObject->m_uAutoReleaseCount); m_uReference = 2； m_uAutoReleaseCount = 1；

pObject->release(); m_uReference = 1； m_uAutoReleaseCount = 1；

在调用autorelease之前，两个值与手工模式并无差别，在autorelease后，m_uReference值没有变，但m_uAutoReleaseCount被加1。

m_uAutoReleaseCount这个字段的名字很容易让人误解，以为是个计数器，但实际上绝大多数时刻它是一个标识的角色，以前版本代码中有一个布尔字段m_bManaged，似乎后来被m_uAutoReleaseCount替换掉了，因此**m_uAutoReleaseCount兼有m_bManaged的含义**， 也就是说该object是否在自动释放池的控制之下，如果在自动释放池的控制下，自动释放池会定期调用该object的release方法，直到该 object内存计数降为0，被真正释放。否则该object不能被自动释放池自动释放内寸，需手工release。这个理解非常重要，再后面我们能用到 这个理解。

**四、自动释放时机**

通过autorelease我们已经将object放入autoreleasePool中，那究竟何时对象会被释放呢？答案是每帧执行一次自动内存对象释放操作。

在“[Hello，Cocos2d-x](http://tonybai.com/2014/03/11/hello-cocos2dx/)”一文中，我们讲过整个Cocos2d-x引擎的驱动机制在于GLThread的guardedRun函数，后者会 “死循环”式（实际帧绘制频率受到屏幕vertsym信号的影响）的调用Render的onDrawFrame方法实现，而最终程序会进入 CCDirector::mainLoop方法中，也就是说mainLoop的执行频率是每帧一次。我们再来看看mainLoop的实现：

void CCDisplayLinkDirector::mainLoop(void)

{

if (m_bPurgeDirecotorInNextLoop)

{

m_bPurgeDirecotorInNextLoop = false;

purgeDirector();

}

else if (! m_bInvalid)

{

drawScene();

// release the objects

CCPoolManager::sharedPoolManager()->pop();

}

}

这次我们要关注的不是drawScene，而是 CCPoolManager::sharedPoolManager()->pop()，显然在游戏未退出 (m_bPurgeDirecotorInNextLoop决定）的条件下，CCPoolManager的pop方法每帧执行一次，这就是自动释放池执行 的起点。

void CCPoolManager::pop()

{

if (! m_pCurReleasePool)

{

return;

}

int nCount = m_pReleasePoolStack->count();

**m_pCurReleasePool->clear();**

if(nCount > 1)

{

m_pReleasePoolStack->removeObjectAtIndex(nCount-1);

m_pCurReleasePool = (CCAutoreleasePool*)m_pReleasePoolStack->objectAtIndex(nCount – 2);

}

}

真正释放对象的方法是m_pCurReleasePool->clear()。

void CCAutoreleasePool::clear()

{

if(m_pManagedObjectArray->count() > 0)

{

CCObject* pObj = NULL;

CCARRAY_FOREACH_REVERSE(m_pManagedObjectArray, pObj)

{

if(!pObj)

break;

**–(pObj->m_uAutoReleaseCount);**

}

**m_pManagedObjectArray->removeAllObjects();**

}

}

void CCArray::removeAllObjects()

{

ccArrayRemoveAllObjects(data);

}

void ccArrayRemoveAllObjects(ccArray *arr)

{

while( arr->num > 0 )

{

**(arr->arr[--arr->num])->release();**

}

}

不出预料，当前自动释放池遍历每个“受控制”Object，–m_uAutoReleaseCount，并调用该object的release方法。

我们接着按释放流程来看看m_uAutoReleaseCount和m_uReference值的变化：

CCPoolManager::sharedPoolManager()->pop()； m_uReference = 0； m_uAutoReleaseCount = 0；

**五、自动释放池的初始化**

自动释放池本身是何时出现的呢？回顾一下Cocos2d-x引擎的初始化过程（android版），引擎初始化实在Render的onSurfaceCreated方法中进行的，我们不难追踪到以下代码：

//hellocpp/jni/hellocpp/main.cpp

Java_org_cocos2dx_lib_Cocos2dxRenderer_nativeInit {


//这里CCDirector第一次被创建

if (**!CCDirector::sharedDirector()->getOpenGLView()**)

{

CCEGLView *view = CCEGLView::sharedOpenGLView();

view->setFrameSize(w, h);

AppDelegate *pAppDelegate = new AppDelegate();

CCApplication::sharedApplication()->run();

}

}


CCDirector* CCDirector::sharedDirector(void)

{

if (!s_SharedDirector)

{

s_SharedDirector = new CCDisplayLinkDirector();

** s_SharedDirector->init();**

}

return s_SharedDirector;

}

bool CCDirector::init(void)

{

setDefaultValues();

… …

// create autorelease pool

**CCPoolManager::sharedPoolManager()->push();**

return true;

}

**六、探寻Cocos2d-x内核对象的自动化内存释放**

前面我们基本了解了Cocos2D-x的自动化内存释放原理。如果你之前翻看过一些Cocos2d-x的内核源码，你会发现很多内核对象都是通过单例模式create出来的，也就是说都使用了autorelease将自己放入自动化内存释放池中被管理。

比如我们在HelloCpp中看到过这样的代码：

//HelloWorldScene.cpp

bool HelloWorld::init() {

…. ….

// add "HelloWorld" splash screen"

**CCSprite* pSprite = CCSprite::create("HelloWorld.png");**

// position the sprite on the center of the screen

pSprite->setPosition(ccp(visibleSize.width/2 + origin.x, visibleSize.height/2 + origin.y));

// add the sprite as a child to this layer

**this->addChild(pSprite, 0);**

… …

}

CCSprite采用自动化内存管理模式create object（cocos2dx/sprite_nodes/CCSprite.cpp），之后将自己加入到HelloWorld这个CCLayer实例 中。按照上面的分析，create结束后，CCSprite object的m_uReference = 1； m_uAutoReleaseCount = 1。一旦如此，那么在下一帧时，该object就会被CCPoolManager释放掉。但我们在屏幕上依旧可以看到该Sprite的存在，这是怎么回事呢？

问题的关键就在this->addChild(pSprite, 0)这行代码中。addChild方法实现在CCLayer的父类CCNode中：

// cocos2dx/base_nodes/CCNode.cpp

void CCNode::addChild(CCNode *child, int zOrder, int tag)

{

… …

if( ! m_pChildren )

{

this->childrenAlloc();

}

**this->insertChild(child, zOrder);**

… …

}

void CCNode::insertChild(CCNode* child, int z)

{

m_bReorderChildDirty = true;

ccArrayAppendObjectWithResize(m_pChildren->data, child);

child->_setZOrder(z);

}

void ccArrayAppendObjectWithResize(ccArray *arr, CCObject* object)

{

ccArrayEnsureExtraCapacity(arr, 1);

ccArrayAppendObject(arr, object);

}

void ccArrayAppendObject(ccArray *arr, CCObject* object)

{

CCAssert(object != NULL, "Invalid parameter!");

object->retain();

arr->arr[arr->num] = object;

arr->num++;

}

又是一系列方法调用，最终我们来到了ccArrayAppendObject方法中，看到了陌生而又眼熟的retain方法调用。

在本文开始我们介绍CCObject时，我们知道retain是CCObject的一个方法，用于增加m_uReference计数。而实际上retain还隐含着“保留”这层意思。

在完成this->addChild(pSprite, 0)调用后，CSprite object的m_uReference = 2； m_uAutoReleaseCount = 1，这很关键。

我们在脑子里再过一下自动释放池释放object的过程：–m_uReference, –m_uAutoReleaseCount。一帧之后，两个值变成了m_uReference = 1； m_uAutoReleaseCount = 0。还记得前面说过的m_uAutoReleaseCount的另外一个非计数含义么，那就是表示该object是否“**受控**”，现在值为0，显然不再受自动释放池的控制了，后续即便再执行100次内存自动释放，也不会影响到该object的存活。

后续要想释放这个“精灵”，我们还是需要手工调用release，或再调用其autorelease方法。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

mark。。。

还记得前面说过的m_uAutoReleaseCount的另外一个非计数含义么，那就是表示该object是否“受控”，现在值为0，显然不再受自动释放池的控制了。 这句话哪里有代码表现啊,在object的析构里面吗?求解答啊