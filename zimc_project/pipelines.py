# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ZimcProjectPipeline:
    def __init__(self):
        self.file = open('data.csv', 'w', newline='')
        self.csvwriter = csv.writer(self.file)
        # 定义存储csv的表头
        self.csvwriter.writerow(['标题', '链接', '日期', '详情（前50字）'])

    def process_item(self, item, spider):
        # 插入数据
        self.csvwriter.writerow([item["title"], item["url"], item["date"], item["detail"]])
        return item

    def close_spider(self, spider):
        # 关闭csv
        self.file.close()
