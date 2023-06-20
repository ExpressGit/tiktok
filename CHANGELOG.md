# [](https://github.com/imgyh/tiktok/compare/v1.6.4...v) (2023-05-28)


### Bug Fixes

* **webapi:** 修复作品列表为空时不返回cursor ([1e69ee8](https://github.com/imgyh/tiktok/commit/1e69ee8a140b7761f3ebdebf1b1d9e31af79bd2c)), closes [#40](https://github.com/imgyh/tiktok/issues/40)


### Features

* **douyin:** 修改文件名命名风格 ([b38e210](https://github.com/imgyh/tiktok/commit/b38e2109271a07e408bbbad2454ebc99f48437fe))



# [](https://github.com/imgyh/tiktok/compare/v1.6.3...v) (2023-05-21)


### Features

* **tiktok:** 规范包目录结构 ([942bc35](https://github.com/imgyh/tiktok/commit/942bc359126a0ce9241b44576063bf42b161d02a))
* **tiktok:** 删除多余文件 ([2114bc9](https://github.com/imgyh/tiktok/commit/2114bc925edf8c050834f1ba2f3ddb4be22b6ed3))



# [](https://github.com/imgyh/tiktok/compare/v1.6.2...v) (2023-04-24)


### Bug Fixes

* **tiktok:** 优化视频链接获取 ([321d462](https://github.com/imgyh/tiktok/commit/321d4622a16a26cc8587e16c0e5b9f8601c16f99))
* **web:** 解决浏览器提示不安全问题 ([87b48ae](https://github.com/imgyh/tiktok/commit/87b48aec06bce777c427d03ab02590fd7089bb9b))


### Features

* **tiktok:** 增加数据库功能与增量更新功能 ([ebf6671](https://github.com/imgyh/tiktok/commit/ebf6671d336767595a01941562db397546ab2fe9)), closes [#24](https://github.com/imgyh/tiktok/issues/24)



# [](https://github.com/imgyh/tiktok/compare/v1.6.1...v) (2023-04-21)


### Bug Fixes

* **result:** 修复1080p清晰度链接 ([ada1851](https://github.com/imgyh/tiktok/commit/ada1851e869ae4a65a43fb07eff3c22baeced087))
* **tiktok:** 修复接口失效问题 ([9aaab2f](https://github.com/imgyh/tiktok/commit/9aaab2f691adff5f43c0f40899b1eb37cd4665d5)), closes [#33](https://github.com/imgyh/tiktok/issues/33)


### Features

* **web:** 前段静态文件使用国内cdn ([72aca75](https://github.com/imgyh/tiktok/commit/72aca75960b0f2fe4ef918682debec5c9af8cb59))



# [](https://github.com/imgyh/tiktok/compare/v1.6.0...v) (2023-04-16)


### Bug Fixes

* **command:** 修复mode命令解析问题 ([aebc144](https://github.com/imgyh/tiktok/commit/aebc14429ded01203b2d3b3385d7f1bdcbafae1a))
* **tiktok:** 增加请求重试机制 ([8f6c1ea](https://github.com/imgyh/tiktok/commit/8f6c1ea70dd4da63c772f45f0326047deb3daef7))
* **tiktok:** 更改多作品接口请求逻辑, 不再调用单个作品的方法 ([2ea2ac0](https://github.com/imgyh/tiktok/commit/2ea2ac07a844421d665684e3273c3b6b8e7064a6))
* **tiktok:** 缩短文件名长度,只使用数字字母汉字作为文件名 ([99c6292](https://github.com/imgyh/tiktok/commit/99c62922ca701de2e7eccb68b3c3e67b98d9fcef)), closes [#19](https://github.com/imgyh/tiktok/issues/19)
* **web:** 前端适配新接口 ([2f13bd5](https://github.com/imgyh/tiktok/commit/2f13bd5122b25e507cf55a58aea24396016414da))


### Features

* **command:** 未传入cookie则使用默认值 ([596a0fc](https://github.com/imgyh/tiktok/commit/596a0fc63308c2ea515c305161f115e6914f7504))
* **web:** 增加解析接口 ([918d6c9](https://github.com/imgyh/tiktok/commit/918d6c9ebaa47ce7259fc2f23efbd53b320095a9)), closes [#28](https://github.com/imgyh/tiktok/issues/28)
* **web:** 所有接口支持json与form两种格式, cookie不传使用默认值 ([d3d091d](https://github.com/imgyh/tiktok/commit/d3d091d9ddadf1f01588b7e273b40356ed09cfa2)), closes [#31](https://github.com/imgyh/tiktok/issues/31)



# [](https://github.com/imgyh/tiktok/compare/v1.5.5...v) (2023-03-28)


### Bug Fixes

* **tiktok:** 使用tqdm进度条 ([f55dd00](https://github.com/imgyh/tiktok/commit/f55dd004e9eea039fea04ed9e8e1325bca62c363))
* **tiktok:** 修复主页作品获取失败 ([c5b9ec5](https://github.com/imgyh/tiktok/commit/c5b9ec5faf90c4d00c5cc24b48a774404344be19)), closes [#15](https://github.com/imgyh/tiktok/issues/15)
* **tiktok:** 修复获取单个合集id失败 ([f753c5c](https://github.com/imgyh/tiktok/commit/f753c5c52e4fa54f04f05d555d61b22b544a2169))
* **tiktok:** 修复配置文件路径获取问题 ([2496ccd](https://github.com/imgyh/tiktok/commit/2496ccd90ca5232c61a2ed213f85235fa26354b3))
* **tiktok:** 修改文件名匹配正则表达式 ([8ce13c0](https://github.com/imgyh/tiktok/commit/8ce13c0d72379accbfd38ba083728df87719d471))
* **tiktok:** 增加文件下载失败重试机制 ([794632d](https://github.com/imgyh/tiktok/commit/794632d6c5dce68b9eade8094e74231aa90421f0))
* **tiktok:** 缩短文件名长度 ([01fbd74](https://github.com/imgyh/tiktok/commit/01fbd743f82552e52099637871246ddc21949fc2))
* **tiktok:** 重试失败后返回已经获取到的数据, 而不是抛异常 ([9fc37f1](https://github.com/imgyh/tiktok/commit/9fc37f1048fbd182e00eea89b71ec644f7d9df56))


### Features

* **tiktok:** 使用rich进度条 ([0fb3739](https://github.com/imgyh/tiktok/commit/0fb3739b4734910b6a0d35fdb0033921ef854adb))
* **tiktok:** 单个作品使用多线程下载 ([38fc768](https://github.com/imgyh/tiktok/commit/38fc76826d20257ec63bb7fcdea6eeca38a8aa6d))
* **tiktok:** 增加json数据是否保存的开关 ([8ea8871](https://github.com/imgyh/tiktok/commit/8ea8871cc88b1199bfcb6c2ff7aef16fd1f733c3))
* **tiktok:** 增加配置文件, 手动传入自己的cookie ([ec559e2](https://github.com/imgyh/tiktok/commit/ec559e2913c70836b97ea2634604ac6ca6734a60)), closes [#16](https://github.com/imgyh/tiktok/issues/16)
* **tiktok:** 支持电脑网页版url作为链接 ([c9ece0b](https://github.com/imgyh/tiktok/commit/c9ece0bf502c1a6a6e6b2e12c8ffcbce3303ce6a))
* **tiktok:** 进度条滚动显示 ([20350b8](https://github.com/imgyh/tiktok/commit/20350b8889343bb93ec60081e6369f96d868203b))



# [](https://github.com/imgyh/tiktok/compare/v1.5.4...v) (2023-03-22)


### Bug Fixes

* **tiktok:** 修改命令行帮助提示信息 ([e194a28](https://github.com/imgyh/tiktok/commit/e194a2818b64aaa9b2a5ab172302c87a4f4a5790))
* **tiktok:** 修改文件夹名的正则匹配逻辑 ([4c1a4ed](https://github.com/imgyh/tiktok/commit/4c1a4ed950476c0945bf7986254d75d108d3019f)), closes [#11](https://github.com/imgyh/tiktok/issues/11)
* **tiktok:** 单个作品不使用多线程 ([939a417](https://github.com/imgyh/tiktok/commit/939a417654183a2ac2766a25bdecc13575752e61))
* **tiktok:** 获取x-bogus错误后重试, 单个作品不使用多线程 ([f8ec5e3](https://github.com/imgyh/tiktok/commit/f8ec5e3745d587d08dcba6464a0f990913f55ce5))
* **utils:** 优化获取x-bogus时出错的提示信息 ([f224557](https://github.com/imgyh/tiktok/commit/f2245574611f125f69be9bbe9a2d376c0241bc87))


### Features

* **live:** 直播解析支持APP端分享链接 ([e4a0ebb](https://github.com/imgyh/tiktok/commit/e4a0ebba4f39cc55e8d070e12b6597ab5c3745d3))
* **tiktok:** 使用线程池代替手动创建线程 ([89d4c7c](https://github.com/imgyh/tiktok/commit/89d4c7cd4253cd3ac885b55774dff2853c0d6e4f))
* **web:** 前端提示信息优化 ([d9c224b](https://github.com/imgyh/tiktok/commit/d9c224bd2d5fd382fb22b37f5e68a85894bb9aef))



# [](https://github.com/imgyh/tiktok/compare/v1.5.3...v) (2023-03-16)


### Bug Fixes

* **tiktok:** 修复接口未返回数据时重复请求的死循环(10s后还是未返回就抛异常) ([8c5863d](https://github.com/imgyh/tiktok/commit/8c5863d44f4ae4a5242c8191f98bc0f3936e8e84))
* **tiktok:** 修复无法获取图集id ([85942f2](https://github.com/imgyh/tiktok/commit/85942f2ffce97d853dab96da87737d98f450347e)), closes [#10](https://github.com/imgyh/tiktok/issues/10)


### Features

* **tiktok:** 适配多线程下载 ([83e4632](https://github.com/imgyh/tiktok/commit/83e46322ee13bd14841332538fef22e27e2f0e59))



# [](https://github.com/imgyh/tiktok/compare/v1.5.2...v) (2023-03-05)


### Bug Fixes

* **web:** 取消指定端口为必选项 ([1b85b19](https://github.com/imgyh/tiktok/commit/1b85b1989119cb35888e4e2d4f4018ed276f68d2))


### Features

* **live:** 增加直播解析方法的提示信息开启或关闭选项 ([469fe2c](https://github.com/imgyh/tiktok/commit/469fe2c5217ff22e42c1523d089a119415266c23))
* **url:** 添加速度更快的X-Bogus接口 ([7c44b94](https://github.com/imgyh/tiktok/commit/7c44b9426dc30f3be97d6e5824bf628c47276a87))
* **web:** 增加命令行指定web端口 ([98a9f74](https://github.com/imgyh/tiktok/commit/98a9f74d4b0b319ea1aeb3883c105c0b805105f1))



# [](https://github.com/imgyh/tiktok/compare/v1.5.1...v) (2023-03-04)


### Bug Fixes

* **live:** 修复无法播放http的直播地址 ([04ec0f1](https://github.com/imgyh/tiktok/commit/04ec0f1c400adb5bfacf74dca0114ec9d625e3cc))


### Features

* **live:** 适配web端的直播解析 ([f7fdcd1](https://github.com/imgyh/tiktok/commit/f7fdcd141b3a9877f5fd888383bfa48875d023bf))
* **tiktok:** 支持本地生成X-Bogus ([#3](https://github.com/imgyh/tiktok/issues/3)) ([a4328cd](https://github.com/imgyh/tiktok/commit/a4328cd53bd8a0342cf053050a8066130e008cde))
* **utils:** 重新加入远程调用X-Bogus接口作为备用,防止本地没有JS环境 ([4467018](https://github.com/imgyh/tiktok/commit/44670186afdcb1314194b0c00f39d1baa9681985))
* **web:** 增加web端直播解析 ([90aa105](https://github.com/imgyh/tiktok/commit/90aa10515f7bc90ed35c9484e2993083a533d6cc))



# [](https://github.com/imgyh/tiktok/compare/v1.5.0...v) (2023-03-02)


### Bug Fixes

* **tiktok:** cookies增加passport_csrf_token ([ebe3be4](https://github.com/imgyh/tiktok/commit/ebe3be43ef676c39cd1cd63cc606df1a9e5b1995))



#  (2023-03-02)


### Bug Fixes

* **command:** 修复头像封面音乐总是会下载 ([665ca47](https://github.com/imgyh/tiktok/commit/665ca47b08623699606d56e424eb096a92afa9fe))
* **tiktok:** 自动获取ttwid ([c6bcff6](https://github.com/imgyh/tiktok/commit/c6bcff67da8a659afb1c722ab40da733f1a79403))


### Features

* **tiktok:** 增加下载前n个作品功能 ([4efeb62](https://github.com/imgyh/tiktok/commit/4efeb62701acc6cf8d9fd06d1a80499a7ad5c6cc))
* **tiktok:** 增加音乐合集批量下载功能 ([b3aadf6](https://github.com/imgyh/tiktok/commit/b3aadf630ad8be9b79fa26a18799336c38569645))
* **url:** 增加音乐合集URL ([fa635eb](https://github.com/imgyh/tiktok/commit/fa635ebe7f70478e8408b5a8afe30ff0b1ff890f))



#  (2023-02-23)


### Bug Fixes

* **live:** 统一直播获取的header, 直播接口添加X-Bogus ([197d126](https://github.com/imgyh/tiktok/commit/197d12627d855f3353dba3fd68f0b308593f62e8))
* **tiktok:** 修复主页作品接口 ([e3029be](https://github.com/imgyh/tiktok/commit/e3029be42b021dcdad0736800a4f13428ddd5b98))
* **tiktok:** 修复用户主页作品接口 ([8a01e68](https://github.com/imgyh/tiktok/commit/8a01e681b5206c27a44f4ba10f840e856686e33b))
* **tiktok:** 添加单个作品获取失败后重试逻辑 ([ac73a97](https://github.com/imgyh/tiktok/commit/ac73a97c19840bd7147f3a7e4b400a37b1365fb2))


### Features

* **tiktok:** 增加合集下载功能 ([b95d718](https://github.com/imgyh/tiktok/commit/b95d7188282de5474861043ab011ed27baa79796))



#  (2023-02-20)


### Bug Fixes

* **tiktok:** 修复主页作品接口与直播接口 ([909b9f3](https://github.com/imgyh/tiktok/commit/909b9f3f1cec9684da33f63aeb816aaab2e7e6b9))
* **tiktok:** 修复主页作品接口获取数据不稳定, 增加X-Bogus接口限制 ([62072e8](https://github.com/imgyh/tiktok/commit/62072e881eb3531df68f9fe6d8bdab03a4f00790))


#  (2023-02-13)


### Bug Fixes

* **tiktok:** 修改X-Bogus接口 ([abb9a8e](https://github.com/imgyh/tiktok/commit/abb9a8e857ea98b38b47e3419554dfe490ec1d78))


#  (2023-02-11)


### Bug Fixes

* **tiktok:** 修复失效API，增加X-Bogus ([53d3b58](https://github.com/imgyh/tiktok/commit/53d3b5875ecd4de57f4dc4df4c228cf80b15c764))


#  (2023-01-30)


### Features

* **tiktok:** 初始提交 ([74f9c91](https://github.com/imgyh/tiktok/commit/74f9c91e75b324ae5e0dc5f9fa5bc4baf4611bd2))



