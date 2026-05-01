from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Créer une base de données :
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recommandations.db"

db = SQLAlchemy(app)

class Recommandation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categorie = db.Column(db.String(50), nullable=False)
    sousCategorie = db.Column(db.String(50), nullable=False)
    public = db.Column(db.String(50), nullable=False)
    titre = db.Column(db.String(50), nullable=False)
    recommandation = db.Column(db.String(50), nullable=False)
    source = db.Column(db.String(50), nullable=False)

    # Convertir le model en JSON
    def to_dict(self):
        return {
            "id": self.id,
            "categorie": self.categorie,
            "sousCategorie": self.sousCategorie,
            "public": self.public,
            "titre": self.titre,
            "recommandation": self.recommandation,
            "source": self.source
        }
    
with app.app_context():
    db.create_all()



# Créer mes routes :

# Home
@app.route("/")
def home():
    return jsonify({"message":"Welcome to the Health recommandations API"})

# GET
@app.route("/api/recommandations", methods=["GET"])
def get_recommandations():
    categorie = request.args.get("categorie")
    sousCategorie = request.args.get("sousCategorie")
    public = request.args.get("public")

    query = Recommandation.query

    if categorie:
        query = query.filter_by(categorie=categorie)
    if sousCategorie:
        query = query.filter_by(sousCategorie=sousCategorie)
    if public:
        query = query.filter_by(public=public)

    recommandations = query.all()
    return jsonify([r.to_dict() for r in recommandations])

# Id
@app.route("/api/recommandations/<int:recommandation_id>", methods=["GET"])
def get_recommandation(recommandation_id):
    recommandation = Recommandation.query.get(recommandation_id)
    if recommandation :
        return jsonify(recommandation.to_dict())
    else :
        return jsonify({"error":"Recommandation not found !"}), 404
    
# POST
@app.route("/api/recommandations", methods=["POST"])
def add_recommandation():
    data = request.get_json()

    new_recommandation = Recommandation(categorie = data["categorie"],
                                        sousCategorie = data["sousCategorie"],
                                        public = data["public"],
                                        titre = data["titre"],
                                        recommandation = data["recommandation"],
                                        source = data["source"])

    db.session.add(new_recommandation)
    db.session.commit()

    return jsonify(new_recommandation.to_dict()), 201

# PUT 
@app.route("/api/recommandations/<int:recommandation_id>", methods=["PUT"])
def update_recommandation(recommandation_id):
    data = request.get_json()

    recommandation = Recommandation.query.get(recommandation_id)
    if recommandation :
        recommandation.categorie = data.get("categorie", recommandation.categorie)
        recommandation.sousCategorie = data.get("sousCategorie", recommandation.sousCategorie)
        recommandation.public = data.get("public", recommandation.public)
        recommandation.titre = data.get("titre", recommandation.titre)
        recommandation.recommandation = data.get("recommandation", recommandation.recommandation)
        recommandation.source = data.get("source", recommandation.source)

        db.session.commit()

        return jsonify(recommandation.to_dict())
    
    else :
        return jsonify({"error":"Recommandation not found !"}), 404
    
# DELETE
@app.route("/api/recommandations/<int:recommandation_id>", methods=["DELETE"])
def delete_recommandation(recommandation_id):
    recommandation = Recommandation.query.get(recommandation_id)
    if recommandation :
        db.session.delete(recommandation)
        db.session.commit()

        return jsonify({"message":"recommandation was deleted !"})
    
    else :
        return jsonify({"error":"Recommandation not found !"}), 404


if __name__ == "__main__":
    app.run(debug=True)