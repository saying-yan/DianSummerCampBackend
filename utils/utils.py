import json
from operator import le

from ..modules import *

json_file = "F:\\a学习\\Dian\\Web\\夏令营\\products.json"

def init_mysql():
    """
    从抓包抓到的json数据中读取信息写入数据库
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())
        categories = temp["data"]["categories"]
        for category in categories:
            category_name = category["name"]
            product_category = ProductCategory(category_name, category["category_image_url"], category["gary_category_image_url"])
            db.session.add(product_category)
            db.session.commit()
            c_id = product_category.id
            products = category["products"]
            for product_json in products:
                product_name = product_json["name"]
                description = product_json["description"]
                intro = product_json["intro"]
                imgs = product_json["images"]
                img1 = imgs[0]["url"]
                if len(imgs) > 1:
                    img2 = imgs[1]["url"]
                else:
                    img2 = ""
                price = float(product_json["price"])
                product = Products(c_id, product_name, description, intro, img1, img2, price)
                db.session.add(product)
                db.session.commit()

