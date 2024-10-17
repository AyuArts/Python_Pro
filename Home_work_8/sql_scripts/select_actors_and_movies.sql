SELECT actors.name, GROUP_CONCAT(movies.title, ', ') AS movies
FROM actors
JOIN movie_cast ON actors.id = movie_cast.actor_id
JOIN movies ON movies.id = movie_cast.movie_id
GROUP BY actors.name;