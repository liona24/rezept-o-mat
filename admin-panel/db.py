import sqlite3
from flask import g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("recipes.db", detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    
    if db is not None:
        db.close()


def add_recipe(title, source, description, ingredients):
    db = get_db()

    db.commit()

    #try:

    recipe_id = db.execute(
        "INSERT INTO recipes (title, source) VALUES (?, ?)", 
        (title, source)
    ).lastrowid

    for i, text in enumerate(description):
        db.execute(
            "INSERT INTO descriptions (recipe_id, idx, text) VALUES (?, ?, ?)",
            (recipe_id, i, text)
        )
    for i, ingredient in enumerate(ingredients):
        db.execute(
            "INSERT INTO ingredients (recipe_id, idx, name, amount) VALUES (?, ?, ?, ?)", 
            (recipe_id, i, ingredient[0], ingredient[1])
        )

    """
    except Exception as e:
        print(e)
        db.rollback()
    """

    db.commit()

def get_random_recipe():
    db = get_db()

    recipe = db.execute("SELECT * FROM recipes ORDER BY RANDOM() LIMIT 1").fetchone()
    if recipe is None:
        return None

    id, title, source = recipe

    description = []
    for row in db.execute("SELECT text FROM descriptions WHERE recipe_id = ? ORDER BY idx ASC", (id,)):
        description.append(row[0])

    ingredients = []
    for row in db.execute("SELECT name, amount FROM ingredients WHERE recipe_id = ? ORDER BY idx ASC", (id,)):
        ingredients.append(list(row))

    return {
        "title": title,
        "source": source,
        "id": id,
        "description": description,
        "ingredients": ingredients
    }


def init_app(app):
    app.teardown_appcontext(close_db)

