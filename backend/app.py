from flask_cors import CORS
import re
import json
from flask import Flask, jsonify
from pymongo import MongoClient

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def extract_apn_properties(input_text):
    apn_properties = []
    current_apn = None
    context_name = None

    # Define a regex pattern
    apn_pattern = re.compile(r'^\s*apn\s+([^ ]+)\s*$')
    context_pattern = re.compile(r'^\s*context\s+([^ ]+)$')

    # Iterate through each line in the input text
    for line in input_text.splitlines():
        # Check if the line matches the 'apn' pattern
        apn_match = apn_pattern.match(line)
        context_match = context_pattern.match(line)
        if context_match:
            context_name = context_match.group(1)
            print(context_name)
        if apn_match:
            # If a new 'apn' is found, store the current one and start a new one
            if current_apn:
                apn_properties.append(current_apn)
            current_apn = {"apn": apn_match.group(1), "context_name": context_name, "properties": {}}
        elif current_apn:
            # If within an 'apn' block, parse and add properties
            key_value = line.strip().split(' ', 1)
            if len(key_value) == 2:
                key, value = key_value
                if key in current_apn["properties"]:
                    # If property already exists, convert its value to a list and append the new value
                    if not isinstance(current_apn["properties"][key], list):
                        current_apn["properties"][key] = [current_apn["properties"][key]]
                    current_apn["properties"][key].append(value)
                else:
                    current_apn["properties"][key] = value
    # Add the last 'apn' properties to the list
    if current_apn:
        apn_properties.append(current_apn)
    print(len(apn_properties))
    return apn_properties


def convert_to_json(apn_properties):
    # Convert list of dictionaries to JSON
    return json.dumps(apn_properties, indent=2)


def get_db():
    #client = MongoClient(host='test_mongodb', port=27017)
    client = MongoClient('mongodb://localhost:27017/')
    db = client['apn_db']
    collection = db['apn_collection']
    return collection


def upload_to_mongodb(data):
    try:
        # Connect to MongoDB
        collection = get_db()

        # Print length of data
        print('length of data:', len(data))

        # Drop the existing collection
        collection.drop()

        # Insert the data into MongoDB
        collection.insert_many(data)

        print("successfully Data uploaded to MongoDB.")
    except Exception as e:
        print("Error uploading data to MongoDB:", e)

@app.route('/api/apn', methods=['GET'])
def get_all_apn_data():
    try:
        collection = get_db()
        apn_data = list(collection.find({}, {'_id': False}))
        return jsonify({'status': 'success', 'data': apn_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/apn/<apn_name>', methods=['GET'])
def get_apn_data(apn_name):
    try:
        collection = get_db()
        apn_data = list(collection.find({"apn": apn_name}, {'_id': False}))
        if not apn_data:
            return jsonify({'status': 'error', 'message': 'APN not found'}), 404
        else:
            return jsonify({'status': 'success', 'data': apn_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


def main():
    with open('dataset', 'r') as file:
        input_text = file.read()

    apn_properties = extract_apn_properties(input_text)
    json_output = convert_to_json(apn_properties)
    #Upload data to MongoDB
    upload_to_mongodb(json.loads(json_output))
    # print("Data uploaded to MongoDB.")


if __name__ == "__main__":
    main()
    app.run(host='0.0.0.0', port=5000, debug=True)
