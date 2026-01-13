import pymysql

DB_NAME="Bachpankart"
TABLE_NAME="numbers_903x"


connection=pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="Tiger",
    database=DB_NAME
)

cursor=connection.cursor()

# for fetching the first untouched record automatically
cursor.execute(f"Select id from {TABLE_NAME} where is_on_whatsapp=2 order by id asc limit 1;")
start = cursor.fetchone()
start= start[0]-1
end=20

# lists for Whatsapp status updation 
# on_whatsapp=[]
# not_on_whatsapp=[]

# def printing_lists():
#     print("Numbers present on whatsapp: ", on_whatsapp)
#     print("Numbers not present on whatsapp: ", not_on_whatsapp)

def updateDB(on_whatsapp, not_on_whatsapp):
    print("Data updated successfully.")

# def updateDB(on_whatsapp, not_on_whatsapp):
#     print("Inside the updateDB function.")
#     print("On WhatsApp:", on_whatsapp)
#     print("Not On WhatsApp:", not_on_whatsapp)

#     # On Whatsapp
#     if on_whatsapp:
#         placeholders = ','.join(['%s'] * len(on_whatsapp))
#         query=f"UPDATE {TABLE_NAME} SET is_on_whatsapp = 1 WHERE phone IN ({placeholders});"
#         cursor.execute(query, on_whatsapp)
#         connection.commit()

#     # Not On Whatsapp
#     if not_on_whatsapp:
#         placeholders = ','.join(['%s'] * len(not_on_whatsapp))
#         query=f"UPDATE {TABLE_NAME} SET is_on_whatsapp = 0 WHERE phone IN ({placeholders});"
#         cursor.execute(query, not_on_whatsapp)
#         connection.commit()
#     print("All the updation is completed successfully")
#     # on_whatsapp=[]
#     # not_on_whatsapp=[]

print(f"fetching from {start}")

try:
    cursor.execute(f"Select phone from {TABLE_NAME} order by phone asc limit {start}, {end};")
    start+=end

    result=cursor.fetchall()

    numbers = [str(row[0]) for row in result]
    print(f" to {start}")
    print(numbers)
    print(f"Count is: {len(numbers)}")
except:
    print("Error occured")

exports=numbers
