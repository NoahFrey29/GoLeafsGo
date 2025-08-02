from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

names = {"Noah": {"Age": 19, "Gender": "male"},
         "Krupa": {"Age": 21, "Gender": "female"}}

class HelloWorld(Resource):
    def get(self, name, test):
        return names[name]

    def post(self):
        return {"data": "posted"}

api.add_resource(HelloWorld, "/helloworld/<string:name>/<int:test>")

if __name__ == "__main__":
    app.run(debug=True)