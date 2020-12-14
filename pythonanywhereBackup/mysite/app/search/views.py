from flask import render_template, abort, request

from . import search



@search.route('/searchTree')
def searchTree():
    return render_template("/search/searchTree.html")

@search.route('/searchStreet')
def searchStreet():
    return render_template("/search/searchStreet.html")
