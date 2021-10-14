from flask import Flask, jsonify, request, views
import os
from ..models import Product, Category, ProductMeta
from xplur.utility.utils import transform_list, AbstractView, api_response, get_pagination_resp
from .swagger import data
from sqlalchemy.orm import joinedload

class ProductView(AbstractView):
    singular_name = 'Product'
    model = Product

    def validate(self, data, product_id = None, is_partial=False):
        name_error = 'name is requied'
        sku_error = 'sku is requied'
        description_error = 'description is requied'
        data_req_error = 'data is requied'
        category_id_int_error = 'category_id must be an integer'
        category_not_found = 'category not found'
        products_exist = 'product with this sku already exist'
        price_not_float = 'price should be a float'
        if not is_partial:
            if not data:
                return {'error':data_req_error}
            if not data.get('name'):
                return {'error':name_error}
            if not data.get('sku'):
                return {'error': sku_error}
            if not data.get('description'):
                return {'error': description_error}

        if data.get('sku'):
            is_exist = self.model.query.filter_by(sku=data.get('sku')).all()
        
            if is_exist:
                if product_id :
                    if is_exist[0].id != product_id:
                        return {'error':products_exist}
                else:
                    return {'error':products_exist}

        if data.get('category_id'):
            if type(data.get('category_id')) != int:
                return {'error':category_id_int_error}

            category_instance = Category.query.filter_by(id=data.get('category_id')).all()
            if not category_instance:
                return {'error':category_not_found}

        if data.get('price') and type(data.get('price')) not in  [float, int]:
            print(type(data.get('price')))
            return {'error':price_not_float}

        filter_data = { }
        if data.get('name'):
            filter_data['name'] = data.get('name')
        if data.get('sku'):
            filter_data['sku'] = data.get('sku')
        if data.get('description'):
            filter_data['description'] = data.get('description')
        if data.get('category_id'):
            filter_data['category_id'] = data.get('category_id')

        return {'error':None, 'data':filter_data}

    def create_product_meta(self, req_data, product_id, is_post):
        products_meta_data = req_data.get('product_meta')
        products_meta_list = list()
        if products_meta_data:
            for key, value in products_meta_data.items():
                obj = ProductMeta(meta_key=key, meta_value=value, product_id=product_id)
                products_meta_list.append(obj)

            ProductMeta.query.filter_by(product_id=product_id).delete()
            products_meta_instance = ProductMeta.bulk_create(products_meta_list)
            return products_meta_instance
        return False

    def get(self):
        try:
            get_id = request.args.get('id')
            if get_id:
                instance = self.model.query.options(joinedload('category'), joinedload('products_meta')).filter_by(id = get_id).all()
                if not instance:
                    return api_response(message=f'{self.singular_name} not found', code=404, success=False)

                response_data = self.transform_single(instance[0])
                return api_response(message='ok', code=200, success=True, data=response_data)

            joins = ['category', 'products_meta']
            paginated_response = get_pagination_resp(self.model, request, joins)
            response_data = transform_list(self, paginated_response.get('data'))
            return api_response(message='ok', code=200, success=True, data=response_data, paginator=paginated_response.get('paginator'))
        except Exception as e:
            return api_response(message=[str(e.args[0])], code=500, success=False)
    
    def post(self):
        try:
            req_data = request.json
            validated_data = self.validate(req_data)
            if validated_data.get('error'):
                return api_response(message=validated_data.get('error'), code=400, success=False)
            
            instance = self.model.create(validated_data.get('data'))
            products_meta_instance = self.create_product_meta(req_data, instance.id, is_post=True)
            return api_response(message=f'{self.singular_name} created successfully', code=201, success=True)
        except Exception as e:
            return api_response(message=[str(e.args[0])], success=False,code=500)

    def put(self):
        try:
            req_data = request.json
            get_id = req_data.get('id')
            if not get_id:
                return api_response(message='id is requied', code=400, success=False)

            queryset = self.model.query.filter_by(id=get_id)
            if not queryset:
                return api_response(message=f'{self.singular_name} no found', code=404, success=False)

            validated_data = self.validate(req_data, product_id=queryset[0].id, is_partial=True)
            if validated_data.get('error'):
                return api_response(message=validated_data.get('error'), code=400, success=False)


            self.model.update(queryset, validated_data.get('data'))
            products_meta_instance = self.create_product_meta(req_data, queryset[0].id, is_post=False)
            return api_response(message=f'{self.singular_name} updated successfully', code=200, success=True)
        except Exception as e:
            return api_response(message=[str(e.args[0])], code=500, success=False)
        

    def delete(self):
        try:
            get_id = request.args.get('id')
            if not get_id:
                return api_response(message='id is requied', code=404, success=False)

            instance = self.model.query.filter_by(id=get_id).first()
            if not instance:
                return api_response(message=f'{self.singular_name} no found', code=404, success=False)

            obj = self.model.delete(instance)
            return api_response(message=f'{self.singular_name} deleted successfully', code=200, success=True)
        except Exception as e:
            return api_response(message=[str(e.args[0])], code=500, success=False)

    def transform_single(self, instance):
        res_dict = dict()
        res_dict['id'] = instance.id
        res_dict['sku'] = instance.sku
        res_dict['name'] = instance.name
        res_dict['category_id'] = instance.category_id
        res_dict['price'] = instance.price
        if instance.category:
            res_dict['category_name'] = instance.category.name 
        if instance.products_meta:
            products_meta_instance = instance.products_meta
            products_meta_dict = {}
            for obj in products_meta_instance:
                if obj.meta_key:
                    products_meta_dict[obj.meta_key] = obj.meta_value
            res_dict['product_meta'] = products_meta_dict 
        return res_dict

    def transform_product_meta(self, instance):
        res_dict = {}
        if instance.meta_key:
            res_dict[instance.meta_key] = instance.meta_value

        return res_dict