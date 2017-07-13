CREATE TABLE users (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar,
	password varchar,
	grade integer
);

CREATE TABLE files (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar,
	user integer,
	created_at integer,
	uniqid varchar,
	source varchar
);
