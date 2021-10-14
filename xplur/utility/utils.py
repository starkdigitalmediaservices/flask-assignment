from flask import Flask, jsonify, request, views
from .constant import PAGE_SIZE
from math import ceil
from sqlalchemy.orm import joinedload, backref

class AbstractView(views.MethodView):
    pass

def transform_list(self, queryset):
    # print(queryset.__dict__)
    return list(map(self.transform_single, queryset))

def get_pagination_resp(model, request, join=None):
    page_response = {"total_count": None, "total_pages": None,
                     "current_page": None, "limit": None}
    if request.args.get('type') == 'all':
        return {"data": model.query.all(), "paginator": page_response}

    page = int(request.args.get('page')) if request.args.get('page') else 1
    limit = int(request.args.get('limit')) if request.args.get('limit') else PAGE_SIZE
    if join:
        joins = [joinedload(i) for i in join]
        paginated_response = model.query.options(*joins).paginate(page, limit,error_out=False)
    else:
        paginated_response = model.query.paginate(page, limit,error_out=False)

    page_response = {"total_count": paginated_response.total, "total_pages":int(ceil(paginated_response.total/paginated_response.per_page) ),
                     "current_page": paginated_response.page, "limit": paginated_response.per_page}
    paginator = {"paginator": page_response}
    response_data = {"data": paginated_response.items, "paginator": paginator.get('paginator')}
    return response_data

def api_response(message, code, success, data={}, paginator={}):
    response_data = {"message": [message], "code": code, "success": success, "data": data}
    if paginator:
        response_data['paginator'] = paginator
    return jsonify(response_data), code