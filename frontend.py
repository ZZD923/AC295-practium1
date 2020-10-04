from flask import Flask,render_template,request,make_response,send_file
from flask_restful import Resource,Api
import requests
import io

app = Flask(__name__)
api = Api(app)

class GetImage(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)
    def post(self):
        image_name = request.form['imagename']
        db_url = "http://0.0.0.0:8082/GetImagebyname"
        resp = requests.post(url=db_url,json={'image_name':image_name})
        imagebyte=io.BytesIO(resp.content)
        imagebyte.seek(0)
        return send_file(imagebyte, mimetype='image/jpeg')

class SimilarImage(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('similar_image.html'),200,headers)
    def post(self):
        image = request.files['image_file']
        image.save('frontend_upload.jpg')
        url = "http://0.0.0.0:8082/GetSimilarImage"
        files = {
            'image_file': open('frontend_upload.jpg','rb')
        }
        resp = requests.post(url, files=files)
        return resp.text

api.add_resource(GetImage, '/GetImage')
api.add_resource(SimilarImage, '/SimilarImage')

if __name__=="__main__":
    app.run(debug=True)
    

