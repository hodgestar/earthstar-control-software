# -*- coding: utf-8 -*-

""" Effect event API blueprint. """

import json

from flask import Blueprint, current_app, jsonify, request, url_for


effect_api_bp = Blueprint('effect_api', __name__, template_folder='templates')


@effect_api_bp.route('/effect')
def index():
    return jsonify({
        "transition-timer": url_for(".transition_timer"),
        "spindots": url_for(".spindots"),
    })


@effect_api_bp.route('/effect/transition-timer', methods=["POST"])
def transition_timer():
    data = request.get_json()
    effect = {
        'type': 'transition-timer',
        'seconds': data["seconds"],
    }
    current_app.effect_socket.send(json.dumps(effect))
    return jsonify(effect)


@effect_api_bp.route('/effect/spindots', methods=["POST"])
def spindots():
    data = request.get_json()
    effect = {
        'type': 'spindots',
        'ring': data["ring"],
        'angle': data["angle"],
    }
    current_app.effect_socket.send(json.dumps(effect))
    return jsonify(effect)
