"""This script combines a list of rooms and students into a list of rooms with students."""
import argparse
from json_loader import JsonLoader
from file_writers import JsonWriter, XmlWriter
from base import BaseWorker
import queries
import mysql.connector
def parse_args():
    """This method parse args from console"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rooms", help="Path for rooms json file")
    parser.add_argument("-s", "--students", help="Path for students json file")
    parser.add_argument(
        "-f", "--format", choices=["json", "xml"], help="Format output file"
    )
    parser.add_argument("-H", "--host", help="Server IP")
    parser.add_argument("-u", "--user", help="Username")
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-b", "--base", help="Base name")
    return parser.parse_args()


format_classes = {"json": JsonWriter(), "xml": XmlWriter()}


if __name__ == "__main__":
    args = parse_args()
    db = BaseWorker(args.host, args.user, args.password, args.base)
    db.create_tables()
    list_of_rooms = JsonLoader(args.rooms).load_json()
    rooms = [tuple(room.values()) for room in list_of_rooms]
    list_of_students = JsonLoader(args.students).load_json()
    students = [tuple(student.values()) for student in list_of_students]
    db.insert_tables(rooms, students)

    hostel = {
        room["id"]: {"room": room["name"], "students": []} for room in list_of_rooms
    }
    for student in list_of_students:
        hostel[student["room"]]["students"].append(student["name"])
    id, hostel = zip(*hostel.items())
    file_writer = format_classes[args.format]
    db.create_indexes()
    count_students_in_the_room = db.query_exectutor(queries.count_students_in_the_room, True)

    file_writer.write(count_students_in_the_room, "count_students_in_the_room")
    top_five_rooms_min_avg_age = db.query_exectutor(queries.top_five_rooms_min_avg_age, False)
    file_writer.write(top_five_rooms_min_avg_age, "top_five_rooms_min_avg_age")
    top_five_rooms_max_avg_diff = db.query_exectutor(queries.top_five_rooms_max_avg_diff, True)
    file_writer.write(top_five_rooms_max_avg_diff, "top_five_rooms_max_avg_diff")
    bisex_rooms = db.query_exectutor(queries.bisex_rooms, False)
    file_writer.write(bisex_rooms, "bisex_rooms")

