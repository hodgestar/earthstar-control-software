# -*- coding: utf-8 -*-

""" Root blueprint. """

from flask import Blueprint, render_template


root_bp = Blueprint('root', __name__, template_folder='templates')


@root_bp.route('/')
def index():
    return render_template('root.html')
