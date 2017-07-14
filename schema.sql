CREATE TABLE IF NOT EXISTS users (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar,
	password varchar,
	grade integer
);

CREATE TABLE IF NOT EXISTS files (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar,
	user integer,
	created_at integer,
	uniqid varchar,
	source varchar
);
