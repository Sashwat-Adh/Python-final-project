/*
  app.js
  ------
  This is the "interactive" part of the app. It runs in the browser.
  Every time you add/delete something, it calls our Flask API (fetch),
  gets JSON back, and re-draws the page — no full page reload needed.

  Structure:
    1. Tiny helpers (fetchJSON, formatting)
    2. Tab / section switching
    3. Loaders for each module (students, teachers, courses, marks, attendance)
    4. Form submit handlers
    5. Dashboard statistics
    6. Initial boot
*/

// ---------------------------------------------------------------------------
// 1. Helpers
// ---------------------------------------------------------------------------

async function fetchJSON(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error || `Request to ${url} failed`);
  }
  return data;
}

// In-memory cache of the latest lists, so dropdowns/tables can cross-reference
// each other (e.g. show a student's name next to a mark) without refetching.
const state = {
  students: [],
  teachers: [],
  courses: [],
  marks: [],
  attendance: [],
};

// ---------------------------------------------------------------------------
// 2. Tab switching
// ---------------------------------------------------------------------------

document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".section").forEach((s) => s.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`section-${btn.dataset.section}`).classList.add("active");
  });
});

// ---------------------------------------------------------------------------
// 3. Loaders
// ---------------------------------------------------------------------------

async function loadStudents() {
  state.students = await fetchJSON("/api/students");
  renderStudents();
  populateSelect("student-course-select", state.courses, (c) => `${c.code} — ${c.name}`);
  populateSelect("mark-student-select", state.students, (s) => s.name);
  populateSelect("attendance-student-select", state.students, (s) => s.name);
}

async function loadTeachers() {
  state.teachers = await fetchJSON("/api/teachers");
  renderTeachers();
  populateSelect("course-teacher-select", state.teachers, (t) => t.name, true, "No teacher assigned");
}

async function loadCourses() {
  state.courses = await fetchJSON("/api/courses");
  renderCourses();
  populateSelect("student-course-select", state.courses, (c) => `${c.code} — ${c.name}`);
  populateSelect("mark-course-select", state.courses, (c) => `${c.code} — ${c.name}`);
  populateSelect("attendance-course-select", state.courses, (c) => `${c.code} — ${c.name}`);
}

async function loadMarks() {
  state.marks = await fetchJSON("/api/marks");
  renderMarks();
}

async function loadAttendance() {
  state.attendance = await fetchJSON("/api/attendance");
  renderAttendance();
}

async function loadStatistics() {
  const stats = await fetchJSON("/api/statistics");
  document.getElementById("stat-students").textContent = stats.total_students;
  document.getElementById("stat-teachers").textContent = stats.total_teachers;
  document.getElementById("stat-courses").textContent = stats.total_courses;
  document.getElementById("stat-marks").textContent = stats.total_marks_recorded;
  document.getElementById("stat-avg").textContent = `${stats.average_mark_percent}%`;
  document.getElementById("stat-attendance").textContent = `${stats.attendance_rate_percent}%`;

  const topEl = document.getElementById("top-student");
  topEl.textContent = stats.top_student
    ? `${stats.top_student.name} is leading the class with a ${stats.top_student.average}% average.`
    : "No marks recorded yet.";
}


// ---------------------------------------------------------------------------
// Small render helpers
// ---------------------------------------------------------------------------

function populateSelect(id, items, labelFn, includeEmpty = false, emptyLabel = "—") {
  const select = document.getElementById(id);
  if (!select) return;
  const previouslySelected = new Set(
    Array.from(select.selectedOptions || []).map((o) => o.value)
  );
  select.innerHTML = "";
  if (includeEmpty) {
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = emptyLabel;
    select.appendChild(opt);
  }
  items.forEach((item) => {
    const opt = document.createElement("option");
    opt.value = item.id;
    opt.textContent = labelFn(item);
    if (previouslySelected.has(item.id)) opt.selected = true;
    select.appendChild(opt);
  });
}

function studentName(id) {
  const s = state.students.find((s) => s.id === id);
  return s ? s.name : "(removed student)";
}

function teacherName(id) {
  const t = state.teachers.find((t) => t.id === id);
  return t ? t.name : "Unassigned";
}

function courseLabel(id) {
  const c = state.courses.find((c) => c.id === id);
  return c ? `${c.code} — ${c.name}` : "(removed course)";
}

function emptyRow(colspan, text) {
  return `<tr><td class="empty" colspan="${colspan}">${text}</td></tr>`;
}

// ---------------------------------------------------------------------------
// Render tables
// ---------------------------------------------------------------------------

function renderStudents() {
  const body = document.getElementById("students-body");
  if (state.students.length === 0) {
    body.innerHTML = emptyRow(4, "No students yet — add your first one above.");
    return;
  }
  body.innerHTML = state.students.map((s) => `
    <tr>
      <td>${s.name}</td>
      <td>${s.email}</td>
      <td>${(s.course_ids || []).map(courseLabel).join(", ") || "—"}</td>
      <td><button class="row-delete" data-kind="students" data-id="${s.id}">✕ remove</button></td>
    </tr>
  `).join("");
}

function renderTeachers() {
  const body = document.getElementById("teachers-body");
  if (state.teachers.length === 0) {
    body.innerHTML = emptyRow(4, "No teachers yet — add your first one above.");
    return;
  }
  body.innerHTML = state.teachers.map((t) => `
    <tr>
      <td>${t.name}</td>
      <td>${t.email}</td>
      <td>${t.subject || "—"}</td>
      <td><button class="row-delete" data-kind="teachers" data-id="${t.id}">✕ remove</button></td>
    </tr>
  `).join("");
}

function renderCourses() {
  const body = document.getElementById("courses-body");
  if (state.courses.length === 0) {
    body.innerHTML = emptyRow(5, "No courses yet — add your first one above.");
    return;
  }
  body.innerHTML = state.courses.map((c) => `
    <tr>
      <td>${c.code}</td>
      <td>${c.name}</td>
      <td>${teacherName(c.teacher_id)}</td>
      <td>${c.credits}</td>
      <td><button class="row-delete" data-kind="courses" data-id="${c.id}">✕ remove</button></td>
    </tr>
  `).join("");
}

function renderMarks() {
  const body = document.getElementById("marks-body");
  if (state.marks.length === 0) {
    body.innerHTML = emptyRow(6, "No marks logged yet.");
    return;
  }
  body.innerHTML = state.marks.map((m) => {
    const pct = m.max_score ? ((m.score / m.max_score) * 100).toFixed(1) : "—";
    return `
    <tr>
      <td>${studentName(m.student_id)}</td>
      <td>${courseLabel(m.course_id)}</td>
      <td>${m.score} / ${m.max_score}</td>
      <td>${pct}%</td>
      <td>${m.date}</td>
      <td><button class="row-delete" data-kind="marks" data-id="${m.id}">✕ remove</button></td>
    </tr>`;
  }).join("");
}

function renderAttendance() {
  const body = document.getElementById("attendance-body");
  if (state.attendance.length === 0) {
    body.innerHTML = emptyRow(5, "No attendance logged yet.");
    return;
  }
  body.innerHTML = state.attendance.map((a) => `
    <tr>
      <td>${studentName(a.student_id)}</td>
      <td>${courseLabel(a.course_id)}</td>
      <td><span class="pill ${a.status.toLowerCase()}">${a.status}</span></td>
      <td>${a.date}</td>
      <td><button class="row-delete" data-kind="attendance" data-id="${a.id}">✕ remove</button></td>
    </tr>
  `).join("");
}

// ---------------------------------------------------------------------------
// 4. Delete buttons (event delegation — one listener for the whole page)
// ---------------------------------------------------------------------------

document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".row-delete");
  if (!btn) return;
  const { kind, id } = btn.dataset;
  try {
    await fetchJSON(`/api/${kind}/${id}`, { method: "DELETE" });
    await refreshAll();
  } catch (err) {
    alert(err.message);
  }
});

// ---------------------------------------------------------------------------
// 4b. Form submissions
// ---------------------------------------------------------------------------

function formToObject(form, multiSelectFields = []) {
  const fd = new FormData(form);
  const obj = {};
  for (const [key, value] of fd.entries()) {
    if (multiSelectFields.includes(key)) continue; // handled separately
    obj[key] = value;
  }
  multiSelectFields.forEach((field) => {
    const select = form.querySelector(`[name="${field}"]`);
    if (select) {
      obj[field] = Array.from(select.selectedOptions).map((o) => o.value).filter(Boolean);
    }
  });
  return obj;
}

document.getElementById("form-student").addEventListener("submit", async (e) => {
  e.preventDefault();
  const obj = formToObject(e.target, ["course_ids"]);
  try {
    await fetchJSON("/api/students", { method: "POST", body: JSON.stringify(obj) });
    e.target.reset();
    await refreshAll();
  } catch (err) { alert(err.message); }
});

document.getElementById("form-teacher").addEventListener("submit", async (e) => {
  e.preventDefault();
  const obj = formToObject(e.target);
  try {
    await fetchJSON("/api/teachers", { method: "POST", body: JSON.stringify(obj) });
    e.target.reset();
    await refreshAll();
  } catch (err) { alert(err.message); }
});

document.getElementById("form-course").addEventListener("submit", async (e) => {
  e.preventDefault();
  const obj = formToObject(e.target);
  obj.credits = Number(obj.credits) || 3;
  if (!obj.teacher_id) delete obj.teacher_id;
  try {
    await fetchJSON("/api/courses", { method: "POST", body: JSON.stringify(obj) });
    e.target.reset();
    await refreshAll();
  } catch (err) { alert(err.message); }
});

document.getElementById("form-mark").addEventListener("submit", async (e) => {
  e.preventDefault();
  const obj = formToObject(e.target);
  obj.score = Number(obj.score);
  obj.max_score = Number(obj.max_score);
  try {
    await fetchJSON("/api/marks", { method: "POST", body: JSON.stringify(obj) });
    e.target.reset();
    await refreshAll();
  } catch (err) { alert(err.message); }
});

document.getElementById("form-attendance").addEventListener("submit", async (e) => {
  e.preventDefault();
  const obj = formToObject(e.target);
  try {
    await fetchJSON("/api/attendance", { method: "POST", body: JSON.stringify(obj) });
    e.target.reset();
    await refreshAll();
  } catch (err) { alert(err.message); }
});

// ---------------------------------------------------------------------------
// 5 & 6. Boot
// ---------------------------------------------------------------------------

async function refreshAll() {
  // Teachers and courses first, since students/marks/attendance dropdowns
  // depend on them already being in `state`.
  await loadTeachers();
  await loadCourses();
  await loadStudents();
  await loadMarks();
  await loadAttendance();
  await loadStatistics();
}

refreshAll();
