-- GPA of Knutson
SELECT ROUND(SUM(
    CASE
       WHEN grade = 'A+' THEN 4.00
       WHEN grade = 'A' THEN 3.75
       WHEN grade = 'A-' THEN 3.50
       WHEN grade = 'B+' THEN 3.25
       WHEN grade = 'B' THEN 3.00
       WHEN grade = 'B-' THEN 2.75
       WHEN grade = 'C+' THEN 2.50
       WHEN grade = 'C' THEN 2.25
       WHEN grade = 'C-' THEN 2.00
       WHEN grade = 'D+' THEN 1.75
       WHEN grade = 'D' THEN 1.50
       WHEN grade = 'D-' THEN 1.25
       WHEN grade = 'E' THEN 1.00
       WHEN grade = 'F' THEN 0.00
       END)/count(*),3) AS GPA
FROM
    takes,student
WHERE
    student.id = takes.id
    AND student.name = 'Knutson';

-- GPA of all students
SELECT student.name AS student_name,
       student.id AS student_id,
       student.dept_name AS major,
       ROUND(SUM(
           CASE
               WHEN takes.grade = 'A+' THEN 4.00
               WHEN takes.grade = 'A' THEN 3.75
               WHEN takes.grade = 'A-' THEN 3.50
               WHEN takes.grade = 'B+' THEN 3.25
               WHEN takes.grade = 'B' THEN 3.00
               WHEN takes.grade = 'B-' THEN 2.75
               WHEN takes.grade = 'C+' THEN 2.50
               WHEN takes.grade = 'C' THEN 2.25
               WHEN takes.grade = 'C-' THEN 2.00
               WHEN takes.grade = 'D+' THEN 1.75
               WHEN takes.grade = 'D' THEN 1.50
               WHEN takes.grade = 'D-' THEN 1.25
               WHEN takes.grade = 'E' THEN 1.00
               WHEN takes.grade = 'F' THEN 0.00
           END) / COUNT(*), 3) AS GPA
FROM student, takes, course
WHERE student.id = takes.id
      AND takes.course_id = course.course_id
GROUP BY student.name, student.id;






