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
