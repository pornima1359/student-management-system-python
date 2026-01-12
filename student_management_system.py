import sqlite3

# -------------------------------
# Student Class
# -------------------------------
class Student:
    def __init__(self, student_id, name, age, course):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course


# -------------------------------
# Database Class
# -------------------------------
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("students.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                course TEXT
            )
        """)
        self.conn.commit()

    def add_student(self, student):
        try:
            self.cursor.execute(
                "INSERT INTO students VALUES (?, ?, ?, ?)",
                (student.student_id, student.name, student.age, student.course)
            )
            self.conn.commit()
            print("✅ Student added successfully!")
        except sqlite3.IntegrityError:
            print("❌ Student ID already exists!")

    def view_students(self):
        self.cursor.execute("SELECT * FROM students")
        students = self.cursor.fetchall()
        if not students:
            print("⚠ No student records found.")
        for s in students:
            print(s)

    def search_student(self, student_id):
        self.cursor.execute(
            "SELECT * FROM students WHERE student_id=?",
            (student_id,)
        )
        student = self.cursor.fetchone()
        if student:
            print("🔍 Student Found:", student)
        else:
            print("❌ Student not found.")

    def update_student(self, student):
        self.cursor.execute("""
            UPDATE students
            SET name=?, age=?, course=?
            WHERE student_id=?
        """, (student.name, student.age, student.course, student.student_id))
        self.conn.commit()
        if self.cursor.rowcount:
            print("✏ Student updated successfully!")
        else:
            print("❌ Student ID not found.")

    def delete_student(self, student_id):
        self.cursor.execute(
            "DELETE FROM students WHERE student_id=?",
            (student_id,)
        )
        self.conn.commit()
        if self.cursor.rowcount:
            print("🗑 Student deleted successfully!")
        else:
            print("❌ Student ID not found.")


# -------------------------------
# Main Program
# -------------------------------
def menu():
    print("\n===== Student Management System =====")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")


def main():
    db = Database()

    while True:
        menu()
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            try:
                sid = int(input("Student ID: "))
                name = input("Name: ")
                age = int(input("Age: "))
                course = input("Course: ")
                student = Student(sid, name, age, course)
                db.add_student(student)
            except ValueError:
                print("⚠ Please enter valid input.")

        elif choice == "2":
            db.view_students()

        elif choice == "3":
            sid = int(input("Enter Student ID: "))
            db.search_student(sid)

        elif choice == "4":
            try:
                sid = int(input("Student ID: "))
                name = input("New Name: ")
                age = int(input("New Age: "))
                course = input("New Course: ")
                student = Student(sid, name, age, course)
                db.update_student(student)
            except ValueError:
                print("⚠ Invalid input.")

        elif choice == "5":
            sid = int(input("Enter Student ID: "))
            db.delete_student(sid)

        elif choice == "6":
            print("👋 Exiting Student Management System")
            break

        else:
            print("⚠ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
