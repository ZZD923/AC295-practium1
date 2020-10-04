from flask import Flask,request,Response,send_file
from flask_restful import Resource,Api
from PIL import Image
import requests


app = Flask(__name__)
api = Api(app)

class GetSimilarImage(Resource):
    def get(self):
        
        return "Please use post method"
    def post(self):
        image = request.files['image_file']
        input_image=Image.open(image)
        return Response(response=f'Size of image {input_image.size}',status=200)

class GetImagebyname(Resource):
    def get(self):
        
        return "Please use post method"
    def post(self):
        image_name = request.get_json()['image_name'] 
        image_path= 'gap_images/'+image_name
        return send_file(image_path, mimetype='image/jpeg')

api.add_resource(GetSimilarImage, '/GetSimilarImage')
api.add_resource(GetImagebyname, '/GetImagebyname')
    
if __name__=="__main__":
    # determine what the URL for the database should be, port is always 8082 for DB

    app.run(host='0.0.0.0', port=8082, debug=True)


