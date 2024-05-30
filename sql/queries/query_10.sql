-- query_10.sql
SELECT subjects.name
FROM subjects
JOIN grades ON subjects.subject_id = grades.subject_id
JOIN students ON grades.student_id = students.student_id
JOIN teachers ON subjects.teacher_id = teachers.teacher_id
WHERE students.name = 'Student Name' -- Replace 'Student Name' with the actual name
AND teachers.name = 'Teacher Name'; -- Replace 'Teacher Name' with the actual name
