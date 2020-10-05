from flask import Flask,request,Response,send_file
from flask_restful import Resource,Api
from PIL import Image
import dask.dataframe as dd
import pandas as pd
import numpy as np
import requests
import tensorflow as tf
from dask.diagnostics import ProgressBar

app = Flask(__name__)
api = Api(app)

def read_and_resize(filename, resize_dim = (32,32)):
    im = Image.open('gap_images/'+ filename).convert('L')
    im = np.array(im)
    im = np.expand_dims(im, axis=2)
    resize_im = tf.cast(im, tf.float32)/255.
    resize_im = tf.image.resize(resize_im, resize_dim)
    return resize_im

def generate_sim_score(filepath, resized_input):
    im = read_and_resize(filepath)
    return np.sum(im*resized_input)/np.sqrt(np.sum(im*im) * np.sum(resized_input*resized_input))

class GetSimilarImage(Resource):
    def get(self):
        
        return "Please use post method"
    def post(self):
        image = request.files['image_file']
        input_image=Image.open(image).convert('L')
        input_image = np.array(input_image)
        input_image = np.expand_dims(input_image, axis=2)
        resize_image = tf.cast(input_image, tf.float32)/255.
        resize_image= tf.image.resize(resize_image, (32,32))
        meta = dd.read_csv('metadata.csv')
        meta['similarity']=meta['file_id'].apply(generate_sim_score,resized_input=resize_image,meta=('x', float))
        with ProgressBar():
            largest_row=meta.nlargest(2,'similarity').compute()
        image_id=largest_row['file_id'].values[1]
        image_path= 'gap_images/'+image_id
        return send_file(image_path, mimetype='image/jpeg')

class GetImagebyname(Resource):
    def get(self):
        
        return "Please use post method"
    def post(self):
        image_name = request.get_json()['image_name'] 
        artist = request.get_json()['artist'] 
        collection = request.get_json()['collection'] 
        genre = request.get_json()['genre'] 
        df=dd.read_csv("metadata.csv")
        if image_name !='':
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
        elif artist=='' and collection=='' and genre=='':
            return Response(response=f'No information provided',status=400)
        else:
            if artist!='':
                df=df[df['Artist']==artist]
            if collection!='':
                df=df[df['Collection']==collection]
            if genre !='':
                df=df[df['Genre']==genre]
            image_id=df.file_id.compute().values
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


