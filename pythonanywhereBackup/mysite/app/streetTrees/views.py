from flask import render_template, abort, request

from . import streetTrees


@streetTrees.route('/streetTrees')

def streetTrees():
    return render_template('streetTrees/why-street-trees.html')