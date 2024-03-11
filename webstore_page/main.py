from flask import Blueprint, render_template, request
from sqlalchemy import or_
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

    for key, val in args.items():

        sub_query = cursor.session.query(Filter.id).filter(Filter.transcription == key).scalar_subquery()
        sub_query = cursor.session.query(ProductParameter.product_id).join(FilterParameter)\
            .filter(FilterParameter.feature_id.in_(sub_query),
                    FilterParameter.transcription.in_(val.split(',')))\
            .scalar_subquery()

        query = query.filter(Product.id.in_(sub_query))

    return query


