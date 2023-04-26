import mysql.connector
 
# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "whatsapp_tracker"
)
cursor = mydb.cursor()

def storeWhatsAppToken(auth_key):
    sql = "INSERT INTO whats_authentication (name,auth_key,status) VALUES (%s, %s, %s)"
    val = ("Token", auth_key,1)
    cursor.execute(sql, val)
    mydb.commit()

def deleteWhatsAppToken():
    sql = "DELETE FROM whats_authentication"
    cursor.execute(sql)
    mydb.commit()

def storeContactList(auth_key):
    sql = "INSERT INTO whats_authentication (name,auth_key,status) VALUES (%s, %s, %s)"
    val = ("Token", auth_key,1)
    cursor.execute(sql, val)
    mydb.commit()

def saveUserProfileInfo(data):
    sql = "INSERT INTO tbl_user_profile (name,phone_no,profile_photo,profile_bio,user_token,user_status) VALUES (%s, %s, %s,%s, %s, %s)"
    val = (data[0]['user_name'],'+918899007766',data[0]['user_photo'],'Hey I am using whatsapp!!!','$%2Sdfd756765757dfghgfh46466666$$@#$fhdfh567567657767757fdgdgdgg',1)
    cursor.execute(sql, val)
    user_id = cursor.lastrowid;
    mydb.commit()
    return user_id;

def saveContactList(data):
    sql = "INSERT INTO tbl_contact_list (contact_name,contact_photo,user_id,last_msg,online_status,contact_phone) VALUES (%s, %s, %s, %s,%s, %s)"
    val = (data[0]['contact_name'],data[0]['contact_photo'],data[0]['user_id'],"hello",data[0]['online_status'],data[0]['contact_phone'])
    cursor.execute(sql, val)
    mydb.commit()

def getUserProfileInfo(username):
    sql = "SELECT * from tbl_user_profile WHERE name='"+username+"'"
    cursor.execute(sql)
    return cursor.fetchone()
# Printing the