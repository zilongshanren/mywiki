---
title: 装饰器模式（Swift）
url: http://frankorz.com/2017/02/20/decorator-in-swift/
author: 文章作者 猫冬
published: '2017-02-20'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

阅读《大话设计模式》和《精通 Swift 设计模式》中的装饰器模式，本文为笔记。

简介
装饰器模式，可以用于在运行时选择性地修改对象的行为，在处理无法修改的类时能发挥其强大的能力。

我们可以在想修改对象的行为 时，又不想修改对象所属的类或其使用者 ，就可以使用装饰器模式。如果想修改对象的类实现，则不推荐使用装饰器模式，此时直接修改类往往更简单。

例子
阅读前请下载 OS X 命令工具行初始项目 Decorator_start ，项目中注释较详细，如有问题请联系我。

项目地址：Decorator_in_Swift


Purchase 类表示顾客在商店买了什么，其中定义了两个属性来存储商品名称和价格，还有两个计算属性把信息提供给外界。

CustomerAccount 类表示一组 Purchase 对象，代表了顾客所购买的商品，`addPurchase(Purchase)`

方法代表顾客购买了新商品。

Options 类中包含三个类，为前两个类提供了礼品服务，例如：2 元的礼品包装、1 元的彩带和 5 元的礼品配送。这里利用继承在 Options 类创建了三个装饰器类解决一个小问题——在不修改原来的两个类时添加了礼品服务功能。

Purchase 类和 CustomerAccount 类实现了创建一个用户对象，然后买一个特定价格的商品，如：张三购买了 10 元的帽子。后三个类则扩展了功能，能为每一个商品增加一个礼品服务的选项，如：张三购买了有彩带包装的 10 元的帽子。

但是已有的代码实现不了为一个商品添加多个礼品服务，如：张三购买了有礼品和彩带包装的 10 元的帽子。

源码运行结果：

1 2 3 4 Purchase Red Hat, Price ￥10.00 Purchase Scarf, Price ￥20.00 Purchase Scarf + delivery, Price ￥25.00 Total due: ￥55.00

装饰器模式
装饰器模式通过创建装饰器类解决上述组合问题（礼品包装+彩带、礼品包装+彩带+礼品配送等），装饰器类是指用于封装原始类并改变其行为的类。

装饰器类提供的 API 和封装的原始类相同，为了创建其他组合，装饰器还可以封装其他装饰器。

这里的单个礼品服务类 `Options.swift`

可以看做是一个小小的装饰器。


实现
装饰器类需要继承无法修改的类，来创建一个拥有该类所有方法和属性的类，用来替换原始类的功能。装饰器需要定义一个用来存储被封装对象的私有属性，从而为外界提供该对象的基本功能。

Options.swift

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 class BasePurchasDecorator : Purchase { private let wrappedPurchase: Purchase init (purchase : Purchase ) { wrappedPurchase = purchase super .init (product: purchase.description, price: purchase.totalPrice) } } class PurchaseWithGiftWrap : BasePurchasDecorator { override var description: String { return "\(super .description) + giftwrap" } override var totalPrice: Float { return super .totalPrice + 2 } } class PurchaseWithRibbon : BasePurchasDecorator { override var description: String { return "\(super .description) + ribbon" } override var totalPrice: Float { return super .totalPrice + 1 } } class PurchaseWithDelivery : BasePurchasDecorator { override var description: String { return "\(super .description) + delivery" } override var totalPrice: Float { return super .totalPrice + 5 } }

这里在开头创建了一个继承自 Purchase 类的礼品服务的基类 BasePurchasDecorator，并把原有礼品服务类的父类修改成了它。在 BasePurchasDecorator 类中，不仅定义了一个私有属性 `wrappedPurchase`

来保存 Purchase 对象（增加新功能 小节能看到用途），还会对礼品服务类的属性（`description`

和 `totalPrice`

）进行处理，以供继承的子类去根据自身的配送描述和价格修改其内容。

main.swift 修改为

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 let account = CustomerAccount (name: "Joe" )account.addPurchase(Purchase (product: "Red Hat" , price: 10 )) account.addPurchase(Purchase (product: "Scarf" , price: 20 )) account.addPurchase( PurchaseWithDelivery (purchase: Purchase (product: "Scarf" , price: 20 ))) account.addPurchase( PurchaseWithDelivery (purchase: PurchaseWithGiftWrap (purchase: Purchase (product: "Sunglasses" , price:25 )))) account.printAccount()

1 2 3 4 5 Purchase Red Hat, Price ￥10.00 Purchase Scarf, Price ￥20.00 Purchase Scarf + delivery, Price ￥25.00 Purchase Sunglasses + giftwrap + delivery, Price ￥32.00 Total due: ￥87.00

增加新功能
如果我们还想要用装饰器为原对象增加新的方法或属性，例如节日打折，我们可以继续定义一个折扣装饰器 `DiscountDecorator`

，并创建子类实现不同折扣。

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 class DiscountDecorator : Purchase { private let wrappedPurchase: Purchase init (purchase : Purchase ) { self .wrappedPurchase = purchase super .init (product: purchase.description, price: purchase.totalPrice) } override var description: String { return super .description } var discountAmount: Float { return 0 } func countDiscounts () -> Int { var total = 1 if let discounter = wrappedPurchase as? DiscountDecorator { total += discounter.countDiscounts() } return total } } class BlackFridayDecorator : DiscountDecorator { override var totalPrice: Float { return super .totalPrice - discountAmount } override var discountAmount: Float { return super .totalPrice * 0.20 } } class EndOfLineDecorator : DiscountDecorator { override var totalPrice: Float { return super .totalPrice - discountAmount } override var discountAmount: Float { return super .totalPrice * 0.70 } }

其中我们根据 `wrappedPurchase`

属性是否继承自折扣装饰器，来判断方法所包含的对象是否是有折扣的商品。例如下面代码中的 `EndOfLineDecorator(Purchase)`

方法所包含的对象： `BlackFirdayDecorator(purchase: PurchaseWithDelivery(purchase: PurchaseWithGiftWrap(purchase: Purchase(product: "Towel", price: 12))))`

有黑五折扣的礼品配送和礼品包装服务的12元太阳眼镜。

main.swift 中新增用了折扣的商品的代码

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 account.addPurchase( EndOfLineDecorator (purchase: BlackFridayDecorator (purchase: PurchaseWithDelivery (purchase: PurchaseWithGiftWrap (purchase: Purchase (product: "Towel" , price: 12 )))))) account.printAccount() for purchase in account.purchases { if let discountPurchase = purchase as? DiscountDecorator { print ("\(discountPurchase) has \(discountPurchase.countDiscounts()) discounts" ) } else { print ("\(purchase) has no discounts" ) } }

1 2 3 4 5 6 7 8 9 10 11 Purchase Red Hat, Price ￥10.00 Purchase Scarf, Price ￥20.00 Purchase Scarf + delivery, Price ￥25.00 Purchase Sunglasses + giftwrap + delivery, Price ￥32.00 Purchase Towel + giftwrap + delivery, Price ￥4.56 Total due: ￥91.56 Red Hat has no discounts Scarf has no discounts Scarf + delivery has no discounts Sunglasses + giftwrap + delivery has no discounts Towel + giftwrap + delivery has 2 discounts


如果想要让折扣只作用在产品价格而不对礼品服务做影响，也是很简单的。

main.swift

1 2 3 4 5 6 7 account.addPurchase( EndOfLineDecorator (purchase: PurchaseWithDelivery (purchase: PurchaseWithGiftWrap (purchase: BlackFridayDecorator (purchase: Purchase (product: "Towel" , price: 12 ))))))

1 2 3 4 ... Purchase Towel + giftwrap + delivery, Price ￥4.98 ... Towel + giftwrap + delivery has 1 discounts

计算折扣数的时候有点小问题，但是价格是对的。

用装饰器的时候需要谨慎，要评估对应用其他部分带来哪些影响，特别是已经使用了其他装饰器的情况下。

合并装饰器
装饰器可以为原始类新增新功能，也能合并装饰器。

注意：

装饰器的作用应该是增强或者拓展原始类的功能，而不是给现有的 API 渗透功能。
小项目中直接用多个独立的装饰器类会比较简单，对于复杂的项目会不便于维护，所以将相关联的装饰器类合并会比较合适。
Options.swift

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 class GiftOptionDecorator : Purchase { private let wrappedPurchase: Purchase private let options: [Option ] enum Option { case giftWrap case ribbon case delivery } init (purchase : Purchase , options : [Option ]) { self .wrappedPurchase = purchase self .options = options super .init (product: purchase.description, price: purchase.totalPrice) } override var description: String { var result = wrappedPurchase.description for option in options { switch option { case .giftWrap: result = "\(result) + giftwrap" case .ribbon: result = "\(result) + ribbon" case .delivery: result = "\(result) + delivery" } } return result } override var totalPrice: Float { var result = wrappedPurchase.totalPrice for option in options { switch option { case .giftWrap: result += 2 case .ribbon: result += 1 case .delivery: result += 5 } } return result } }

main.swift

1 2 3 4 5 6 7 account.addPurchase(EndOfLineDecorator (purchase: BlackFridayDecorator (purchase: GiftOptionDecorator (purchase: Purchase (product: "Towel" , price: 12 ), options: [GiftOptionDecorator .Option .giftWrap, GiftOptionDecorator .Option .delivery]))))

1 2 3 4 ... Purchase Towel + giftwrap + delivery, Price ￥4.56 ... Towel + giftwrap + delivery has 2 discounts


结果一样，但是实现方式简洁了不少。

合并装饰器的优点是能把类的核心职责和装饰功能区分开，去除相关类重复的装饰逻辑。

总结
完整的项目放在 Decorator_end 。

如果我们错误地实现了装饰器模式，那么装饰器所做的修改会对所有对象产生影响，或者另应用多出一些和对象无关的功能。

如增加新功能 小节中所提及的，实现装饰器模式后，要注意装饰顺序，否则不同的折扣就应用到不同的范围上了。

重申一遍，装饰器模式是在已有功能 上加更多 功能的一种方式，不能修改原始类的已有功能和属性。