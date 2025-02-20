drop table if exists record_workouts;
drop table if exists template_workouts;
drop table if exists users;


CREATE TABLE users
(user_id int NOT NULL PRIMARY KEY,
first_name varchar(32), 
last_name varchar(32), 
type_training varchar(32) NOT NULL);

CREATE TABLE template_workouts
(tw_id serial PRIMARY KEY,
 user_id int,
 day_of_week varchar(32) NOT NULL,
 workout text NOT NULL, 
 approuch int NOT NULL, 
 level int NOT NULL,
 CONSTRAINT ct_user_id FOREIGN KEY (user_id) REFERENCES users(user_id));

 CREATE TABLE record_workouts
(rw_id serial PRIMARY KEY,
 user_id int,
 workout_date date NOT NULL,
 day_of_week varchar(32) NOT NULL,
 workout text NOT NULL,
 level int NOT NULL,
 weight int,
 number_approuch int NOT NULL,
 repetition int,
 approuch int NOT NULL,
 CONSTRAINT rw_user_id FOREIGN KEY (user_id) REFERENCES users(user_id));

-- select * from users;
-- select * from gym;
-- select * from template_workouts;