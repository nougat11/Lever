"""This module contains classes for data output."""
from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom


class Writer(ABC):
    """Abstract class for output classes."""
    @abstractmethod
    def write(self, hostel):
        """This method output information"""


class JsonWriter(Writer):
    """This class outputs result in json format"""
    def write(self, hostel):
        with open('result.json', 'w') as file:
            json.dump(hostel, file, indent=4)


class XmlWriter(Writer):
    """This class outputs result in xml format"""
    def write(self, hostel):
        with open('result.xml', 'w') as file:
            root = ET.Element('result')
            for room in hostel:
                room_xml = ET.SubElement(root, 'room')
                room_name = ET.SubElement(room_xml, 'name')
                room_name.text = room['room']
                students = ET.SubElement(room_xml, 'students')
                for student in room['students']:
                    student_xml = ET.SubElement(students, 'student')
                    student_name = ET.SubElement(student_xml, 'student_name')
                    student_name.text = student
            data = ET.tostring(root, method='xml').decode()
            dom = xml.dom.minidom.parseString(data)
            file.write(dom.toprettyxml())
