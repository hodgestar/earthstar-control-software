# -*- coding: utf-8 -*-

""" Controller (i.e. buttons) blueprint. """

from flask import Blueprint, render_template


controller_bp = Blueprint('controller', __name__, template_folder='templates')


@controller_bp.route('/controller')
def index():
    return render_template('controller.html')
