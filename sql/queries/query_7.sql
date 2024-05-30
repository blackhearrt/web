-- query_7.sql
SELECT students.name, grades.grade
FROM students
JOIN grades ON students.student_id = grades.student_id
JOIN groups ON students.group_id = groups.group_id
WHERE groups.name = 'Group A' -- Replace 'Group A' with the actual group name
AND grades.subject_id = 1; -- Replace 1 with the subject ID
