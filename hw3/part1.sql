-- Part 1 HW 3

-- Ed: There is a syntax error below. I fixed by adding another dash.
-- In fact the whole file is loaded with syntax errors on bad
-- comment delimiters.

-- 3.11
-- Part a
-- selecting student id number and name of students that take at least 1 computer science course

SELECT 
     distinct student.name, student.id 
FROM 
     takes, student, course 
WHERE 
     student.id = takes.id 
AND 
     takes.course_id = course.course_id 
AND 
     course.dept_name = 'Comp. Sci.';


-- Part b
— selecting student id and name of student that did not take course offered before 2005

SELECT 
     distinct student.id, student.name
FROM
     student 
WHERE 
     student.id not in (SELECT 
                             id 
                         FROM 
                             takes 
                         WHERE 
                             year<2005);

-- Part c
—- selecting max salary of instructors in each department

SELECT 
     dept_name, max(salary) 
FROM 
     instructor 
group 
     by dept_name

-- Part d
— selecting lowest per department salary among the max salaries

SELECT 
     min(max_salary)
FROM 
    (SELECT 
           dept_name, max(salary) AS max_salary 
     FROM 
          instructor 
     group by dept_name) 
AS 
     max_table;

-- 3.12
-- Part a
— The error given was as below 
— 0 credit courses cannot be created as there exists a constraint 
-- ERROR:  new row for relation "course" violates check constraint “course_credits_check"

— Altering table to remove constraint
ALTER TABLE 
    course 
DROP 
    constraint course_credits_check;

— inserting 0 credit course 
INSERT INTO 
     course
VALUES
     ('CS-001','Weekly Seminar','Comp. Sci.',0);

-- Part b
— creating section of course in fall 2017 with section 1 and no specified location

INSERT INTO 
     section
VALUES
     ('CS-001',1,'Fall',2017, null, null);

-- Part c
— enrolling every student in comp sci department in above section 
INSERT INTO 
     takes(ID, course_id, sec_id, semester, year)
SELECT 
     ID, 'CS-001', '1', 'Fall', 2017
WHERE 
    dept_name = 'Comp. Sci.';

-- Part d
--creating student with id 12345

INSERT INTO 
     student
VALUES
     ('12345','QWERTY',null, null);

-- creating student who takes this course 
INSERT INTO 
     takes
VALUES
     ('12345', 'CS-001', '1', 'Fall'', 2017);

-- deleting said student 
DELETE FROM takes WHERE course_id = 'CS-001
AND sec_id = '1'
AND semester = 'Fall'
AND year = 2017
AND ID = '12345'

-- Part e
-- delete course cs001
-- if deleted before deleting sections error will pop up stating that section exits so course cannot be deleted 
DELETE FROM 
    course
WHERE 
    course_id = 'CS-001';

-- Part f
-- deleting all courses from takes where course title contains advanced

DELETE FROM 
    takes 
WHERE 
    course_id in (SELECT 
                      course_id 
                  FROM 
                      course  
                  WHERE 
                      lower(title) like '%advanced%');

— 3.24
-- name and id of accounting students advised by an instructor in physics department 

SELECT 
  student.ID, student.name
FROM 
  instructor, student, advisor
WHERE 
  advisor.s_ID = student.ID 
AND
  advisor.i_ID = instructor.ID 
AND 
  student.dept_name = 'Accounting' 
AND 
  instructor.dept_name = 'Physics';

— 3.25
-- name of departments whose budget is higher than that of philosophy listed in alphabetical order

SELECT 
   dept_name
FROM 
   department 
WHERE 
   budget > (SELECT 
                   budget 
                FROM 
                   department 
                WHERE 
                   dept_name = 'Philosophy');
— 3.26
-- course id and ID of every student that has retaken course twice 

SELECT 
    distinct course_id, ID
FROM 
    (SELECT 
         ID, course_id, COUNT(*) AS number 
      FROM 
         takes 
      GROUP BY 
         ID, course_id) AS t  
      WHERE 
        t.number > 2 
ORDER BY 
     course_id;

— 3.27 
-- student id of those that have retaken 3 separate courses 

SELECT 
   ID 
FROM 
   student 
WHERE 
  ID = (SELECT 
           distinct ID 
        FROM 
           takes 
        GROUP BY 
           ID, course_id 
        HAVING 
           count(*)>3);








