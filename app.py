from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)

# Dimensions de la toile
toile_largeur, toile_hauteur = 50, 50

def lire_toile_a_partir_des_cookies():
    toile = request.cookies.get("toile")
    if toile:
        return [list(map(str, ligne.split(","))) for ligne in toile.split(";")]
    else:
        return [["white" for _ in range(toile_largeur)] for _ in range(toile_hauteur)]

@app.route("/")
def index():
    toile = lire_toile_a_partir_des_cookies()
    return render_template("index.html", toile=toile)

@app.route("/mettre_pixel", methods=["POST"])
def mettre_pixel():
    x = int(request.form["x"])
    y = int(request.form["y"])
    couleur = request.form["couleur"]

    toile = lire_toile_a_partir_des_cookies()
    toile[y][x] = couleur

    response = make_response(jsonify({"status": "success"}))
    response.set_cookie("toile", ";".join([",".join(ligne) for ligne in toile]))
    return response

if __name__ == "__main__":
    app.run(debug=True)
