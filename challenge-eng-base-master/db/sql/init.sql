USE challenge;

CREATE TABLE links(movieId INT, imdbId INT, tmdbId INT);
CREATE TABLE tags(userId INT, movieId INT, tag VARCHAR(200), timestamp INT);
CREATE TABLE ratings(userId INT, movieId INT, rating INT, timestamp INT);
CREATE TABLE movies(movieId INT, title VARCHAR(200), genres VARCHAR(200));
