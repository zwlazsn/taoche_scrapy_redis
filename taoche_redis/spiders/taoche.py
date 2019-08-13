# -*- coding: utf-8 -*-
import scrapy,re
from scrapy_redis.spiders import  RedisSpider
from taoche_redis.spiders.city import CITY_CODE,CAR_CODE_LIST
from taoche_redis.items import TaocheRedisItem

class TaocheSpider(RedisSpider):
    name = 'taoche'
    allowed_domains = ['taoche.com']
    # start_urls = ["https://shijiazhuang.taoche.com/bmw/"]

    redis_key = 'taoche:start_url'

    #https://beijing.taoche.com/audi/  城市和汽车品牌是可变的
    start_urls =[]

    for city in CITY_CODE:
        # print(city)
        for car in CAR_CODE_LIST:
            # 拼接完整的城市品牌url
            url = f"https://{city}.taoche.com/{car}/"
            # 将url添加进start_urls 中去
            start_urls.append(url)

    # print(start_urls)
    # print(len(start_urls))
    def parse(self, response):#获取每一个url
        # print(response)
        # 获取最大页码
        max_page = response.xpath("//div[@class='paging-box the-pages']"
                                  "/div/a[last()-1]/text()").extract()
        # print(max_page,response.url)  #查看url对应的max_page 是否为空
        sign = response.xpath("//h1/text()").extract() #暂时没有找到符合条件的二手车
        # print(max_page, sign,response.url)
        # 如果max_page 为真 则说明页码大于1
        if max_page:
            max_page = int(max_page[0])
            for page in range(1, max_page + 1):
                # 拼接完整的分页url
                page_url = response.url + f"?page={page}"
                # print(page_url)
                yield scrapy.Request(url=page_url, callback=self.parse_page_url, dont_filter=True)
        # 如果max_page 和sign都是空的 说明网页只有一页
        elif not max_page and not sign:
            #一页的情况 response.url
            # pass
            yield scrapy.Request(url=response.url,callback=self.parse_page_url)
        # else:

    def parse_page_url(self,response):
        # print(response)
        li_list = response.xpath("//ul[@class='gongge_ul']/li[@data-id]")
        # print(len(li_list))
        for li in li_list:
            # 获取图片
            pic = li.xpath(".//img/@data-src").extract()[0]
            pic = "https:" + pic
            # print(pic)

            # 获取标题
            title = li.xpath(".//a[@class='title']/span/text()").extract()[0]
            # print(title)

            # 获取价格
            price = li.xpath(".//i[@class='Total brand_col']/text()").extract()[0]
            price = float(re.sub("[万千]", "", price))
            # print(price)

            # 详情url
            detail_url = li.xpath(".//a[@class='title']/@href").extract()[0]
            detail_url = "https:" + detail_url
            # print(detail_url)

            # 实例化item
            item = TaocheRedisItem()
            item["pic"] = pic
            item["title"] = title
            item["price"] = price
            item["detail_url"] = detail_url

            yield scrapy.Request(url=detail_url, callback=self.parse_detail,
                                 meta={"data": item}, dont_filter=True)

    def parse_detail(self, response):
        # print(response)
        item = response.meta["data"]
        # print(item)

        # 车源号
        source_id = response.xpath("//span[contains(text(), '车源号')]/text()").extract()
        if source_id:
            source_id = int(re.findall("\d+", source_id[0])[0])
        else:
            source_id = ''
        # print(source_id)

        # 获取图片
        pic_list_1 = response.xpath("//ul[@id='taoche-details-piclist']/li/img/@data-zoomimage").extract()
        # print(len(pic_list), pic_list)
        pic_list = []
        # 拼接完整的图片url
        for p in pic_list_1:
            p = "https:" + p
            pic_list.append(p)
        # print(pic_list)
        pic_list = '#'.join(pic_list)
        # print(pic_list)

        # 注册日期
        regist_date = response.xpath("//dt[text()='上牌时间']/following-sibling::dd/text()").extract()
        if regist_date:
            regist_date = regist_date[0]
        else:
            regist_date = ''
        print(regist_date,source_id)

        # 长宽高
        ckg = response.xpath("//li[text()='长宽高']/span/text()").extract()
        if ckg:
            ckg =ckg[0]
        elif ckg == "- -":
            ckg = ""
        else:
            ckg =''
        print(regist_date,source_id,ckg)

        item["source_id"] = source_id
        item["pic_list"] = pic_list
        item["regist_date"] = regist_date
        item["ckg"] = ckg

        # print(item)

        yield item







