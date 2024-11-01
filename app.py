from flask import Flask, render_template, request, redirect
from database import db, Vehicle, Feedback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', methods=["GET", "POST"])
def home():
    vehicles = Vehicle.query.all()
    feedbacks = Feedback.query.all()

    if request.method == "POST":
        model = request.form.get("model")
        brand = request.form.get("brand")
        price = request.form.get("price")

        if model and brand and price:
            try:
                price = float(price)
                vehicle = Vehicle(model=model, brand=brand, price=price)
                db.session.add(vehicle)
                db.session.commit()
                return redirect("/")
            except ValueError:
                print("Preço inválido, não foi possível adicionar o veículo.")

    return render_template("index.html", vehicles=vehicles, feedbacks=feedbacks)

@app.route("/vehicle/<int:vehicle_id>")
def vehicle_detail(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return render_template("info_mais.html", vehicle=vehicle)

@app.route("/update/<int:vehicle_id>", methods=["GET", "POST"])
def update(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if request.method == "POST":
        vehicle.model = request.form.get("newmodel")
        vehicle.brand = request.form.get("newbrand")
        vehicle.price = float(request.form.get("newprice"))
        db.session.commit()
        return redirect("/")
    return render_template("update_vehicle.html", vehicle=vehicle)

@app.route("/delete", methods=["POST"])
def delete():
    model = request.form.get("model")
    vehicle = Vehicle.query.filter_by(model=model).first()
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
    return redirect("/")

@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name")
        user_feedback = request.form.get("feedback")
        if name and user_feedback:
            feedback_entry = Feedback(name=name, message=user_feedback)
            db.session.add(feedback_entry)
            db.session.commit()
            return redirect("/")
    return render_template("feedback.html")

@app.route('/search', methods=["POST"])
def search():
    search_query = request.form.get("search_query")
    vehicles = Vehicle.query.filter(Vehicle.model.contains(search_query)).all()
    feedbacks = Feedback.query.all()
    return render_template("index.html", vehicles=vehicles, feedbacks=feedbacks)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
