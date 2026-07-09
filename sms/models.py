"""
models.py
---------
Week 5-7 (Object-Oriented Programming) concepts live here.

We define three classes: Student, Teacher, and Course.
Each one demonstrates:
  - the __init__ constructor
  - instance attributes
  - encapsulation (using a leading underscore _ for "internal" fields)
  - a to_dict() method (turns the object into a plain dict, ready for JSON)
  - a from_dict() class method (rebuilds an object FROM a dict loaded from JSON)
  - __str__ / __repr__ special methods

Person is a small base class that Student and Teacher both inherit from.
This shows inheritance: both share a name/email/id, but each adds its own
extra fields. Since to_dict() is overridden differently in each subclass but
called the exact same way everywhere, that's polymorphism in action.
"""

import uuid


class Person:
    """Base class shared by Student and Teacher (inheritance)."""

    def __init__(self, name, email, person_id=None):
        self._id = person_id or str(uuid.uuid4())[:8]
        self.name = name
        self.email = email

    @property
    def id(self):
        return self._id

    def to_dict(self):
        return {"id": self._id, "name": self.name, "email": self.email}

    def __str__(self):
        return f"{self.name} <{self.email}>"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._id!r}, name={self.name!r})"


class Student(Person):
    """A student. Inherits id/name/email from Person, adds student-specific data."""

    def __init__(self, name, email, course_ids=None, person_id=None):
        super().__init__(name, email, person_id)
        self.course_ids = course_ids or []  # Course ids this student is enrolled in

    def to_dict(self):
        data = super().to_dict()
        data["course_ids"] = self.course_ids
        return data

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d["name"],
            email=d["email"],
            course_ids=d.get("course_ids", []),
            person_id=d.get("id"),
        )


class Teacher(Person):
    """A teacher. Inherits id/name/email from Person, adds a subject specialty."""

    def __init__(self, name, email, subject="", person_id=None):
        super().__init__(name, email, person_id)
        self.subject = subject

    def to_dict(self):
        data = super().to_dict()
        data["subject"] = self.subject
        return data

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d["name"],
            email=d["email"],
            subject=d.get("subject", ""),
            person_id=d.get("id"),
        )


class Course:
    """A course, taught by one teacher, with a code, name and credit value."""

    def __init__(self, name, code, teacher_id=None, credits=3, course_id=None):
        self._id = course_id or str(uuid.uuid4())[:8]
        self.name = name
        self.code = code
        self.teacher_id = teacher_id
        self.credits = credits

    @property
    def id(self):
        return self._id

    def to_dict(self):
        return {
            "id": self._id,
            "name": self.name,
            "code": self.code,
            "teacher_id": self.teacher_id,
            "credits": self.credits,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d["name"],
            code=d["code"],
            teacher_id=d.get("teacher_id"),
            credits=d.get("credits", 3),
            course_id=d.get("id"),
        )

    def __str__(self):
        return f"{self.code} - {self.name} ({self.credits} credits)"

    def __repr__(self):
        return f"Course(id={self._id!r}, code={self.code!r})"
