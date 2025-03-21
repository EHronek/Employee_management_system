#!/usr/bin/python3
from flask import request, jsonify
from models import storage
from api.v1.views import app_views
from models.company_asset import CompanyAssets


@app_views.route('/company_assets', methods=['GET'])
def get_assets():
    """Retrieve all company assets"""
    assets = [asset.to_dict() for asset in storage.all(CompanyAssets).values()]
    return jsonify(assets)


@app_views.route('/company_assets/<asset_id>', methods=['GET'])
def get_asset(asset_id):
    """Retrieve a specific company asset by ID"""
    asset = storage.get(CompanyAssets, asset_id)
    if not asset:
        return jsonify({'error': 'Asset not found'}), 404
    return jsonify(asset.to_dict())


@app_views.route('/company_assets', methods=['POST'])
def create_asset():
    """Create a new company asset"""
    data = request.get_json()
    if not data or 'employee_id' not in data or 'asset_name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    new_asset = CompanyAssets(**data)
    new_asset.save()
    return jsonify(new_asset.to_dict()), 201


@app_views.route('/company_assets/<asset_id>', methods=['PUT'])
def update_asset(asset_id):
    """Update an existing company asset"""
    asset = storage.get(CompanyAssets, asset_id)
    if not asset:
        return jsonify({'error': 'Asset not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        if hasattr(asset, key):
            setattr(asset, key, value)
    asset.save()
    return jsonify(asset.to_dict())


@app_views.route('/company_assets/<asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    """Delete a company asset"""
    asset = storage.get(CompanyAssets, asset_id)
    if not asset:
        return jsonify({'error': 'Asset not found'}), 404
    asset.delete()
    storage.save()
    return jsonify({'message': 'Asset deleted'})
