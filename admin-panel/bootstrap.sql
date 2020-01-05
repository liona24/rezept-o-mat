DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS descriptions;
DROP TABLE IF EXISTS ingredients;

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    source TEXT UNIQUE NOT NULL
);

CREATE TABLE descriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    idx INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id)
);

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    idx INTEGER NOT NULL,
    name TEXT NOT NULL,
    amount TEXT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id)
);

