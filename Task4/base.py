import mysql.connector as msc
import queries


class BaseWorker:
    def __init__(self, host, user, password, base):
        self.connection = None
        try:
            self.connection = msc.connect(
                host=host, user=user, password=password, database=base
            )
        except msc.InterfaceError:
            print("You entered an invalid server address.")
        except msc.ProgrammingError:
            print("Invalid username or password.")

    def create_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute(queries.create_rooms)
            cursor.execute(queries.create_students)
        self.connection.commit()

    def create_indexes(self):
        with self.connection.cursor() as cursor:
            cursor.execute(queries.index_sex)
            cursor.execute(queries.index_birthday)

    def insert_tables(self, rooms, students):
        with self.connection.cursor() as cursor:
            cursor.execute(queries.clear_rooms)
            cursor.executemany(queries.insert_rooms, rooms)
            cursor.execute(queries.clear_students)
            cursor.executemany(queries.insert_students, students)

        self.connection.commit()

    def query_exectutor(self, query, with_value):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
            except msc.Error as err:
                print(err)
            result = cursor.fetchall()
            result = (
                [{"room": room, "value": value} for room, value in result]
                if with_value
                else [{"room": room[0]} for room in result]
            )
            return result
