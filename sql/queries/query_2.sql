-- query_2.sql
SELECT students.name, AVG(grades.grade) as average_grade
FROM students
JOIN grades ON students.student_id = grades.student_id
WHERE grades.subject_id = 1 -- Replace 1 with the subject ID
GROUP BY students.student_id
ORDER BY average_grade DESC
LIMIT 1;
