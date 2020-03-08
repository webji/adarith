-- SQLite
SELECT id, name, fullname, password, born_date
FROM `t_users`;

SELECT * FROM `t_users` WHERE id = 2;

DELETE FROM `t_users` WHERE id = 2;

SELECT * FROM `t_questions` ORDER BY title LIMIT 20;

SELECT * FROM `t_settings` WHERE key = 'initialized';

UPDATE `t_settings` SET value = 'True' WHERE key = 'initialized';
