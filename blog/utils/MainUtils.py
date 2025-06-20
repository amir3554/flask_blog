from flask import request, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from flask_paginate import Pagination, get_page_parameter
from functools import wraps
import secrets
import string


def is_admin_test(func):
    """ensures that the current user is admin and has permessions"""
    @wraps(func)
    def actual_decorator(*args, **kwargs):
        if current_user.is_admin is True:
            return func(*args, **kwargs)
        else:
            abort(403)
    return actual_decorator


def Paginate(numbers_of_records, model_name, query) -> tuple[object,list]:
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = numbers_of_records
    query_list = model_name.query.order_by(query)
    total = query_list.count()
    offset = ( page - 1 ) * per_page
    query_per_page = query_list.limit(per_page).offset(offset)
    pagination = Pagination(page=page, total=total, per_page=per_page)
    return pagination, query_per_page 
    




def random_numeric_string(length: int) -> str:
    digits = string.digits  # "0123456789"
    return "".join(secrets.choice(digits) for _ in range(length))


