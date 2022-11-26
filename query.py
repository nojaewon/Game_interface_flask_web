import mysql.connector 

def search_password(cursor, _ID, _EMAIL):
    email = ""
    password = ""

    cursor.execute(f"select EMAIL, PASSWORD from USERACCOUNT where ACC_ID = '{_ID}';")
    for data in cursor:
        email = data[0]
        password = data[1]
    
    if email != _EMAIL:
        print("error: not matched email!")
        return
    
    print(f"password of {_ID} is {password}!")
    
    

if __name__ == "__main__":
    cnx = mysql.connector.connect(user='root', password='1234', host='127.0.0.1', database='maplestory') 
    cursor = cnx.cursor()

    # 비밀번호 출력
    search_password(cursor, "LOOK014", "LOOK0142NAVERR.COM")

    # 에러메시지 출럭
    search_password(cursor, "LOOK014", "helloworldNAVER.COM")
    
    cursor.close()
    cnx.close() 