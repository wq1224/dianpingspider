# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import json
import copy
import pdb

class DianpingspiderPipeline(object):
	# collection_name = 'music'

 #    def __init__(self, mongo_uri, mongo_db):
 #        self.mongo_uri = mongo_uri
 #        self.mongo_db = mongo_db

 #    @classmethod
 #    def from_crawler(cls, crawler):
 #        return cls(
 #            mongo_uri=crawler.settings.get('MONGO_URI'),
 #            mongo_db=crawler.settings.get('MONGO_DATABASE', 'luoo')
 #        )

 #    def open_spider(self, sipder):
 #        self.client = pymongo.MongoClient(self.mongo_uri)
 #        self.db = self.client[self.mongo_db]

 #    def close_spider(self, spider):
 #        self.client.close()

 #    def process_item(self, item, spider):
 #        self.db[self.collection_name].insert(dict(item))
 #        return item

	def __init__(self, dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls, settings):
		'''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
		   2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
		   3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
		dbparams = dict(
		    host=settings['MYSQL_HOST'],  # 读取settings中的配置
		    db=settings['MYSQL_DBNAME'],
		    user=settings['MYSQL_USER'],
		    passwd=settings['MYSQL_PASSWD'],
		    charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
		    cursorclass=MySQLdb.cursors.DictCursor,
		    use_unicode=False,
		)
		dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
		return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

	# pipeline默认调用
	def process_item(self, item, spider):
		asynItem = copy.deepcopy(item)
		query = self.dbpool.runInteraction(self._conditional_insert, asynItem)  # 调用插入的方法
		query.addErrback(self._handle_error, asynItem, spider)  # 调用异常处理方法
		return item

	# 写入数据库中
	def _conditional_insert(self, tx, item):
		print "writing to item: " + item['shopname']
		sql = "insert into dianping(shopname,shoplevel,shopurl,commentnum,avgcost,taste,envi,service,foodtype,loc,poi,addr,label) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		#sql = "insert into dianping(shopname,shoplevel,shopurl,commentnum,avgcost,taste,envi,service,foodtype,loc) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		params = (item['shopname'], item['shoplevel'], item['shopurl'], item['commentnum'],item['avgcost'],item['taste'],item['envi'],item['service'],item['foodtype'],item['loc'],item['poi'],item['addr'],','.join(item['label']))
		#params = (item['shopname'], item['shoplevel'], item['shopurl'], item['commentnum'],item['avgcost'],item['taste'],item['envi'],item['service'],item['foodtype'],item['loc'])
		tx.execute(sql, params)

	# 错误处理方法
	def _handle_error(self, failue, item, spider):
		print failue
