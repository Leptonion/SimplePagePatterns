from sqlalchemy import Column, Integer, Text, Float, Boolean, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship,scoped_session


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(Text, nullable=False)


class Filter(Base):
    __tablename__ = 'filter'

    id = Column(Integer, primary_key=True, nullable=False)
    category_id = Column(ForeignKey("category.id"), nullable=False)
    title = Column(Text, nullable=False)
    transcription = Column(Text, nullable=False)

    category = relationship('Category', backref='filters')


class FilterParameter(Base):
    __tablename__ = 'fparam'

    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(Text, nullable=False)
    feature_id = Column(ForeignKey("filter.id"), nullable=False)
    transcription = Column(Text, nullable=False)

    filter = relationship('Filter', backref="fparams")


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(Text, nullable=False)
    pic = Column(Text)
    price = Column(Float, nullable=False)
    availability = Column(Boolean, nullable=False)
    keywords = Column(Text, nullable=False)


class ProductParameter(Base):
    __tablename__ = 'pparam'

    id = Column(Integer, primary_key=True, nullable=False)
    product_id = Column(ForeignKey("product.id"), nullable=False)
    param_id = Column(ForeignKey("fparam.id"), nullable=False)

    product = relationship('Product', backref="pparams")


class DBConnector:
    def __init__(self):
        self.engine = create_engine("sqlite:///testfield/dbase/store.db")
        session_factory = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        self.session = scoped_session(session_factory)

    def create_db_file(self):
        Base.metadata.create_all(bind=self.engine)
