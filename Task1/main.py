"""This script combines a list of rooms and students into a list of rooms with students."""
import argparse
from json_loader import JsonLoader
from file_writers import JsonWriter, XmlWriter


def parse_args():
    """This method parse args from console"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rooms', help="Path for rooms json file")
    parser.add_argument('-s', '--students', help="Path for students json file")
    parser.add_argument('-f', '--format', choices=['json', 'xml'], help="Format output file")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    list_of_rooms = JsonLoader(args.rooms).load_json()
    list_of_students = JsonLoader(args.students).load_json()
    hostel = {room['id']: {'room': room['name'], 'students': []} for room in list_of_rooms}
    for student in list_of_students:
        hostel[student['room']]['students'].append(student['name'])
    hostel = [item[1] for item in hostel.items()]
    if args.format == 'json':
        JsonWriter().write(hostel)
    if args.format == 'xml':
        XmlWriter().write(hostel)
