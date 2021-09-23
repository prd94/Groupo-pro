from flask import Blueprint, render_template
# import json

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/efficient-guide')
def efficient_guide():
    return render_template("efficient_guide.html")