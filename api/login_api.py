from flask import *
from extensions import *
from config import *

login_api = Blueprint('login_api', __name__, template_folder='templates')

@login_api.route('/api/login/<username>', methods=['GET'])
def login_route(username):
    db = connect_to_database()
    sql = "SELECT * FROM User WHERE username = '" + username + "';"
    cur = db.cursor()
    cur.execute(sql)
    user_info = cur.fetchall()
    # if not user_info:
    #     sql = "INSERT INTO User (username, firstName, lastName, accountType) VALUES ('" + username + "','" + firstName + "','" + lastName + "', 1)"
    #     print(sql)
    #     cur2 = db.cursor()
    #     cur2.execute(sql)
    #     sql = "SELECT * FROM User WHERE username = '" + username + "';"
    #     cur = db.cursor()
    #     user_info = cur.execute(sql)
    #session["logged_in"] = True

    user_information = {
        "userID": user_info[0]["userID"],
        "username": user_info[0]["username"],
        "firstName": user_info[0]["firstName"],
        "lastName": user_info[0]["lastName"],
        "phone": user_info[0]["phone"],
        "accountType": user_info[0]['accountType'],
    }

    return jsonify(user_information)

@login_api.route('/api/login', methods=['POST'])
def login_post_route():
    db = connect_to_database()
    dataObject = request.get_json()
    cur = db.cursor()
    user_info = cur.execute("SELECT * FROM User WHERE username = '" + dataObject['username'] + "';")
    # if user has never logged in before, add user info to database
    if not user_info:
        print("new user")
        cur2 = db.cursor()
        cur2.execute("INSERT INTO User (username, firstName, lastName, phone, accountType) VALUES ('" + dataObject['username'] + "','" + dataObject['firstName'] + "','" + dataObject['lastName'] + "','" + dataObject['phone'] + "', 1)")
    
    cur.execute("SELECT * FROM User WHERE username = '" + dataObject['username'] + "';")
    user_info = cur.fetchall()
    print(user_info)
    user_information = {
        "userID": user_info[0]["userID"],
        "username": user_info[0]["username"],
        "firstName": user_info[0]["firstName"],
        "lastName": user_info[0]["lastName"],
        "phone": user_info[0]["phone"],
        "accountType": user_info[0]['accountType'],
    }
    return jsonify(user_information)

@login_api.route('/api/login', methods=['PUT'])
def login_put_route():
    print("PUT")
    db = connect_to_database()
    dataObject = request.get_json()
    cur = db.cursor()
    cur.execute("UPDATE User SET firstName = %s, lastName = %s, phone = %s WHERE username = %s", 
        (dataObject['firstName'], dataObject['lastName'], dataObject['phone'], dataObject['username']))
    cur2 = db.cursor()
    cur2.execute("SELECT * FROM User WHERE username = '" + dataObject['username'] + "';")
    user_info = cur2.fetchall()
    user_information = {
        "userID": user_info[0]["userID"],
        "username": user_info[0]["username"],
        "firstName": user_info[0]["firstName"],
        "lastName": user_info[0]["lastName"],
        "phone": user_info[0]["phone"],
        "accountType": user_info[0]['accountType'],
    }
    return jsonify(user_information)