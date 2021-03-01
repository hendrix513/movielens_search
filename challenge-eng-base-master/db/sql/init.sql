USE challenge;

CREATE TABLE links(movieId INT, imdbId INT, tmdbId INT, PRIMARY KEY (movieId));
CREATE TABLE tags(userId INT, movieId INT, tag VARCHAR(200), timestamp INT);
CREATE TABLE ratings(userId INT, movieId INT, rating INT, timestamp INT);
CREATE TABLE movies(movieId INT, title VARCHAR(200), genres VARCHAR(200), PRIMARY KEY (movieId));

CREATE INDEX idx_1 on ratings (movieId);
CREATE INDEX idx_2 on tags (movieId);

CREATE INDEX idx_3 on ratings (userId);
CREATE INDEX idx_4 on tags (userId);

