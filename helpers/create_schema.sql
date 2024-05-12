CREATE DATABASE IF NOT EXISTS your_database_name;

\c your_database_name;

CREATE TABLE IF NOT EXISTS Grammars (
    id SERIAL PRIMARY KEY,
    Grammar TEXT NOT NULL,
    class TEXT,
    kind TEXT,
    examples TEXT
);

CREATE TABLE IF NOT EXISTS Graphs (
    id SERIAL PRIMARY KEY,
    graph TEXT NOT NULL,
    num_nodes INT,
    num_edges INT,
    download_link TEXT
);

CREATE TABLE IF NOT EXISTS graph_grammars (
    id SERIAL PRIMARY KEY,
    graph_id INT NOT NULL,
    grammar_id INT NOT NULL,
    FOREIGN KEY (graph_id) REFERENCES Graphs(id),
    FOREIGN KEY (grammar_id) REFERENCES Grammars(id)
);
