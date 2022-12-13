import scrapy
from zimc_project.items import ZimcProjectItem


class ZimcSpider(scrapy.Spider):
    name = 'zimc'
    allowed_domains = ['zimc.cn']
    start_urls = ['https://www.zimc.cn/index/ywdd.htm']

    def parse(self, response, *args, **kwargs):
        tr_list = response.xpath('//div[@class="right fr"]//li[position()>6 and position()<27]')
        for tr in tr_list:
            item = ZimcProjectItem()
            # 提取新闻标题
            item["title"] = tr.xpath("./a//text()").extract_first()
            # 提取链接
            url = tr.xpath("./a/@href").extract_first()
            url = ''.join(url).replace("../", "")
            # 链接拼接
            item["url"] = "https://www.zimc.cn/" + url
            # 发布时间
            item["date"] = tr.xpath("./i//text()").extract()[1][-11:-1]
            yield scrapy.Request(
                item["url"],
                callback=self.parse_detail,
                meta={"item": item}
            )

        # 翻页，一页20条数据
        for i in range(128, 130):
            next_url = "https://www.zimc.cn/index/ywdd/" + str(i) + ".htm"
            yield scrapy.Request(next_url, callback=self.parse)

    # 解析详情页
    def parse_detail(self, response):
        item = response.meta["item"]
        # 获取详情页的内容，并提取长度为50的字符串
        item["detail"] = ''.join(response.xpath("//p//text()").extract()).replace(" ", "").replace("\r\n", "")[0:50]
        yield item  # 对返回的数据进行处理
