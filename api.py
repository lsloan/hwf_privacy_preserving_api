from flask import Flask, request, g
from flask_restful import Resource, Api
from flask_restful_swagger import swagger

from privacy_preserving import PreserveCsv

app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='0.1')

class Count(Resource):
    @swagger.operation(
        dataType="number",
        parameters=[
            {
              "name": "query",
              "description": "DataFrame query by which to return a count.",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "path",
            }
          ],
        )
    def get(self, query):
        count = g.private_source.count(query)
        return count

api.add_resource(Count, '/count/<string:query>')

with app.app_context():
    g.private_source = PreserveCsv('./public_data/student-por.csv')
    app.run()
