# Ledger — Student Management System

A capstone project that ties together everything from Weeks 1–8: variables,
control flow, collections, functions, files, and OOP — built as an
interactive web app.

## 1. What's in the box

```
sms/
├── app.py                 Flask web server + all API routes
├── models.py               Student / Teacher / Course classes (OOP)
├── data_manager.py         Reads & writes the JSON files safely
├── requirements.txt         Python packages this project needs
├── data/                    Your saved data lives here as JSON
│   ├── students.json
│   ├── teachers.json
│   ├── courses.json
│   ├── marks.json
│   └── attendance.json
├── templates/
│   └── index.html           The single page the browser loads
└── static/
    ├── css/style.css        All the styling
    └── js/app.js             All the interactivity (fetch calls, tables, forms)
```

## 2. How to run it

You need Python 3.9+ installed. Then, in a terminal, inside the `sms` folder:

```bash
pip install -r requirements.txt
python app.py
```

You'll see something like:

```
 * Running on http://127.0.0.1:5000
```

Open that address in your browser. That's it — the whole app runs on your
own computer, and everything you add is saved permanently into the `.json`
files inside `data/`.

To stop the server, go back to the terminal and press `Ctrl + C`.

## 3. How to use it

1. Go to **Teachers** and add a teacher (name, email, subject).
2. Go to **Courses** and add a course, assigning the teacher you just made.
3. Go to **Students** and add a student, ticking which course(s) they're in
   (hold `Ctrl`/`Cmd` to select more than one in the box).
4. Go to **Marks** to log a score for a student in a course.
5. Go to **Attendance** to mark them Present / Late / Absent for the day.
6. Go to **Dashboard** to see live statistics recalculated from everything
   you entered — total students, class average, attendance rate, and the
   top-performing student.

Every add/remove instantly updates the `.json` file on disk — refresh the
page or restart the server and your data is still there.

## 4. How this maps to what you learned

| Week | Concept | Where it shows up |
|---|---|---|
| 1 | Variables, data types, operators | Form values, `credits`, `score` math throughout `app.py` |
| 2 | Conditionals, loops, strings | `if`/`for` in `app.py` routes, f-strings in `models.py` |
| 3 | Lists, dicts, sets | Every `.json` file is a **list of dicts**; statistics use dict-building patterns |
| 4 | Functions, modules, files, exceptions | Every route is a function; `data_manager.py` does file I/O with `try/except` |
| 5 | Classes & objects | `Person`, `Student`, `Teacher`, `Course` in `models.py` |
| 6-7 | Inheritance & polymorphism | `Student` and `Teacher` both inherit from `Person`; each overrides `to_dict()` |
| 8 | JSON | Every route reads/writes JSON; the whole API speaks JSON to the browser |

## 5. Ideas to extend it yourself (good practice!)

- Add a "Reports" tab that shows each student's grade per course, not just overall.
- Add form validation messages instead of `alert()` popups.
- Add a search/filter box on the Students table.
- Swap JSON storage for a real database (SQLite) once you learn `sqlite3`.
- Add login so each teacher only sees their own courses.

## 6. If something goes wrong

- **`ModuleNotFoundError: No module named 'flask'`** → run
  `pip install -r requirements.txt` again.
- **Port already in use** → another program is using port 5000. Stop it, or
  change the last line of `app.py` to `app.run(debug=True, port=5050)`.
