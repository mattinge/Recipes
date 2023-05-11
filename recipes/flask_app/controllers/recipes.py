
from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route("/recipes/home")
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = { "id": session['user_id']}
    return render_template("dashboard.html", user = User.get_user_by_id(data), recipes = Recipe.get_all_recipes())


@app.route("/recipes/<int: recipe_id>")
def display_recipe(recipe_id):
    user = User.get_user_by_id(session['user_id'])
    recipe = Recipe.get_recipe_by_id(recipe_id)
    return render_template("display_recipe.html", user = user, recipe = recipe)

@app.route("/recipes/add_recipe")
def add_recipe():
    return render_template("create_recipe.html")

@app.route("recipes/edit/<int:recipe_id>")
def edit_recipe(recipe_id):
    recipe = Recipe.get_recipe_by_id(recipe_id)
    return render_template("edit_recipe.html", recipe = recipe)

@app.route("recipes/add", methos=["POST"])
def add_recipe_form():
    valid_recipe = Recipe.create_recipe(request.form)
    if valid_recipe:
        return redirect(f'/recipes/{valid_recipe.id}')
    return redirect("/recipes/add_recipe")

@app.route("/recipes/<int:recipe_id>", methods=['POST'])
def edit_recipe_form(recipe_id):
    valid_recipe = Recipe.edit_recipe(request.form, session["user_id"])
    if not valid_recipe:
        return redirect(f'/recipes/edit/{recipe_id}')
    return redirect(f'/recipes/{recipe_id}')

@app.rotue("/recipes/delete/<int:recipe_id>")
def delete_recipe_by_id(recipe_id)
    Recipe.delete_recipe(recipe_id)
    return redirect("/dashboard")
