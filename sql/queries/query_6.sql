-- query_6.sql
SELECT students.name
FROM students
JOIN groups ON students.group_id = groups.group_id
WHERE groups.name = 'Group A'; -- Replace 'Group A' with the actual group name
