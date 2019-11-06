from peewee import *

db = MySQLDatabase('python_spider', user='root', password='123456', host="localhost", port=3306, charset='utf8')

class BaseModel(Model):
    class Meta:
        database = db

class DDangBooks(BaseModel):
    id = IntegerField(primary_key=True, verbose_name='书id')
    name = CharField(verbose_name='书名')
    image_url = TextField(verbose_name='图片')
    author = CharField(verbose_name='作者')
    price = FloatField(default=0.0, verbose_name='价格')
    publisher = CharField(verbose_name='出版社')
    pub_time = DateFieldField(verbose_name='出版时间')
    title = CharField(verbose_name='标题')
    comment_nums = IntegerField(verbose_name='评论数')
    star_level = FloatField(verbose_name='评星')
    category_1 = CharField(verbose_name='一级分类')
    category_2 = CharField(default="", verbose_name='二级分类')
    category_3 = CharField(default="", verbose_name='三级分类')
    book_url = CharField(verbose_name='图书详情页')

if __name__ == "__main__":
    db.connect()
    if not db.table_exists(['ddangbooks']):
        db.create_tables([DDangBooks])
