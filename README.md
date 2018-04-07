# dianpingspider

1. pip install Scrapy
2. scrapy start project dianpingspider
3. scrapy crawl dianping
4. pip install MySQL-Python    
    (xcode-select --install, meet issue https://stackoverflow.com/questions/25994429/mysql-python-on-mac-osx-10-9-2-error-command-usr-bin-clang-failed-with-exit)
5. sudo pip install selenium
6. pip install "mitmproxy==0.18.2"

###注意事项
- 有时访问 http://www.dianping.com/shanghai/ch10/r8167 出现403，或者访问 http://www.dianping.com/shanghai/ch10/r8167p2 出现200但是无内容，需要更换ip地址重新访问

- 有时数据库会有重复或者串数据，原因：由于Spider的速率比较快，而scapy操作数据库操作比较慢，导致pipeline中的方法调用较慢，这样当一个变量正在处理的时候，一个新的变量过来，之前的变量的值就会被覆盖，解决方案是对变量进行保存，在保存的变量进行操作，通过互斥确保变量不被修改。
    #pipeline默认调用
    def process_item(self, item, spider):
        #深拷贝
        asynItem = copy.deepcopy(item)
        d = self.dbpool.runInteraction(self._do_upinsert, asynItem, spider)
详见 https://bbs.csdn.net/topics/391847368
同样多层scrapy pass meta数据时, 也需要使用这种方法避免数据重复
    yield Request(item['shopurl'], meta={'item':copy.deepcopy(item), 'phantomjs':True}, callback=self.parse_single_shop)
详见https://www.zhihu.com/question/57843251/answer/154608419

- 访问 http://www.dianping.com/shop/97572936 时只有200没有body,经调试添加更为真实的useragent可以解决此问题。
    DEFAULT_REQUEST_HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

- 每家商店的点评标签是ajax加载的，并且api call有token验证, 因此需要使用Phantomjs/Chrome headless 运行js, 参见 https://www.jianshu.com/p/b93c21401944
- 然而使用js运行技术仍然加载不到点评tag信息, 点评可以识别出是由selenium调用的chrome。
  解决方法：
  将window.navigator.webdriver设置为false  
  see https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver
  如何设置：
  需要在加载html前运行js:
    Object.defineProperty(navigator, "webdriver", {value: false,configurable: true});
  如何做到inject js:
  see https://intoli.com/blog/making-chrome-headless-undetectable/
  没有找到selenium能直接在所有js执行之前插入js的方法, 因此使用mitmproxy加上代理在webdriver请求html的时候对html插入js
    pip install "mitmproxy==0.18.2"
    mitmproxy -p 8080 -s "inject.py"


headless mode 参考
chrome headless
puppeteer https://developers.google.com/web/tools/puppeteer/

一些爬虫与反爬虫策略
http://imweb.io/topic/595b7161d6ca6b4f0ac71f05
http://python.jobbole.com/86502/
https://juejin.im/post/5a22af716fb9a045132a825c
https://www.zhihu.com/question/50738719
https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver

https://intoli.com/blog/making-chrome-headless-undetectable/

