from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def show_index():
    return render_template('index.html')