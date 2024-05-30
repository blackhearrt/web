-- query_3.sql
SELECT groups.name, AVG(grades.grade) as average_grade
FROM groups
JOIN students ON groups.group_id = students.group_id
JOIN grades ON students.student_id = grades.student_id
WHERE grades.subject_id = 1 -- Replace 1 with the subject ID
GROUP BY groups.group_id;
