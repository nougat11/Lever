create_rooms = """
CREATE TABLE IF NOT EXISTS rooms(
    id INT NOT NULL,
    name CHAR(16) NULL,
    PRIMARY KEY(id)
)
"""
create_students="""
CREATE TABLE IF NOT EXISTS students (
  id INT NOT NULL,
  birthday DATETIME NULL,
  name CHAR(100) NULL,
  room INT NULL,
  sex CHAR(1) NULL,
  PRIMARY KEY (id),
  CONSTRAINT room
    FOREIGN KEY (room)
    REFERENCES rooms (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
    )
"""
clear_rooms="""
DELETE FROM rooms
"""
clear_students="""
DELETE FROM students
"""
insert_students="""
INSERT INTO students(birthday, id, name, room, sex)
VALUES (%s, %s, %s, %s, %s)
"""
insert_rooms="""
INSERT INTO rooms (id, name) VALUES (%s, %s)
"""
count_students_in_the_room="""
select rooms.name as room, count(*) as students
from rooms
inner join students on students.room = rooms.id
group by rooms.name
"""
top_five_rooms_min_avg_age="""
select rooms.name as room
from rooms
inner join students on students.room = rooms.id
group by rooms.id
order by avg(datediff(students.birthday, now())) desc
limit 5;
"""
top_five_rooms_max_avg_diff="""
select rooms.name as room, datediff(max(students.birthday), min(students.birthday)) as date_diff
from rooms
inner join students on rooms.id = students.room
group by rooms.id
order by datediff(max(students.birthday), min(students.birthday)) desc
limit 5
"""
bisex_rooms="""
select rooms.name as room
from rooms
inner join students on rooms.id = students.room 
group by rooms.id
having count(distinct students.sex)=2;
"""
