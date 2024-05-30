-- query_5.sql
SELECT subjects.name
FROM subjects
JOIN teachers ON subjects.teacher_id = teachers.teacher_id
WHERE teachers.name = 'Teacher Name'; -- Replace 'Teacher Name' with the actual name
