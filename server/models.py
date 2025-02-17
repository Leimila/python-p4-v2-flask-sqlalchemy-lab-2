from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# MetaData configuration for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy with metadata
db = SQLAlchemy(metadata=metadata)


# Customer model
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationship with Review
    reviews = db.relationship('Review', back_populates='customer')

    # Association Proxy to get items directly from reviews
    items = association_proxy('reviews', 'item')

    # SerializerMixin to handle serialization
    serialize_rules = ('-reviews.customer',)  # Avoid recursion by excluding reviews.customer

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


# Item model
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationship with Review
    reviews = db.relationship('Review', back_populates='item')

    # SerializerMixin to handle serialization
    serialize_rules = ('-reviews.item',)  # Avoid recursion by excluding reviews.item

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


# Review model
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # Relationships to Customer and Item
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    # SerializerMixin to handle serialization
    serialize_rules = ('-customer.reviews', '-item.reviews')  # Avoid recursion by excluding reviews

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}, {self.customer_id}, {self.item_id}>'
