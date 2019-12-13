from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import uuid 
from crawl import *

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)


# Image Class/Model
class Image(db.Model):
    image_id = db.Column(db.Integer,primary_key=True)
    job_id = db.Column(db.String)
    url = db.Column(db.String)

    def __init__(self,job_id,url):
        self.job_id = job_id
        self.url  = url

# Image Schema
class ImageSchema(ma.Schema):
    class Meta:
        fields = ('job_id','url')

# Domain Class/Model
class Domain(db.Model):
    domain_id = db.Column(db.Integer,primary_key=True)
    job_id = db.Column(db.String)
    url = db.Column(db.String)

    def __init__(self,job_id,url):
        self.job_id = job_id
        self.url  = url

# Domain Schema
class DomainSchema(ma.Schema):
    class Meta:
        fields = ('job_id','url')

# Init schema
image_schema = ImageSchema()
images_schema = ImageSchema(load_only=('image_id','job_id'),many=True)
domain_schema = DomainSchema()
domains_schema = DomainSchema(load_only=('domain_id','job_id'),many=True)



@app.route('/', methods = ['POST'])
def add_images():
    nb_thread = request.args.get('threads',default = 0,type = int)
    data = request.get_json()
    urls = data['urls']

    # Crawl urls to find images
    images = crawl(nb_thread,urls)

    # Generate an uuid
    id = str(uuid.uuid4())

    # Put crawled domain in the database
    for url in urls:
        new_domain = Domain(id,url)
        db.session.add(new_domain)
        db.session.commit()

    # Create Images in database
    for image in images:
        new_image = Image(id,image)
        db.session.add(new_image)
        db.session.commit()

    # Create JSON output file
    json = jsonify(
        job_id = id,
        urls = urls,
    )

    return make_response(json,200)


    
@app.route('/status/<id>', methods = ['GET'])
def get_images(id):
    all_images = Image.query.filter_by(job_id=id) 
    images = images_schema.dump(all_images)

    all_domains = Domain.query.filter_by(job_id=id)
    domains = domains_schema.dump(all_domains)

    urls = list()
    for image in images:
        urls.append(image.get('url'))

    crawled_domain = list()
    for domain in domains:
        crawled_domain.append(domain.get('url'))
        
    json = jsonify(
        job_id = id,
        domain = crawled_domain,
        urls = urls,
    )
        
    return make_response(json,200)



# Run Server
if __name__ == '__main__':
    app.run(debug=True, port=8080)

    




