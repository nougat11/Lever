"""This module contains classes for data output."""
from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom


class Writer(ABC):
    """Abstract class for output classes."""

    @abstractmethod
    def write(self, data, query):
        """This method output information"""


class JsonWriter(Writer):
    """This class outputs result in json format"""
    def write(self, data, query):
        with open(f'{query}.json', 'w') as file:
            json.dump(data, file, indent=4)


class XmlWriter(Writer):
    """This class outputs result in xml format"""
    def write(self, data, query):
        with open(f'{query}.xml', 'w') as file:
            root = ET.Element('root')
            for room in data:
                room_xml = ET.SubElement(root, 'room')
                room_name = ET.SubElement(room_xml, 'name')
                room_name.text = room['room']
                if len(room) > 1:
                    room_value = ET.SubElement(room_xml, 'value')
                    room_value.text = str(room['value'])
            data = ET.tostring(root).decode()
            dom = xml.dom.minidom.parseString(data)
            file.write(dom.toprettyxml())
