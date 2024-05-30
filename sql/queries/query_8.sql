-- query_8.sql
SELECT AVG(grades.grade) as average_grade
FROM grades
JOIN subjects ON grades.subject_id = subjects.subject_id
JOIN teachers ON subjects.teacher_id = teachers.teacher_id
WHERE teachers.name = 'Teacher Name'; -- Replace 'Teacher Name' with the actual name
