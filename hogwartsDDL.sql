DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
first VARCHAR NOT NULL,
last VARCHAR NOT NULL,
id INT NOT NULL,
PRIMARY KEY (id)
);

CREATE TABLE courses (
coursenum VARCHAR NOT NULL,
title VARCHAR NOT NULL,
PRIMARY KEY (coursenum)
);

CREATE TABLE enrollments (
id INT NOT NULL,
coursenum VARCHAR NOT NULL,
term VARCHAR NOT NULL,
year INT NOT NULL,
PRIMARY KEY (id, coursenum, term, year),
FOREIGN KEY (id) REFERENCES students(id),
FOREIGN KEY (coursenum) REFERENCES courses(coursenum)
);

insert into students values ('Harry', 'Potter', 1);
insert into students values ('Hermione', 'Granger', 2);
insert into students values ('Ron', 'Weasley', 3);

insert into courses values ('P140', 'Intro to Potions');
insert into courses values ('DA101', 'Intro to Dark Arts');
insert into courses values ('HB100', 'Intro to Herbology');

insert into enrollments values (1, 'DA101', 'Fall', 2010);
insert into enrollments values (1, 'P140', 'Fall', 2010);
insert into enrollments values (2, 'P140', 'Fall', 2011);
insert into enrollments values (3, 'P140', 'Fall', 2011);
insert into enrollments values (3, 'P140', 'Fall', 2012);