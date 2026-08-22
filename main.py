#Импорт
from flask import Flask, render_template,request, redirect, flash



app = Flask(__name__)
app.secret_key = "eco-score-belajar"
# DB_PATH = os.path.join(os.path.dirname(__file__), "eco_score.db")

WASTE = {
    "plastic": {"name": "Plastik", "icon": "🥤", "factor": 1.5, 
        "desc": "Botol, gelas, kantong, dan kemasan plastik. Bisa digunakan kembali atau disalurkan ke bank sampah.", "example": "Memilah botol plastik lalu menyetorkannya."},
    "paper": {"name": "Kertas", "icon": "📄", "factor": 1.0,  
        "desc": "Koran, kardus, buku, dan kertas bekas. Keringkan dan pisahkan dari sampah lain.", "example": "Mengumpulkan kardus dan kertas untuk didaur ulang."},
    "metal": {"name": "Logam", "icon": "🥫", "factor": 4.0, 
        "desc": "Kaleng aluminium dan benda logam tertentu. Material logam bisa dipilah dan dilebur kembali.", "example": "Memilah kaleng minuman dan menyetorkannya."},
    "glass": {"name": "Kaca", "icon": "🍾", "factor": 0.5,
        "desc": "Botol dan toples kaca. Jika masih aman, gunakan kembali sebelum didaur ulang.", "example": "Menggunakan kembali toples kaca di rumah."},
    "organic": {"name": "Organik", "icon": "🍌", "factor": 0.4,
        "desc": "Sisa makanan, daun, dan bahan alami yang mudah terurai.", "example": "Memilah sisa makanan untuk dibuat kompos."},
    "ewaste": {"name": "E-waste", "icon": "🔌", "factor": 2.5,
        "desc": "Baterai, kabel, charger, dan perangkat elektronik yang sudah tidak dipakai.", "example": "Mengumpulkan baterai dan menyerahkannya ke pengelola e-waste."},
}

ACTIVITY = {
    "recycle": {"name": "Daur ulang", "icon": "♻️", "mult": 1.0, "desc": "Material masuk ke proses daur ulang."},
    "reuse": {"name": "Gunakan kembali", "icon": "🔁", "mult": 0.75, "desc": "Barang digunakan lagi sehingga tidak cepat menjadi sampah."},
    "dropoff": {"name": "Setor ke bank sampah", "icon": "🏦", "mult": 0.9, "desc": "Material dipilah lalu disalurkan ke pengelola."},
    "compost": {"name": "Kompos", "icon": "🌱", "mult": 1.0, "desc": "Khusus sampah organik: diolah menjadi kompos."},
}

def calculate(waste_key,activity_key,kg):
    waste=WASTE[waste_key]
    activity=ACTIVITY[activity_key]
    co2=kg*waste["factor"]*activity["mult"]
    score = min(100, max(0, round(co2 * 8 + kg * 3)))
    return {"co2": co2, "score": score, "trees": co2 / 21, "kg": kg,
            "waste_name": waste["name"], "activity_name": activity["name"]}
#Halaman Konten Berjalan

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    button_python = None
    button_discord = None
    selected_waste = "plastic"
    selected_activity = "recycle"
    amount = 1.0

    if request.method == "POST":
        # Portfolio project buttons tetap bekerja seperti versi awal.
        button_python = request.form.get("button_python")
        button_discord = request.form.get("button_discord")

        # Calculator berada di halaman / yang sama.
        if request.form.get("form_type") == "calculator":
            selected_waste = request.form.get("waste", "plastic")
            selected_activity = request.form.get("activity", "recycle")
            try:
                amount = max(0.0, float(request.form.get("amount", "0")))
            except ValueError:
                amount = 0.0

            if selected_waste not in WASTE:
                selected_waste = "plastic"
            if selected_activity not in ACTIVITY:
                selected_activity = "recycle"
            if selected_activity == "compost" and selected_waste != "organic":
                selected_activity = "recycle"

            if amount <= 0:
                flash("berat harus lebih dari 0 kilo","error")
            else:
                result=calculate(selected_waste,selected_activity,amount)
                flash("sudah berhasil Woi","succes")
    return render_template("index.html", result=result, selected_waste=selected_waste,
                           selected_activity=selected_activity, amount=amount,
                           waste=WASTE, activities=ACTIVITY,
                           button_python=button_python, button_discord=button_discord)


#Keterampilan Dinamis
@app.route('/', methods=['POST'])
def process_form():
    button_python = request.form.get('button_python')
    button_discord = request.form.get('button_discord')
    return render_template('index.html', button_python=button_python,button_discord=button_discord)


if __name__ == "__main__":
    app.run(debug=True)
