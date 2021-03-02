This application allows a user to query against a database of movies. The database
is populated by a cli command, shown below, which pulls the latest available dataset from
movielens.org and inserts the contents into the database

Code changes should trigger live reload of the docker services in the docker
containers by way of the volume binds specified in the compose file.

To run application:
 - docker-compose up backend site

To load data into backend:
 - docker-compose exec backend flask load-movielens
 
To run regression tests:
 - docker-compose exec backend pytest -x -s
 
To use front-end, go to to http://localhost:8090 and enter data in available fields, then hit
'submit query' button - results will display on page. Each query will return an array of results, with
each element containing a movie's title, average rating, genre list, imdb and tmdb link for a all movies
matching search. Note that all queries must have a value for 'page' and 'limit'. page=1 gets first page of
results, page=2 the second, etc.

With more time I would like to:
- update front-end to include a more extensive 'query builder' to expand the set of possible queries
- add more regression tests
- update handling of movie genres- for a given movie, its list of genres is stored as a pipe-separated list.
  in the 'movies' table. It would be better if there was a separate table for genres to capture the relationship between moveis
  and genres
- update backend code to be able to support different options for returning data- for example
  to return, for a given movie, the N most recent ratings, etc.

