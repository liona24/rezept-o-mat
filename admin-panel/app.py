from flask import Flask, request, jsonify, abort, render_template, redirect, url_for, g, session
from flask_cors import CORS
from bs4 import BeautifulSoup
from werkzeug.security import check_password_hash, generate_password_hash

from functools import wraps
from urllib.parse import urlparse
from urllib.request import urlopen
import re
import secrets

import db

app = Flask(__name__)
# this is fine for our use case
app.secret_key = secrets.token_bytes(16)
cors = CORS(app, resources={
    '/recipes': { 'origins': 'https://liona24.github.io/rezept-o-mat' }
})
db.init_app(app)

KNOWN_DOMAINS = {
    'chefkoch.de',
    'www.chefkoch.de'
}

# demo password: bzqG{ ]K"4ot
PASSWORD = 'pbkdf2:sha256:150000$tpl8rGtS$16ccd4e50cf15bdbb2b96d2e8da3863e09e66119ecd684d2f5f24e57205e7ea7'

TRIM_WHITESPACE_PATTERN = re.compile(r'\s\s+')


def requires_auth(view):
    @wraps(view)
    def wrapper(*args, **kvargs):
        if session.get("is_authorized") is not True:
            return redirect(url_for('index'))

        return view(*args, **kvargs)
    return wrapper


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    # POST
    password = request.form.get('password', None)
    if password is None:
        abort(400)

    print(generate_password_hash(password))

    session.clear()
    if check_password_hash(PASSWORD, password):
        session["is_authorized"] = True
        return redirect(url_for('parse_recipe'))
    else:
        return redirect(url_for('index'))


@app.route('/parse_recipe', methods=['GET', 'POST'])
@requires_auth
def parse_recipe():
    if request.method == 'GET':
        return render_template('parse_recipe.html')

    # POST
    url = request.form.get('url', None)
    if url is None:
        abort(400)

    domain = urlparse(url).netloc
    if domain not in KNOWN_DOMAINS:
        abort(400)

    resp = urlopen(url)
    content = resp.read()
    soup = BeautifulSoup(content, 'html.parser')

    title = soup.select('.ds-mb-col > div:nth-child(2) > h1:nth-child(1)')[0].get_text().strip()

    description = soup.select('article.ds-box:nth-child(8) > div:nth-child(3)')[0]
    description = description.get_text().strip().replace('\r', '').split('\n')
    description = list(filter(None, map(lambda s: s.strip(), description)))

    ingredients_table = soup.select('.ingredients')[0]
    ingredients = []
    for row in ingredients_table.find_all('tr'):
        amount = row.select('.td-left')[0].get_text().strip()
        ingredient = row.select('.td-right')[0].get_text().strip()

        amount = TRIM_WHITESPACE_PATTERN.sub(' ', amount).strip()
        ingredient = TRIM_WHITESPACE_PATTERN.sub(' ', ingredient).strip()

        ingredients.append([ingredient, amount])

    db.add_recipe(title, url, description, ingredients)

    return jsonify(description=description, id=10, source=url, ingredients=ingredients, title=title)


@app.route('/recipe', methods=['GET'])
def recipes():
    recipe = db.get_random_recipe()
    if recipe is None:
        abort(404)

    return jsonify(**recipe)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
