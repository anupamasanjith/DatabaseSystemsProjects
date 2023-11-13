-- Exam 1
-- Question 1
-- Write a query that generates a table of actors as and the movies they acted in.
-- row contains (actor name,movie title. release year,director, and character name
-- ordered by last name, release year.


-- Ed: Good, but use natural join or join syntax for clarity. -1
SELECT
    actors.firstname,actors.lastname,
    movies.title,movies.releaseyear,movies.director,
    actsin.charactername
FROM
    actors,movies,actsin
WHERE
    actors.actorid = actsin.actorid AND
    movies.movieid = actsin.movieid
ORDER BY
    actors.lastname,movies.releaseyear;


--Question 2
-- Query that displays names of the actors who have acted in most number of movies
-- output schema (lastname,actorid,count)

-- Ed: Nice. Same comment about join syntax for brevity and clarity. -1
SELECT
    lastname,actorid,count
FROM(SELECT
    lastname,actorid,count(*) as count
     FROM
         (SELECT
              actors.firstname,
              actors.lastname,
              movies.title,
              actors.actorid
         FROM
             actors,
             movies,
             actsin
         WHERE
             actors.actorid = actsin.actorid AND
             movies.movieid = actsin.movieid) AS t
     GROUP BY firstname,t.lastname, actorid) AS sub

WHERE
    count = (SELECT max(count)
             FROM
                 (SELECT
                     count(*) as count
                  FROM
                      (SELECT
                           actors.firstname,
                           actors.lastname,
                           movies.title,
                           actors.actorid
                       FROM
                           actors,
                           movies,
                           actsin
                       WHERE
                           actors.actorid = actsin.actorid AND
                           movies.movieid = actsin.movieid) AS t2
                  GROUP BY
                      lastname,actorid) as subtwo);




