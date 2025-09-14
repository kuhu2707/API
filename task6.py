#TASK 6 - Create a Flask API that takes a number and returns its square via POST method.

from flask import Flask , request , jsonify

app=Flask(__name__)


@app.route("/square", methods =["POST"])
def square_number():
    try:
        data = request.get_json()
        number = data.get("number")
        if number is None:
            return jsonify("Error: 'number' is required")
    
        result = number ** 2
        return jsonify({"square": result})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    
    
    
if __name__ =="__main__":
    app.run(debug=True)