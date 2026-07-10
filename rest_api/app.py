from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    available = db.Column(db.Boolean, default=True)

with app.app_context():
    db.create_all()

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': b.id, 
        'title': b.title, 
        'author': b.author, 
        'isbn': b.isbn, 
        'available': b.available
    } for b in books])

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(
        title=data.get('title'), 
        author=data.get('author'), 
        isbn=data.get('isbn')
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added', 'id': new_book.id}), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.available = data.get('available', book.available)
    db.session.commit()
    return jsonify({'message': 'Book updated'})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)