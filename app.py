from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)
tasks = [
    {"id": 1, "title": "Understand CI/CD pipeline", "done": False},
    {"id": 2, "title": "Build Docker image", "done": True},
]
next_id = 3

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Student Task Manager</title>
<style>
body{font-family:Arial,sans-serif;background:#f4f7fb;color:#182230;margin:0}
header{background:#183153;color:white;padding:24px;text-align:center}main{max-width:760px;margin:28px auto;padding:0 16px}
.card{background:white;padding:20px;border-radius:12px;box-shadow:0 4px 18px #152b4b12;margin-bottom:18px}
form.add{display:flex;gap:10px}input[type=text]{flex:1;min-width:0;padding:12px;border:1px solid #ccd5e0;border-radius:8px}
button{padding:10px 14px;border:0;border-radius:8px;background:#1769aa;color:white;cursor:pointer}
ul{padding:0;list-style:none}li{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid #edf0f4}
li:last-child{border-bottom:0}.task{flex:1}.done{text-decoration:line-through;color:#718096}.inline{display:inline}.delete{background:#b42318}
.meta{color:#65758b;font-size:.9rem}
</style></head><body>
<header><h1>Student Task Manager</h1><div>CCA 2 • CI/CD Demonstration Application</div></header>
<main><section class="card"><h2>Add a task</h2>
<form class="add" method="post" action="/add"><input type="text" name="title" placeholder="e.g. Test the deployment" required maxlength="120"><button>Add task</button></form>
</section><section class="card"><h2>Your tasks ({{ tasks|length }})</h2>
{% if tasks %}<ul>{% for task in tasks %}<li><span class="task {% if task.done %}done{% endif %}">{{ task.title }}</span>
<form class="inline" method="post" action="/toggle/{{ task.id }}"><button>{% if task.done %}Undo{% else %}Complete{% endif %}</button></form>
<form class="inline" method="post" action="/delete/{{ task.id }}"><button class="delete">Delete</button></form></li>{% endfor %}</ul>
{% else %}<p>No tasks yet. Add your first task above.</p>{% endif %}
<p class="meta">Health check: <a href="/health">/health</a></p></section></main></body></html>"""

@app.get("/")
def index():
    return render_template_string(PAGE, tasks=tasks)

@app.get("/health")
def health():
    return {"status": "ok", "application": "student-task-manager"}, 200

@app.post("/add")
def add():
    global next_id
    title = request.form.get("title", "").strip()
    if title:
        tasks.append({"id": next_id, "title": title[:120], "done": False})
        next_id += 1
    return redirect(url_for("index"))

@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect(url_for("index"))

@app.post("/delete/<int:task_id>")
def delete(task_id):
    tasks[:] = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
