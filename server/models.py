from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# association table
customer_items = db.Table('customer_items', metadata, db.Column('customer_id',db.Integer, db.ForeignKey('customers.id'), primary_key=True),db.Column('item_id',db.Integer, db.ForeignKey('items.id'), primary_key=True))

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # define relationships
    reviews = db.relationship('Review', back_populates = 'customer')

    # association proxy
    #items = db.relationship('Review', secondary=customer_items, back_populates = 'customers')
    items = association_proxy('reviews', 'item', creator=lambda item_obj: Review(item=item_obj))


    serialize_rules = ('-reviews.customer',)

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'
    

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db. Integer, db.ForeignKey('items.id'))

    # define the relationship
    customer = db.relationship('Customer', back_populates = 'reviews')
    item = db. relationship('Item', back_populates = 'reviews')

    serialize_rules = ('-customer.reviews','-item.reviews',)


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # relationships
    reviews = db.relationship('Review', back_populates = 'item')

    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
