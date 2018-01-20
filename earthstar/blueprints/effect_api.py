# -*- coding: utf-8 -*-

""" Effect event API blueprint. """

from flask import Blueprint, jsonify


effect_api_bp = Blueprint('effect_api', __name__, template_folder='templates')


@effect_api_bp.route('/effect')
def index():
    return jsonify({
        'effect-api': 'coming soon',
    })
