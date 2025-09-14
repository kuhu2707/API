#Task 2: Use Postman to send a POST request with JSON data to your local Flask app.
#Task 3: Build GET, POST, PUT, DELETE Flask API and test it on Postman.


from flask import Flask , request , jsonify
import json
import sqlite3

app=Flask(__name__)

# books_list=[ 
#     {
#         "id":0,
#         "author":"kuhu",
#         "language":"hindi",
#         "title":"singham",
#     },
#     {
#         "id":1,
#         "author":"pihu",
#         "language":"english",
#         "title":"fight",
#     },
#     {
#         "id":3,
#         "author":"jay",
#         "language":"tamil",
#         "title":"book12",
#     },
#     {
#         "id":4,
#         "author":"rajat",
#         "language":"marathi",
#         "title":"kite",
#     },
#     {
#         "id":5,
#         "author":"shweta",
#         "language":"japanese",
#         "title":"fairy-tales",
#     },
#     {
#         "id":6,
#         "author":"kajol",
#         "language":"hindi",
#         "title":"things fall for",
#     },
    
# ]
#---------for db connection -----------
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/books' , methods=["GET" , "POST"])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == "GET":   #localhost:5000/books but do this after post
        cursor = conn.execute("SELECT * FROM Book")
        books = [
            dict(id=row[0] , author=row[1] , language=row[2] , title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)
        
    if request.method == "POST":                #localhost:5000/books and give title , author and lang in form-data 
        new_author = request.form["author"]
        new_lang = request.form["language"]
        new_title = request.form["title"]
        sql="""INSERT INTO Book (author , language , title) VALUES (? ,? , ?)"""
        cursor.execute(sql,(new_author , new_lang , new_title))
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created successfully"
            
            
@app.route('/book/<int:id>' , methods=["GET" , "PUT" , "DELETE"])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None 
    
    if request.method == "GET":
        cursor.execute("SELECT * FROM Book WHERE id=?" , (id,))
        rows=cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book) , 200
        else:
            return "Something wrong" , 404
        
    if request.method == "PUT":
        sql = """UPDATE Book SET title=? , author = ? , language=?  WHERE id=?"""
        
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        updated_book={
            "id":id,
            "author":author,
            "language":language,
            "title":title
        }
        conn.execute(sql , (title , author , language ,id ))
        conn.commit()
        return jsonify(updated_book)
    
    if request.method == "DELETE":
        sql="""DELETE FROM Book WHERE id=?"""
        conn.execute(sql , (id,))
        conn.commit()
        return "The Book with id: {} has been deleted ".format(id) , 200
        


if __name__ == "__main__":
    app.run(debug=True)
    
  