'''
    Notes:
        https://stackoverflow.com/questions/12193013/flask-python-trying-to-return-list-or-dict-to-ajax-call
'''

from flask import Flask, render_template
from flask import jsonify
import os
from flask import request
import time    

app = Flask(__name__)

#app.register_blueprint()

import base64
import sys
import codecs
import MySQLdb


def get_db():
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="test",         # your username
                     passwd="test",  # your password
                     db="test")        # name of the data base
    
    return db
    
def get_db_cursor():
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="test",         # your username
                     passwd="test",  # your password
                     db="test")        # name of the data base    

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    return db.cursor()


'''
    Add Github
'''
def add_github(db, github_link, admin_notes=None):
    
    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    time_now = time.strftime('%Y-%m-%d %H:%M:%S')
    
    #
    sql = "INSERT INTO TP_GITHUB_ANALYZER (GITHUB_LINK, ADMIN_NOTES, ADDED_DATE) VALUES (%s, %s, %s)"
    values = (github_link, admin_notes, time_now)

    # Use all the SQL you like
    cur.execute(sql, values)

    db.commit()

    print('Done : '+str(cur.rowcount)+" inserted") 

'''
    Read Github
'''
def read_github(db):
    
    cur = db.cursor()
    
    # Use all the SQL you like
    cur.execute("SELECT * FROM TP_GITHUB_ANALYZER")   

    # print all the first cell of all the rows
    counter = 0;
    github_list = []
    for row in cur.fetchall():
        try:
            counter = counter + 1

            github_dict = {}
        
            github_dict['gid'] = str(row[0])
            github_dict['github_link'] = str(row[1])
            github_dict['added_date'] = str(row[2])
            github_dict['updated_date'] = str(row[3])
            github_dict['admin_notes'] = str(row[4])

            github_list.append(github_dict)        
            
            print(github_dict)

        except ValueError as error:
            print('Error', format(error))

    return github_list

'''
    Add City
'''
def add_city(db, name, state, country):
    
    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()
    
    #
    sql = "INSERT INTO CITY (NAME, STATE, COUNTRY) VALUES (%s, %s, %s)"
    values = (name, state, country)

    # Use all the SQL you like
    cur.execute(sql, values)

    db.commit()

    print('Done : '+str(cur.rowcount)+" inserted") 
    
    
'''
    Update City
'''    
def update_city(db, name, state, country, id):
    
    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()
    
    #
    sql = "UPDATE CITY SET NAME = %s, STATE = %s, COUNTRY = %s WHERE ID = %s"
    values = (name, state, country, id)

    # Use all the SQL you like
    cur.execute(sql, values)

    db.commit()

    print('Done : '+str(cur.rowcount)+" updated") 


'''
    Delete City
'''    
def delete_city(db, id):
    
    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()
    
    #
    sql = "DELETE FROM CITY WHERE ID = %s"
    values = (id, )

    # Use all the SQL you like
    cur.execute(sql, values)

    db.commit()
    
    if(cur.rowcount == 0):
        raise Exception("Item Not Available to Delete")
    
    if(cur.rowcount > 1):
        raise Exception("More than one item deleted")

    print('Done : '+str(cur.rowcount)+" deleted")            


'''
    Read City
'''
def read_city(db):
    
    cur = db.cursor()
    
    # Use all the SQL you like
    cur.execute("SELECT * FROM city")   

    # print all the first cell of all the rows
    counter = 0;
    city_list = []
    for row in cur.fetchall():
        try:
            counter = counter + 1

            city_dict = {}
        
            pid = str(row[0])
            name = str(row[1])
            state = str(row[2])
            country = str(row[3])

            city_dict['pid'] = pid
            city_dict['name'] = name
            city_dict['state'] = state
            city_dict['country'] = country

            city_list.append(city_dict)
        
            #print(pid + " - " +  name + " - " + state + " - "+country)            
            print(city_dict)
        except ValueError as error:
            print('Error', format(error))

    return city_list


@app.route("/")
def hello():
    return render_template('index.html')

'''
    Get Cities

    possible urls:
        http://localhost:5000/get/cities
'''
@app.route("/get/cities")
def get_cities():

    db = get_db()

    c_list = read_city(db)

    return jsonify(c_list)

    #return "Hello World 2"

'''
    Add Github

    possible urls:
        http://localhost:5000/add/github
'''
@app.route("/add/github")
def add_github_rest():

    db = get_db()

    g_link  = request.form.get('link')    

    add_github(db, g_link, None)

    return "added"

'''
    Add Github View

    possible urls:
        http://localhost:5000/add/github/view
'''
@app.route("/add/github/view", methods=['POST'])
def add_github_view():

    db = get_db()

    g_link  = request.form.get('link')    

    add_github(db, g_link, None)

    result = {
        'apiresult' : 0,
        'apimessage': 'ok'
    }       
    
    return render_template('add-result.html', result=result)
    

'''
    Get Github links

    possible urls:
        http://localhost:5000/get/github/links
'''
@app.route("/get/github/links")
def get_github_links():

    db = get_db()

    github_list = read_github(db)

    return jsonify(github_list)


'''
    Get Github links view

    possible urls:
        http://localhost:5000/get/github/links/view
'''
@app.route("/get/github/links/view")
def get_github_links_view():

    db = get_db()

    github_list = read_github(db)

    g_list_json = (github_list)    

    result = {
        'apiresult' : 0,
        'apimessage': 'ok',
        'apivalue' : g_list_json
    }       
    
    return render_template('view-links.html', result=result)    



if __name__ == "__main__":
    
    app.config['city'] = 'Toronto'
    
    host = os.environ.get('IP', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host= host, port = port, use_reloader = False)