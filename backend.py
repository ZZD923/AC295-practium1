from flask import Flask,request,Response,send_file
from flask_restful import Resource,Api
from PIL import Image
import dask.dataframe as dd
import pandas as pd
import numpy as np
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
        df=dd.read_csv("metadata.csv")
        if image_name[-4:]!='.jpg':
            full_image_name=image_name+'.jpg'
        else:
            full_image_name=image_name
        df_select=df[df['original_image_name']==full_image_name]
        image_id=df_select.file_id.compute().values
        if image_id.shape[0]==0:
            return Response(response=f'No such image {image_name} in the database',status=400)
        else:
            image_path= 'gap_images/'+image_id[0]
            return send_file(image_path, mimetype='image/jpeg')

api.add_resource(GetSimilarImage, '/GetSimilarImage')
api.add_resource(GetImagebyname, '/GetImagebyname')
    
if __name__=="__main__":
    # determine what the URL for the database should be, port is always 8082 for DB

    app.run(host='0.0.0.0', port=8082, debug=True)


