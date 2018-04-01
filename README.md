# dianpingspider

1. pip3 install Scrapy
2. scrapy start project dianpingspider
3. scrapy crawl dianping
4. pip3 install MySQL-Python    
    (xcode-select --install, meet issue https://stackoverflow.com/questions/25994429/mysql-python-on-mac-osx-10-9-2-error-command-usr-bin-clang-failed-with-exit)

###注意事项
- 有时访问 http://www.dianping.com/shanghai/ch10/r8167 出现403，或者访问 http://www.dianping.com/shanghai/ch10/r8167p2 出现200但是无内容，需要更换ip地址重新访问
- 又是数据库会有重复或者串数据，原因：由于Spider的速率比较快，而scapy操作数据库操作比较慢，导致pipeline中的方法调用较慢，这样当一个变量正在处理的时候，一个新的变量过来，之前的变量的值就会被覆盖，解决方案是对变量进行保存，在保存的变量进行操作，通过互斥确保变量不被修改。
    #pipeline默认调用
    def process_item(self, item, spider):
        #深拷贝
        asynItem = copy.deepcopy(item)
        d = self.dbpool.runInteraction(self._do_upinsert, asynItem, spider)
详见https://bbs.csdn.net/topics/391847368
