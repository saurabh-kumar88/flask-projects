from flask import render_template, abort, request

from . import aboutMap



@aboutMap.route('/aboutmap')
def aboutmap():
    return render_template("/about map/aboutMap.html")
