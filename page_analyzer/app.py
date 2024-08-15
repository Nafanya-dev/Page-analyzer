from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
)

from page_analyzer.moduls.url_manager import normalize_url, validate, check_url
from page_analyzer.moduls.models import Url
from page_analyzer.moduls import db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def show_home_page():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    new_url = request.form.get('url')
    errors = validate(new_url)
    if errors:
        flash(errors['message'], 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            messages=messages,
            url=new_url
        )
    normalized_url = normalize_url(new_url)
    id_ = db.get_id(normalized_url, DATABASE_URL)
    url = Url(name=normalized_url, id=id_)
    if url.id:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', id=url.id))
    db.save_url(url, DATABASE_URL)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=url.id))


@app.route('/urls/<id>', methods=['GET'])
def show_url(id):
    messages = get_flashed_messages(with_categories=True)
    url = db.get_url(id, DATABASE_URL)
    urls_checked = db.get_checked_urls(url, DATABASE_URL)
    return render_template(
        'showURL.html',
        messages=messages,
        url=url,
        urls_checked=urls_checked
    )


@app.route('/urls', methods=['GET'])
def show_all_urls():
    urls = db.get_all_urls(DATABASE_URL)
    return render_template(
        'showURLS.html',
        urls=urls
    )


@app.route('/urls/<id>/checks', methods=['POST'])
def check_and_add_url(id):
    url = db.get_url(id, DATABASE_URL)
    url_checked = check_url(url)
    if not url_checked or url_checked.status_code != 200:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        flash('Страница успешно проверена', 'success')
        db.add_checked_url(url, url_checked, DATABASE_URL)
    return redirect(url_for('show_url', id=id))
