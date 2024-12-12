SELECT id, title, release_year, genre
FROM movies
ORDER BY id
LIMIT ? OFFSET ?;
