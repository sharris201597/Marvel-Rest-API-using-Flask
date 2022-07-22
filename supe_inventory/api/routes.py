from flask import Blueprint, request, jsonify
from supe_inventory.helpers import token_required
from supe_inventory.models import db, User, Supe, Supe_schema, Supes_schema

api = Blueprint('api',__name__,url_prefix= '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some':'value'}

#Create Endpoit
@api.route('/supes', methods = ['POST'])
@token_required
def create_supe(current_user_token):
    super_hero_name = request.json['super_hero_name']
    secret_identity = request.json['secret_identity']
    home_planet = request.json['home_planet']
    villian_or_hero = request.json['villian_or_hero']
    user_token = current_user_token.token

    print(f'Big Tester: {current_user_token.token}')

    supe = Supe(super_hero_name,secret_identity,home_planet,villian_or_hero,user_token = user_token)

    db.session.add(supe)
    db.session.commit()

    response = Supe_schema.dump(supe)
    
    return jsonify(response)

#Retrieve all Super Hero endpoints
@api.route('/supes', methods = ['GET'])
@token_required
def get_drones(current_user_token):
    owner = current_user_token.token
    supes = Supe.query.filter_by(user_token = owner).all()
    response = Supes_schema.dump(supes)
    return jsonify(response)

