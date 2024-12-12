SELECT genre, COUNT(*) AS movies_count
FROM movies
GROUP BY genre;
