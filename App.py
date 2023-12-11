from flask import Flask, request, jsonify, render_template, redirect, url_for, flash,json
from pymongo import MongoClient
from bson import Binary
import base64
from dotenv import load_dotenv
import os
from bson import ObjectId
from cloudinary.uploader import upload
import cloudinary


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nitin'  

          
cloudinary.config( 
  cloud_name = "dukhwifbt", 
  api_key = "632226813216255", 
  api_secret = "rMJBxDO8nhsW9qcIHOng8BkO6sE" 
)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
client = MongoClient(app.config['MONGO_URI'])
mongo = client.get_database("CUSTOMERS")  

customers_collection = mongo.c3


class Customer:
    def __init__(self, name, mobile, area, ip_address,image):
        self.name = name
        self.mobile = mobile
        self.area = area
        self.ip_address = ip_address
        self.image=image


    def to_dict(self):
        return {
            'name': self.name,
            'mobile': self.mobile,
            'area': self.area,
            'ip_address': self.ip_address,
            'image':self.image
        }


@app.route('/')
def index():
    all_data = customers_collection.find()
    return render_template("index.html", customers=all_data)

@app.route('/insert_customer', methods=['POST'])
def insert_customer():
    
        print(request.files['image'])
        if 'image' in request.files:
                image_file = request.files['image']
                try:
                    upload_result = upload(image_file)
                    image_url = upload_result['url']
                except:
                    image_url = 'https://icon-library.com/images/anonymous-avatar-icon/anonymous-avatar-icon-25.jpg'


                print(image_url)

        image = image_url
        name = request.form['name']
        mobile = request.form['mobile']
        area = request.form['area']
        ip_address = request.form['ip_address']

        customer = Customer(name, mobile, area, ip_address,image)

        result = customers_collection.insert_one(customer.to_dict())


        if result.inserted_id:
             flash("Customer inserted successfully.")
             return redirect(url_for('index'))       
        else:
            return jsonify({'success': False, 'message': 'Failed to insert customer'}), 500
    



# @app.route('/update_customer/<customer_id>', methods=['PUT'])
# def update_customer(customer_id):
#     data = request.get_json()
#     name = data['name']
#     mobile = data['mobile']
#     area = data['area']
#     ip_address = data['ip_address']

#     result = customers_collection.update_one(
#         {'_id': ObjectId(customer_id)},
#         {'$set': {'name': name, 'mobile': mobile, 'area': area, 'ip_address': ip_address}}
#     )

#     if result.modified_count > 0:
#         flash("Customer updated successfully.")
#         return jsonify({'success': True, 'message': 'Customer updated successfully'})
#     else:
#         return jsonify({'success': False, 'message': 'Customer not found or no changes applied'}), 404

@app.route('/update_customer/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    name = request.form['name']
    mobile = request.form['mobile']
    area = request.form['area']
    ip_address = request.form['ip_address']

    if 'image' in request.files:
        image_file = request.files['image']
        try:
            upload_result = upload(image_file)
            image_url = upload_result['url']
        except:
            image_url = 'https://icon-library.com/images/anonymous-avatar-icon/anonymous-avatar-icon-25.jpg'
    else:
        image_url = 'https://icon-library.com/images/anonymous-avatar-icon/anonymous-avatar-icon-25.jpg'

    update_data = {'name': name, 'mobile': mobile, 'area': area, 'ip_address': ip_address, 'image': image_url}

    result = customers_collection.update_one(
        {'_id': ObjectId(customer_id)},
        {'$set': update_data}
    )

    if result.modified_count > 0:
        flash("Customer updated successfully.")
        return jsonify({'success': True, 'message': 'Customer updated successfully'})
    else:
        return jsonify({'success': False, 'message': 'Customer not found or no changes applied'}), 404



@app.route('/delete_customer/<customer_id>', methods=['GET'])
def delete_customer(customer_id):
    if customer_id:
        result = customers_collection.delete_one({'_id': ObjectId(customer_id)})

        if result.deleted_count > 0:
            flash("Customer deleted successfully.")
            return redirect(url_for('index'))       
        else:
            return jsonify({'success': False, 'message': 'Customer not found'}), 404
    else:
        return jsonify({'success': False, 'message': 'Invalid request. Customer ID is required'}), 400

    


if __name__ == '__main__':
    app.run(debug=True)
