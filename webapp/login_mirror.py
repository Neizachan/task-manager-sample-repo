"""Local look-alike of https://the-internet.herokuapp.com/login (same element ids / flash messages).
Used ONLY for the locator-drift step of Lab 5, because you cannot edit a public site.
  python -m webapp.login_mirror                      -> normal page  (username input id="username")
  $env:USERNAME_ID="user-name"; python -m webapp.login_mirror   -> DRIFTED page (id renamed)
"""
import os
from flask import Flask, redirect, request, render_template_string

MSG = {
    "ok": ("success", "You logged into a secure area!"),
    "user": ("error", "Your username is invalid!"),
    "pass": ("error", "Your password is invalid!"),
}
PAGE = """<!doctype html><title>The Internet (mirror)</title>
<h2>Login Page</h2>
{% if flash %}<div id="flash" class="flash {{ flash[0] }}">{{ flash[1] }} <a href="#" class="close">x</a></div>{% endif %}
<form action="/authenticate" method="post">
  <input type="text" name="username" id="{{ uid }}">
  <input type="password" name="password" id="password">
  <button class="radius" type="submit">Login</button>
</form>"""


def create_app():
    app = Flask(__name__)
    uid = os.environ.get("USERNAME_ID", "username")

    @app.get("/login")
    def login():
        return render_template_string(PAGE, uid=uid, flash=MSG.get(request.args.get("msg")))

    @app.get("/secure")
    def secure():
        return render_template_string("<h2>Secure Area</h2>{% if flash %}<div id='flash' class='flash success'>{{ flash[1] }} <a href='#' class='close'>x</a></div>{% endif %}", flash=MSG["ok"])

    @app.post("/authenticate")
    def authenticate():
        u, p = request.form.get("username", ""), request.form.get("password", "")
        if u != "tomsmith":
            return redirect("/login?msg=user")
        if p != "SuperSecretPassword!":
            return redirect("/login?msg=pass")
        return redirect("/secure")

    return app


if __name__ == "__main__":
    create_app().run()
