from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
)

from page_analyzer.modules.url_manager import normalize_url, validate, check_url
from page_analyzer.modules.models import Url
from page_analyzer.modules import db
from page_analyzer.modules.config import SECRET_KEY


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def show_home_page():
    """
    Отображает главную страницу.

    :return:
    HTML-шаблон главной страницы.
    """
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    """
    Получает URL из формы, выполняет валидацию и сохраняет его в базе данных.

    :return:
    Перенаправление на страницу URL
    или рендеринг главной страницы с сообщением об ошибке.
    """
    new_url = request.form.get('url')
    errors = validate(new_url)
    if errors:
        flash(errors['message'], 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            messages=messages,
            url=new_url
        ), 422
    normalized_url = normalize_url(new_url)
    id_ = db.get_id(normalized_url)
    url = Url(name=normalized_url, id=id_)
    if url.id:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', id=url.id))
    db.save_url(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=url.id))


@app.route('/urls/<id>', methods=['GET'])
def show_url(id):
    """
    Отображает страницу конкретного URL.

    :return:
    HTML-шаблон страницы с информацией о конкретном URL.
    """
    messages = get_flashed_messages(with_categories=True)
    url = db.get_url(id)
    urls_checked = db.get_checked_urls(url)
    return render_template(
        'showURL.html',
        messages=messages,
        url=url,
        urls_checked=urls_checked
    )


@app.route('/urls', methods=['GET'])
def show_all_urls():
    """
    Отображает страницу со всеми сохраненными URL.

    :return:
    HTML-шаблон страницы со списком всех URL.
    """
    urls = db.get_all_urls()
    return render_template(
        'showURLS.html',
        urls=urls
    )


@app.route('/urls/<id>/checks', methods=['POST'])
def check_and_add_url(id):
    """
    Проверяет указанный URL и добавляет его в базу данных проверенных URL.

    :return:
    Перенаправление на страницу конкретного URL после проверки.
    """
    url = db.get_url(id)
    url_checked = check_url(url)
    if not url_checked or url_checked.status_code != 200:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        flash('Страница успешно проверена', 'success')
        db.add_checked_url(url, url_checked)
    return redirect(url_for('show_url', id=id))
