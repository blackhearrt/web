-- query_9.sql
SELECT subjects.name
FROM subjects
JOIN grades ON subjects.subject_id = grades.subject_id
JOIN students ON grades.student_id = students.student_id
WHERE students.name = 'Student Name'; -- Replace 'Student Name' with the actual name
