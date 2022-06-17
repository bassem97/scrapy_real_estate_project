# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from asyncio import log

from itemadapter import ItemAdapter
import pymongo


class MongoDBPipeline:
    """Define an Item Pipeline to write data to MongoDB.
    An Item pipeline is just a regular Python class with some
    predefined methods that will be used by Scrapy.
    """

    def __init__(self, mongo_uri, mongo_db, mongo_coll):
        """Init the Item pipeline with settings for MongoDB."""
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):
        """Create a pipeline instance from a Crawler.
        A Crawler object provides access to all Scrapy core components
        like settings.
        This method must return a new instance of the pipeline.
        """
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "scraping"),
            mongo_coll=crawler.settings.get("MONGO_COLL_QUOTES", "realestate_items"),
        )

    def open_spider(self, spider):
        """Connect to MongoDB when the spider is opened."""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_coll]

    def close_spider(self, spider):
        """Close the connection to MongoDB when the spider is closed."""
        self.client.close()

    def process_item(self, item, spider):
        """Process the items one by one.
        Here you can filter some data, normalize the data, or save it
        to an external database as we are doing here.
        Specially, in modern Scrapy projects, ItemAdapter provides a
        common interface that can be used to deal with all kinds Item
        types such as dictionaries, Item objects, dataclass objects,
        and attrs objects.
        Reference:
          - https://docs.scrapy.org/en/latest/topics/items.html#item-types
        """
        item_dict = ItemAdapter(item).asdict()
        self.collection.insert_one(item_dict)
        return item


class ScrapyProjectPipeline:
    def process_item(self, item, spider):
        return item
