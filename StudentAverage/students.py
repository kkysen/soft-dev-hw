from collections import KeysView

from csv2db import Database


class Student(object):
    def __init__(self, id, name, num_classes, average):
        # type: (int, str, int, float) -> None
        self.id = id
        self.name = name
        self.num_classes = num_classes
        self.average = average

    def __str__(self):
        return 'Student[id={}, name={}, num_classes={}, average={}]'\
            .format(self.id, self.name, self.num_classes, self.average)

    def __repr__(self):
        return str(self)


class Students(object):
    """Wrapper for students, courses, and averages tables."""

    def __init__(self,
                 db_path='students.db',
                 students_csv_path='students.csv',
                 courses_csv_path='courses.csv',
                 averages_table_name='peeps_avg'):
        # type: () -> None

        self.db = Database(db_path)

        self.students_table_name = \
            self.db.add_csv(students_csv_path, types=('TEXT', 'INT', 'INT PRIMARY KEY'))

        self.courses_table_name = \
            self.db.add_csv(courses_csv_path, types=('TEXT', 'INT', 'INT'))

        self.averages_table_name = \
            Database.sanitize(averages_table_name)

        self.students = self._compute_averages()
        self._create_averages_table()

    def _compute_averages(self):
        # type: () -> dict[int, Student]

        query = 'SELECT name, id, grade FROM students, courses WHERE id = student_id'

        students = {}  # type: dict[int, Student]
        for name, id, grade in self.db.cursor.execute(query):
            if id in students:
                student = students[id]  # type: Student
                student.average += grade
                student.num_classes += 1
            else:
                students[id] = Student(id, name, 1, float(grade))

        for student in students.viewvalues():
            student.average /= student.num_classes

        return students

    def _create_averages_table(self):
        if self.db.table_exists(self.averages_table_name):
            return

        self.db.cursor.execute(
            'CREATE TABLE {} (id INT PRIMARY KEY, average DOUBLE)'
                .format(self.averages_table_name))
        self.db.cursor.executemany(
            'INSERT INTO {} VALUES (?, ?)'.format(self.averages_table_name),
            [(student.id, student.average) for student in self.students.viewvalues()])

    def add_course(self, student_id, class_name, grade):
        # type: (int, str, float) -> None

        # update RAM dict
        student = self.students[student_id]
        total_grade = (student.average * student.num_classes) + grade
        student.average = total_grade / (student.num_classes + 1)
        student.num_classes += 1

        # update averages table
        self.db.cursor.execute(
            'UPDATE {} SET average = ? WHERE id = ?'.format(self.averages_table_name),
            [student.average, student_id])

        # update courses table
        self.db.cursor.execute('INSERT INTO {} VALUES (?, ?, ?)'.format(self.courses_table_name),
                               [class_name, grade, student_id])

        self.db.commit()

    def ids(self):
        # type: () -> KeysView[int]
        return self.students.viewkeys()

    def __str__(self):
        # type: () -> str
        return '\n'.join(str(student) for id, student in sorted(self.students.viewitems()))

    def __repr__(self):
        # type: () -> str
        return str(self)

    def __enter__(self):
        # type: () -> Students
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # type: () -> None
        self.db.close()

    def print_averages(self):
        # type: () -> None
        print(self)
