# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from dianpingspider.items import DianpingItem
import time
import sys
import pdb
import copy
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class DianpingSpider(Spider):
	name = 'dianping'
	allowed_domains = ['dianping.com']
	start_urls = ['http://www.dianping.com']
	#['http://www.dianping.com/shanghai/ch10/r8167']

	def parse(self, response):
		#yield Request("http://www.dianping.com/shop/97572936",callback=self.parse_single_shop)
		yield Request("http://www.dianping.com/shanghai/ch10/r8167",callback=self.parse_first)

	def parse_first(self,response):
		selector = Selector(response)
		pg = 0
		pages = selector.xpath('//div[@class="page"]/a/@data-ga-page').extract()

		if len(pages) > 0:
		    pg = pages[len(pages) - 2]

		pg=int(str(pg))+1
		#pg = 2
		url = str(response.url)

		for p in range(1,pg):
		    ul = url+'p'+str(p)
		    #using this way is much faster than chrome headless, so make it slower
		    #time.sleep(5)
		    yield Request(ul,callback=self.parse_list)

	def parse_list(self, response):
		item = DianpingItem()
		selector = Selector(response)
		div = selector.xpath('//div[@id="shop-all-list"]/ul/li')

		for dd in div:
		#if len(div)>0:
			#dd = div[0]
			shopnames = dd.xpath('div[2]/div[1]/a[1]/h4/text()').extract()
			item['shopname']=shopnames[0]
			print shopnames[0]

			shopurls = dd.xpath('div[2]/div[1]/a[1]/@href').extract()
			item['shopurl'] = str(shopurls[0])

			shoplevels = dd.xpath('div[2]/div[2]/span/@title').extract()
			item['shoplevel'] = shoplevels[0]

			commentnums = dd.xpath('div[2]/div[2]/a[1]/b/text()').extract()
			if len(commentnums)>0:
			    item['commentnum'] = commentnums[0]
			else:
			    item['commentnum'] = '0'

			avgcosts = dd.xpath('div[2]/div[2]/a[2]/b/text()').extract()
			# solve unicode problem see https://gitee.com/ldshuang/imax-spider/commit/1d05d7bafdf7758f7b422cc1133abf493bf55086
			if len(avgcosts) > 0:
			    item['avgcost'] = filter(str.isdigit, str(avgcosts[0].encode('utf-8')))
			else:
			    item['avgcost'] = '0'

			tastes = dd.xpath('div[2]/span/span[1]/b/text()').extract()
			if len(tastes) > 0:
			    item['taste'] = tastes[0]
			else:
			    item['taste'] = '0'

			envis = dd.xpath('div[2]/span/span[2]/b/text()').extract()
			if len(envis) > 0:
			    item['envi'] = envis[0]
			else:
			    item['envi'] = '0'

			services = dd.xpath('div[2]/span/span[3]/b/text()').extract()
			if len(services) > 0:
			    item['service'] = services[0]
			else:
			    item['service'] = '0'

			foodtypes = dd.xpath('div[2]/div[3]/a[1]/span/text()').extract()
			item['foodtype'] = foodtypes[0]

			locs = dd.xpath('div[2]/div[3]/a[2]/span/text()').extract()
			item['loc'] = locs[0]

			addrs = dd.xpath('div[2]/div[3]/span/text()').extract()
			item['addr'] = addrs[0]

			#sometimes ip is banned by dianping, use this way to continue work
			if not self.hasResult(item['shopurl']):
				#time.sleep(3)
				yield Request(item['shopurl'], meta={'item':copy.deepcopy(item), 'phantomjs':True}, callback=self.parse_single_shop)

	def hasResult(self,url):
		settings = self.settings
		dbparams = dict(
			host=settings['MYSQL_HOST'],  # 读取settings中的配置
			db=settings['MYSQL_DBNAME'],
			user=settings['MYSQL_USER'],
			passwd=settings['MYSQL_PASSWD']
		)
		db = MySQLdb.connect(dbparams['host'], dbparams['user'], dbparams['passwd'], dbparams['db'], charset='utf8' )
		cursor = db.cursor()
		sql = "select * from dianping where shopurl='%s'" % url
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()
			if len(results) > 0:
				return True		
		except:
		   print "Error: unable to fecth data"
		db.close()
		return False

	def parse_single_shop(self, response):
		item = response.meta['item']
		selector = Selector(response)

		# get comment label
		item['label'] = []
		commentdiv = selector.xpath('//div[@id="summaryfilter-wrapper"]/div/div[@class="content"]/span')
		if len(commentdiv) > 0:
			for labelspan in commentdiv:
				label = labelspan.xpath('a/text()').extract()
				item['label'].append(label[0])

		# get map poi
		item['poi'] = ""
		mapsrc = selector.xpath('//div[@id="map"]/img/@src').extract()
		if len(mapsrc) > 0 :
			mapsrc = mapsrc[0]
			item['poi'] = mapsrc[mapsrc.index("|")+1:len(mapsrc)]

		print "parse item " + item['shopname']

		yield item
         
