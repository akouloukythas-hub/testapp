from flask import Flask, render_template, request, redirect, url_for
from controllers.product_controller import ProductController
from controllers.order_controller import OrderController
from utils.db_utils import init_db, save_order

app = Flask(__name__)
init_db()

product_ctrl = ProductController()
order_ctrl = OrderController()

@app.route("/")
def index():
    products = product_ctrl.get_all()
    return render_template("index.html", products=products)

@app.route("/add", methods=["POST"])
def add_product():
    product_id = int(request.form.get("product_id"))
    quantity = int(request.form.get("quantity"))
    product = product_ctrl.get_by_id(product_id)
    if product:
        order_ctrl.add_product(product, quantity)
    return redirect(url_for("index"))

@app.route("/order")
def view_order():
    items = order_ctrl.get_order()
    total = order_ctrl.get_total()
    return render_template("order.html", items=items, total=total)

@app.route("/checkout")
def checkout():
    save_order(order_ctrl.order)
    return "Η παραγγελία σας αποθηκεύτηκε στη βάση δεδομένων!"

if __name__ == "__main__":
    app.run(debug=True)
