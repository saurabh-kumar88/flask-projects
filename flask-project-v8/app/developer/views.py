from flask import render_template, abort, request

from . import developer

@developer.route('/developer')

def developer():
    return render_template('developer/developer.html')