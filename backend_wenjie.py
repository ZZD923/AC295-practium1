from flask import Flask,request,Response,send_file
from flask_restful import Resource,Api
from PIL import Image
import requests
import dask.array as da
import numpy as np
from scipy import spatial
import glob
from tqdm import tqdm

app = Flask(__name__)
api = Api(app)
img_shape = (32,32)
gap_img_path = 'gap_images/gap_images/'
def resize_flatten_img(img):
    new_image = img.convert("RGB").resize(img_shape)
    img_array = np.asarray(new_image).reshape(-1,)
    return img_array

def cosine_similarity(img_a, img_b):
    img_a = resize_flatten_img(img_a).astype('float64'); img_b = resize_flatten_img(img_b).astype('float64')
    # print(img_a.dtype)
    # print(type(img_b))
    # print(da.dot(img_a,img_b).compute())
    # print(da.linalg.norm(img_a))
    #print("Shape of img a:", img_a.shape)
    #print("Shape of img b:", img_b.shape)
    cos_sim = da.dot(img_a, img_b) / (da.linalg.norm(img_a) * da.linalg.norm(img_b))
    return cos_sim.compute()

def find_most_similar_img(input_img):
    max_sim = -np.inf
    img_list = glob.glob(gap_img_path + '*.jpg')
    for img_b_path in tqdm(img_list):
        img_b = Image.open(img_b_path)
        sim = cosine_similarity(input_img, img_b)
        #print("Similarity is: ", sim)
        if sim > max_sim and sim < 1:
            max_sim = sim
            output_img = img_b_path
    # print("Path to the most similar image is: ", output_img)
    # print("Cosine similarity is: ", max_sim)
    return output_img

class GetSimilarImage(Resource):
    def get(self):
        return "Please use post method"
    def post(self):
        image = request.files['image_file']
        input_image=Image.open(image)

        sim = cosine_similarity(input_image, input_image)
        output_image = find_most_similar_img(input_image)
        return send_file(output_image, mimetype='image/jpeg')

class GetImagebyname(Resource):
    def get(self):
        return "Please use post method"
    def post(self):
        image_name = request.get_json()['image_name'] 
        image_path= 'gap_images/gap_images/'+image_name
        return send_file(image_path, mimetype='image/jpeg')

api.add_resource(GetSimilarImage, '/GetSimilarImage')
api.add_resource(GetImagebyname, '/GetImagebyname')
    
if __name__=="__main__":
    # determine what the URL for the database should be, port is always 8082 for DB

    app.run(host='0.0.0.0', port=8082, debug=True)


