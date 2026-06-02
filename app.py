import os
import frontmatter
import markdown
from flask import Flask, render_template, abort

app = Flask(__name__)

PROJECTS_DIR = os.path.join(os.path.dirname(__file__), "content", "projects")
POSTS_DIR = os.path.join(os.path.dirname(__file__), "content", "posts")

MD = markdown.Markdown(extensions=["fenced_code", "codehilite"])


def _render_md(text):
    MD.reset()
    return MD.convert(text)


def _parse_file(path):
    post = frontmatter.load(path)
    data = dict(post.metadata)
    data["body_html"] = _render_md(post.content)
    return data


def load_projects():
    projects = []
    for fname in os.listdir(PROJECTS_DIR):
        if fname.endswith(".md"):
            projects.append(_parse_file(os.path.join(PROJECTS_DIR, fname)))
    projects.sort(key=lambda p: p.get("date", ""), reverse=True)
    return projects


def load_posts():
    posts = []
    for fname in os.listdir(POSTS_DIR):
        if fname.endswith(".md"):
            posts.append(_parse_file(os.path.join(POSTS_DIR, fname)))
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    return posts


def get_project(slug):
    for p in load_projects():
        if p.get("slug") == slug:
            return p
    return None


def get_post(slug):
    for p in load_posts():
        if p.get("slug") == slug:
            return p
    return None


@app.context_processor
def inject_author():
    return {"author": "Jamie Thomson"}


@app.route("/")
def index():
    projects = [p for p in load_projects() if p.get("featured")]
    posts = load_posts()[:3]
    return render_template("index.html", title="Jamie Thomson", projects=projects, posts=posts)


@app.route("/projects")
def projects():
    all_projects = load_projects()
    return render_template("projects.html", title="Projects", projects=all_projects)


@app.route("/projects/<slug>")
def project(slug):
    p = get_project(slug)
    if p is None:
        abort(404)
    return render_template("project.html", title=p["title"], project=p)


@app.route("/blog")
def blog():
    all_posts = load_posts()
    return render_template("blog.html", title="Blog", posts=all_posts)


@app.route("/blog/<slug>")
def post(slug):
    p = get_post(slug)
    if p is None:
        abort(404)
    return render_template("post.html", title=p["title"], post=p)


@app.route("/about")
def about():
    return render_template("about.html", title="About Me")


if __name__ == "__main__":
    app.run(debug=True)
