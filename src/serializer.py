#!/usr/bin/python

# Reversi is a multiplayer reversi game with dedicated server
# Copyright (C) 2012-2013, Juan Antonio Aldea Armenteros
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf8 -*-

import struct


class Serializer:
    @staticmethod
    def serialize_int(integer):
        return bytearray(struct.pack("!i", integer))

    @staticmethod
    def unserialize_int(byte_array):
        return struct.unpack("!i", str(byte_array))[0]

    @staticmethod
    def serialize_float(f):
        return bytearray(struct.pack("!d", f))

    @staticmethod
    def unserialize_float(byte_array):
        return struct.unpack("!d", str(byte_array))[0]

    @staticmethod
    def serialize_bool(b):
        return bytearray([1 if b else 0])

    @staticmethod
    def unserialize_bool(byte_array):
        return byte_array[0] != 0

    @staticmethod
    def serialize_string(string):
        return bytearray(string)

    @staticmethod
    def unserialize_string(byte_array):
        return str(byte_array)

    @staticmethod
    def serialize_list(l):
        byte_array = bytearray()
        for i in l:
            object_array = Serializer.serialize(i)
            byte_array.extend(Serializer.serialize_int(len(object_array)))
            byte_array.extend(object_array)
        return byte_array

    @staticmethod
    def unserialize_list(byte_array, classtype):
        l = list()
        size = len(byte_array)
        count = 0
        while count < size:
            obj_size = Serializer.unserialize_int(byte_array[count:count + 4])
            count += 4
            obj = Serializer.unserialize(byte_array[count:count + obj_size], classtype)
            count += obj_size
            l.append(obj)
        return l

    @staticmethod
    def serialize(obj):
        byte_array = bytearray()
        for attr, value in sorted(obj.__dict__.iteritems(), key=lambda (k, v): (k, v)):
            field_array = None
            if type(value) == int:
                field_array = Serializer.serialize_int(value)
            elif type(value) == str:
                field_array = Serializer.serialize_string(value)
                byte_array.extend(Serializer.serialize_int(len(field_array)))
            elif type(value) == float:
                field_array = Serializer.serialize_float(value)
            elif type(value) == bool:
                field_array = Serializer.serialize_bool(value)
            if field_array is not None:
                byte_array.extend(field_array)
        return byte_array

    @staticmethod
    def unserialize(byte_array, classtype):
        obj = classtype()
        count = 0
        for attr, value in sorted(obj.__dict__.iteritems(), key=lambda (k, v): (k, v)):
            field_value = None
            if type(value) == int:
                field_value = Serializer.unserialize_int(byte_array[count:count + 4])
                count += 4
            elif type(value) == str:
                size = Serializer.unserialize_int(byte_array[count:count + 4])
                count += 4
                field_value = Serializer.unserialize_string(byte_array[count:count + size])
                count += size
            elif type(value) == float:
                field_value = Serializer.unserialize_float(byte_array[count:count + 8])
                count += 8
            elif type(value) == bool:
                field_value = Serializer.unserialize_bool(byte_array[count:count + 1])
                count += 1
            if field_value is not None:
                setattr(obj, attr, field_value)
        return obj


class Publication:
    def __init__(self, id=0, isbn="", title="", author="", publisher="", price=0.0, available=False):
        self.id = id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.price = price
        self.available = available

    def __str__(self):
        return str(self.id) + "," + self.isbn + "," + self.title + "," + self.author + "," + self.publisher + "," + str(self.price) + "," + str(self.available)

if __name__ == "__main__":
    publication = Publication(
        1729, "748159263-BADASS", "Lærd of The Rïngs", "Stephen King", "Sántillana", 16.561233895177, True)
    print publication
    byte_array = Serializer.serialize(publication)
    print len(byte_array)

    same_publication = Serializer.unserialize(byte_array, Publication)
    print same_publication
    same_byte_array = Serializer.serialize(same_publication)
    print len(same_byte_array)

    print "---------------------------------------------------------------------------------"

    p1 = Publication(1729, "748159263-BADASS", "Lærd of The Rïngs", "Stephen King", "Sántillana", 16.561233895177, True)
    p2 = Publication(4367, "446471231-ZHHHJJ", "Trying other stuff", "Linus Torvals", "Anaya", 5.1623, False)
    p3 = Publication(8888, "000001231-MNMNMM", "A punto de salir está", "Luis Bárcenas", "PP", 1.5, True)
    publications = list()
    publications.append(p1)
    publications.append(p2)
    publications.append(p3)
    byte_array = Serializer.serialize_list(publications)

    same_publications = Serializer.unserialize_list(byte_array, Publication)
    for i in same_publications:
        print i
