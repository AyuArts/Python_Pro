SELECT AVG(actors.birth_year) AS avg_birth_year
FROM actors
INNER JOIN movie_cast ON actors.id = movie_cast.actor_id
INNER JOIN movies ON movies.id = movie_cast.movie_id
WHERE movies.genre = ?;
