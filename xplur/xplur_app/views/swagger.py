from flasgger import Swagger, SwaggerView, Schema, fields



class ProductSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    category_id = fields.Integer()
    price = fields.Integer()


class ProductSwaggerView(SwaggerView):
    parameters = [
        {
            "id": 1,
        }
    ]
    responses = {
    "code": 200,
    "data": [
              {
                  "category_id": None,
                  "id": 2,
                  "name": "p2",
                  "price": None,
                  "sku": "p2"
              }
          ],
          "message": [
              "ok"
          ],
          "paginator": {
              "current_page": 1,
              "limit": 1,
              "total_count": 19,
              "total_pages": 19
          },
          "success": True
      }

    def get(self, palette):
        """
        Colors API using schema
        This example is using marshmallow schemas
        """
        all_colors = {
            'cmyk': ['cian', 'magenta', 'yellow', 'black'],
            'rgb': ['red', 'green', 'blue']
        }
        if palette == 'all':
            result = all_colors
        else:
            result = {palette: all_colors.get(palette)}
        return jsonify(result)