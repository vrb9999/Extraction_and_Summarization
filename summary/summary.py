from flask import Blueprint, render_template
from flask import Flask, request, jsonify, render_template
from textsummarizer import *
from summary.textsummarizer import generate_summary

app = Flask(__name__)

second = Blueprint("second", __name__, template_folder="templates")


@second.route("/home")
@second.route("/")
def home():
    return render_template("base.html")


@second.route('/summarise', methods=['GET','POST'])
def summarize():
    if request.method == 'POST':

        text = request.form['originalText']
        if not request.form['numOfLines']:
            numOfLines = 3
        else:
            numOfLines = int(request.form['numOfLines'])

        summary, original_length = generate_summary(text, numOfLines)

        return render_template('home.html', text_summary=summary, lines_original=original_length, lines_summary=numOfLines)
