from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200"])

client = MongoClient('mongodb://localhost:27017/')
db = client['bard_db']
regex_collection = db["forms"]


@app.route('/get-data', methods=['GET'])
def get_data():
    data = regex_collection.find({})
    response = []
    for d in data:
        item = {
            'type': d['type'],
            'bugid': d['bugid'],
            'bregex': d['bregex'],
            'all_eg': d['all_eg'],
            'blocked_eg': d['blocked_eg'],
            'status': d['status']
        }
        response.append(item)
    print('data', data)
    return jsonify(response)


@app.route('/submit-form', methods=['POST'])
def submit_form():
    form_data = request.get_json()
    # add status field to form_data with value "under review"
    form_data['status'] = 'under review'
    print(form_data)
    # save form_data to MongoDB using PyMongo
    db.forms.insert_one(form_data)
    print("Value of the form submitted")
    return {'message': 'Form data saved successfully'}


@app.route('/approve-item', methods=['POST'])
def approve_item():
    item = request.get_json()
    bugid = item['bugid']
    collection = regex_collection
    result = collection.update_one(
        {'bugid': bugid}, {'$set': {'status': 'approved'}})
    if result.modified_count > 0:
        return jsonify({'message': 'Item approved successfully'})
    else:
        return jsonify({'message': 'Failed to approve item'})


@app.route('/reject-item', methods=['POST'])
def reject_item():
    item = request.get_json()
    bugid = item['bugid']
    collection = regex_collection
    result = collection.update_one(
        {'bugid': bugid}, {'$set': {'status': 'rejected'}})
    if result.modified_count > 0:
        return jsonify({'message': 'Item rejected successfully'})
    else:
        return jsonify({'message': 'Failed to approve item'})


if __name__ == '__main__':
    app.run(debug=True)
