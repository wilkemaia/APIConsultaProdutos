from  flask import Flask,request, json,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ecommerce.db"

# Para criar o banco sqlite:
# flask shell
#-> db.session.create_all()
#-> db.session.commit()
#-> Exit()

db = SQLAlchemy(app)

#Modelagem
class Produto(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text,nullable = True)
    
    @app.route('/api/product/add',methods =["POST"])
    def add_product():
        data = request.json
        if 'name' in data and 'price' in data :
            product = Produto(name=data["name"],price=data["price"],description=data.get("description",""))
            db.session.add(product)
            db.session.commit()
            return jsonify({"message":"Product added with sucessfully."})
        return jsonify({"message":"Invalid product data"}),400
  
@app.route('/')
def hell_world():
    return 'Hello Word'


if __name__ =="__main__":
    app.run(debug=True)