from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'} 
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30))
    phone_number = db.Column(db.String(11))
    password_hash = db.Column(db.String(128))
    wallet = db.Column(db.Float(precision="7,2"), default=100)

    def __init__(self, username, phone_number, password) -> None:
        self.username = username
        self.phone_number = phone_number
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'} 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))  # 最多5个汉字加一个1符，16字节
    img_selected = db.Column(db.String(150))
    img = db.Column(db.String(150))

    def __init__(self, name, img_selected, img) -> None:
        self.name = name
        self.img_selected = img_selected
        self.img = img
    
    @property
    def serialize(self):
        products = Products.query.filter_by(category_id=self.id).all()
        return {
            'id':self.id,
            'name':self.name,
            'img_selected':self.img_selected,
            'img':self.img,
            'product': [product.serialize for product in products]
        }

class Products(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'} 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    name = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    introduction = db.Column(db.String(100))
    img = db.Column(db.String(150))
    img2 = db.Column(db.String(150))
    price = db.Column(db.Float(precision="7,2"))

    productcategory = db.relationship('ProductCategory', backref=db.backref("product_of_category"))

    def __init__(self, category_id, name, description, introduction, img, img2, price) -> None:
        self.category_id = category_id
        self.name = name
        self.description = description
        self.introduction = introduction
        self.img = img
        self.img2 = img2
        self.price = price

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id'            :self.id,
            'name'          :self.name,
            'intro'         :self.introduction,
            'description'   :self.description,
            'img'           :self.img,
            'img2'          :self.img2,
            'price'         :self.price
        }

class Mixture(db.Model):
    __tablename__ = 'mixture'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'} 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float(precision="7,2"))

    def __init__(self, name, price) -> None:
        self.name = name
        self.price = price

class ProductsMixture(db.Model):
    __tablename__ = 'products_mixture'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'} 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    mixture_id = db.Column(db.Integer, db.ForeignKey('mixture.id'))

    products = db.relationship('Products', backref=db.backref("products_mixture"))
    mixture = db.relationship('Mixture', backref=db.backref("products_mixture"))

    def __init__(self, products_id, mixture_id) -> None:
        self.products_id = products_id
        self.mixture_id = mixture_id

class Order(db.Model):
    __tablename__ = 'order'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'} 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id =  db.Column(db.Integer, db.ForeignKey('user_info.uid'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    num = db.Column(db.Integer)

    def __init__(self, user_id, product_id, num) -> None:
        self.user_id = user_id
        self.product_id = product_id
        self.num = num