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
    def add_product(self):
        data = request.json
        if 'name' in data and 'price' in data :
            product = Produto(name=data["name"],price=data["price"],description=data.get("description",""))
            db.session.add(product)
            db.session.commit()
            return jsonify({"message":"Product added with sucessfully."})
        return jsonify({"message":"Invalid product data"}),400
  
  
  
    @app.route('/api/product/delete/<int:product_id>',methods=["DELETE"])
    def delete_product(product_id):
        product = Produto.query.get(product_id)
        if product :
            db.session.delete(product)
            db.session.commit()
            return jsonify({"message":"Product deleteted sucessfully."})
        
        return jsonify({"message":"Product not found"}),404
    
    
    @app.route('/api/product/<int:product_id>',methods=["GET"])
    def get_produto_detail(product_id):
        produto = Produto.query.get(product_id)
        if produto:
            return jsonify ({
                "id": produto.id,
                "name":produto.name,
                "price":produto.price,
                "description":produto.description
            }) 
            
        return jsonify({"message":"Product not found"}),404
    
    
    @app.route('/api/products/update/<int:product_id>',methods=["PUT"])
    def update_product(product_id):
        product = Produto.query.get(product_id)
        if not product :
            return ({"message":"Product not found"}),404
        
        data = request.json
        if 'name' in data:
            product.name = data['name']
            
        if 'price' in data :
            product.price = data['price']
            
        if 'description' in data:
            product.description = data['description']
            
        db.session.commit()
        
        return ({"message":"Product update sucessfully."})
    
            
            
@app.route('/api/products',methods =["GET"])
def get_produtos():
    products = Produto.query.all()
    list_product = []
    for produto in products :
        product_data = {
            "id":produto.id,
            "name":produto.name,
            "price":produto.price,
            "description":produto.description
        } 
        
        list_product.append(product_data)
    return jsonify(list_product)
        
@app.route('/')
def hell_world():
    return 'Hello Word'


if __name__ =="__main__":
    app.run(debug=True)