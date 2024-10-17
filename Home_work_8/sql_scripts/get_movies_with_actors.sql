SELECT movies.title AS movie_title, GROUP_CONCAT(actors.name, ', ') AS actors
FROM movies
JOIN movie_cast ON movies.id = movie_cast.movie_id
JOIN actors ON actors.id = movie_cast.actor_id
GROUP BY movies.id;
