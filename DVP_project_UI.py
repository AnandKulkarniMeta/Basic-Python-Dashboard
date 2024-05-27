from flask import Flask, render_template, request, jsonify
import csv
from datetime import datetime

app = Flask(__name__)
FILE_PATH = "file path of .csv file here"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.form.to_dict()

    current_date = datetime.now().strftime('%m/%d/%Y')
    current_time = datetime.now().strftime('%H:%M:%S')

    try:
        rating = float(data.get("Rating", ""))
    except ValueError:
        return jsonify({"error": "Invalid rating value. Must be a number."}), 400

    if rating <= 5.0:
        customer_satisfaction = "Bad"
    elif 5.0 < rating <= 7.5:
        customer_satisfaction = "Good"
    elif rating > 7.5:
        customer_satisfaction = "Best"
    else:
        customer_satisfaction = "Good"

    try:
        unit_price = float(data.get("Unit price", ""))
        quantity = float(data.get("Quantity", ""))
    except ValueError:
        return jsonify({"error": "Invalid unit price or quantity. Must be a number."}), 400

    cogs = unit_price * quantity

    tax = 0.05 * cogs
    total = tax + cogs
    with open(FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Invoice ID", "Branch", "City", "Customer type", "Gender",
            "Product line", "Unit price", "Quantity", "Tax 5%", "Total",
            "Date", "Time", "Payment", "cogs", "gross margin percentage",
            "gross income", "Rating", "Customer satisfaction"
        ])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({
            "Invoice ID": data.get("Invoice ID", ""),
            "Branch": data.get("Branch", ""),
            "City": data.get("City", ""),
            "Customer type": data.get("Customer type", ""),
            "Gender": data.get("Gender", ""),
            "Product line": data.get("Product line", ""),
            "Unit price": unit_price,
            "Quantity": quantity,
            "Tax 5%": tax,
            "Total": total,
            "Date": current_date,
            "Time": current_time,
            "Payment": data.get("Payment", ""),
            "cogs": cogs,
            "gross margin percentage": "4.761904762",
            "gross income": tax,
            "Rating": rating,
            "Customer satisfaction": customer_satisfaction
        })

    return jsonify({"message": "Data saved successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
