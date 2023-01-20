import json
import os
import awsgi
# from  boto3 import resource
import boto3
from flask_cors import CORS
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest
app = Flask(__name__)
CORS(app)
dynamodb = boto3.resource('dynamodb')


BASE_ROUTE ='/stock'

@app.route(BASE_ROUTE +'/<ticker>', methods=['POST'])
def write_stock_info(ticker):
    try:
        data = request.get_json()
    except BadRequest as e:
        data = request.args.to_dict()
    table = dynamodb.Table('StockPrice'+ticker+'-dev')
    table.put_item(Item=data)
    return jsonify(message=data)

@app.route(BASE_ROUTE +'/<ticker>', method=['GET'])
def get_stock():
    return jsonify(message="item found")

def handler(event, context):
  print('received event:')
  print(event)
#   return app(event,context)
  return awsgi.response(app,event,context)
#   return {
#       'statusCode': 200,
#       'headers': {
#           'Access-Control-Allow-Headers': '*',
#           'Access-Control-Allow-Origin': '*',
#           'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
#       },
#       'body': json.dumps('Hello from your new Amplify Python lambda!')
#   }