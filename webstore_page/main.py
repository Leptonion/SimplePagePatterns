from flask import Blueprint, render_template, request
from sqlalchemy import or_, and_
from .db_patterns import Category, Product, ProductParameter, FilterParameter, Filter
from . import cursor

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def first_start():
    category = cursor.session.query(Category).first()
    products = cursor.session.query(Product)

    args = dict(request.args)

    search = args.pop("search") if "search" in args else None
    page = int(args.pop("page")) if "page" in args else 1

    if search:
        search = search.split(' ')
        search = [Product.keywords.like(f"%{x}%") for x in search]
        products = products.filter(or_(*search))

    products = dot_filters(products, args)

    pages = products.count() / 12
    pages = int(-1 * pages // 1 * -1)

    products = products.limit(12).offset((page - 1) * 12)

    return render_template('main.html', category=category, products=products, pages=list(range(1, pages + 1)))


def dot_filters(query, args: dict):
    """ Get filter args as dict, where key is Filter.transcription, and val is FilterParameter.transcription """

    for key, val in args.items():  # Go to all filter args
        """ Create subquery where we back a list of Filter.id with Filter.transcription == key """
        sub_query = cursor.session.query(Filter.id).filter(Filter.transcription == key).scalar_subquery()
        """ Create subquery where we back a list of Product.id (from ProductParameter.product_id)
            with FilterParameter.transcription in val_list and necessary Filter.id"""
        sub_query = cursor.session.query(ProductParameter.product_id).join(FilterParameter)\
            .filter(FilterParameter.feature_id.in_(sub_query),
                    FilterParameter.transcription.in_(val.split(',')))\
            .scalar_subquery()
        """ Get list of Products from filtered list of ID`s """
        query = query.filter(Product.id.in_(sub_query))
    return query


