from flask import Flask, render_template, request, redirect, url_for
import db




app = Flask(__name__)


# Home route to display inventory items with search and sort functionality
@app.route("/")
def home():
    search = request.args.get("search", "")
    sort_by = request.args.get("sort", "")
    
    items = db.get_all_items()
    
    # Filtering the items based on the search query
    if search:
        items = [item for item in items if search.lower() in item[1].lower()]
        
    # Sorting the items based on the selected criteria 
    if sort_by == "name":
        items.sort(key=lambda x: x[1].lower())
    elif sort_by == "quantity":
        items.sort(key=lambda x: x[2])
    elif sort_by == "price":
        items.sort(key=lambda x: x[3])
        
    # Rendering the home page with the filtered and sorted items
    return render_template("home.html", items=items, search=search, sort_by=sort_by)


@app.route("/add", methods=["POST", "GET"])
def add():
    error = ""
    
    if request.method == "POST":
        name = request.form["name"]
        qty = int(request.form["quantity"])
        price = float(request.form["price"])
        
        # Validating the input data before adding the item to the database
        if not name or qty < 0 or price < 0:
            error = "Please provide valid inputs for all fields."
            return render_template("add.html", error=error)
        else:
            db.add_item(name, qty, price)
            return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/delete/<int:item_id>")
def delete(item_id):
    db.delete_item(item_id)
    return redirect(url_for("home"))


@app.route("/edit/<int:item_id>", methods=["POST", "GET"])
def edit(item_id):
    item = db.get_item_by_id(item_id)
    if request.method == "POST":
        name = request.form["name"]
        qty = int(request.form["quantity"])
        price = float(request.form["price"])
        
        db.update_item(item_id, name, qty, price)
        return redirect(url_for("home"))
    return render_template("edit.html", item=item)


if __name__ == "__main__":
    app.run(debug=True)