from  flask import Flask,request, json,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from sqlalchemy import  ForeignKey


app = Flask(__name__)
app.config['SECRET_KEY'] = "minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ecommerce.db"

# Para criar o banco sqlite:
# flask shell
#-> db.session.create_all()
#-> db.session.commit()
#-> Exit()
login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view ="login"
CORS(app)

#Modelagem

# Obs: Para criar um novo banco : flask shell -> db.drop_all() -> db.create_all() -> db.session.commit() -> exit()
# Para criar usuário pelo flask shell : flask shell -> user = User(username ="admin",password = "123") -> db.session.add(user) -> db.session.commit() -> exit()
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key = True)
    username=db.Column(db.String(80),nullable=False,unique=True)
    password = db.Column(db.String(80),nullable=True)
    cart = db.relationship('CartItem',backref='user',lazy=True)
    
class Produto(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text,nullable = True)
    
    
class CartItem(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey('user.id'),nullable=False)
    produto_id = db.Column(db.Integer,ForeignKey('produto.id'),nullable=False)

   
   #Autenticação
    @login_manager.user_loader
    def loader_user(user_id):
        return User.query.get(int(user_id))

    
    @app.route('/logout',methods=["POST"])
    @login_required
    def logout():
        logout_user()
        return jsonify({"message":"Logout sucessfully"})
    
    
    
    @app.route('/logout',methods=["POST"])
    @login_required
    def deslogar():
        logout_user()
        return jsonify({"message":"Logout sucessfully."})
        
    
    @app.route('/api/product/add',methods =["POST"])
    @login_required
    def add_product():
        data = request.json
        if 'name' in data and 'price' in data :
            product = Produto(name=data["name"],price=data["price"],description=data.get("description",""))
            db.session.add(product)
            db.session.commit()
            return jsonify({"message":"Product added with sucessfully."})
        return jsonify({"message":"Invalid product data"}),400
  
  
  
    @app.route('/api/product/delete/<int:product_id>',methods=["DELETE"])
    @login_required
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
    @login_required
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

@app.route('/login',methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username = data.get("username")).first()
    if user and data.get("password") == user.password :
        login_user(user)
        return jsonify({"message":"Logged sucessfully."})
    return jsonify({"message":"Unathorized. Invalid credentials."}),401

        
#Checkout
@app.route('/api/cart/add/<int:product_id>',methods=["POST"])
@login_required
def add_to_cart(product_id):
    user  = User.query.get(int(current_user.id))
    produto = Produto.query.get(product_id)
    if user and produto :
        cart_item = CartItem(user_id =user.id, produto_id=produto.id)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({"message":"Item adicionado no carrinho"})
    return jsonify({"message":"Falhou  ao adicionar no carrinho."}),400
    

@app.route('/api/cart/remove/<int:product_id>',methods = ["DELETE"])
@login_required
def remover_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id = current_user.id,produto_id = product_id).first()
    if cart_item :
         db.session.delete(cart_item)
         return jsonify({"message":"Item deletado do carrinho"})
    return jsonify({"message":"Falha ao deletar item do carrinho"})

if __name__ =="__main__":
    app.run(debug=True)