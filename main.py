from flask import Flask, render_template, redirect, request;
import mysql.connector 

app = Flask(__name__)
cnx = mysql.connector.connect(user='root', password='1234', host='127.0.0.1', database='maplestory') 
cursor = cnx.cursor()

personal_info_cash = {
    'acc_id' : None,
    'name': "",
    'email' : "",
    'password' : "",
    'character_list' : [None, None, None, None]
}

# 메인화면
@app.route('/')
def main_page():
    return redirect("/login")


# 로그인 화면
@app.route('/login', methods=['POST', 'GET'])
def login_page():
    # GET 방식일 때 로그인 화면 보여주기
    # 로그인 정보가 맞지 안으면 로그인 화면으로 다시 렌더
    # 로그인 정보가 맞으면 /pick 창으로 리다이렉트

    if request.method == 'POST':
        login_id = request.form['ID']
        login_password = request.form['PASSWORD']

        query = (f"""SELECT ACC_ID, NAME, EMAIL, PASSWORD
                    from USERACCOUNT
                    where ACC_ID = '{login_id}' and PASSWORD = '{login_password}'
                """)
        cursor.execute(query)

        for data in cursor:
            personal_info_cash['acc_id'] = data[0]
            personal_info_cash['email'] = data[1]
            personal_info_cash['name'] = data[2]
            personal_info_cash['password'] = data[3]

        if personal_info_cash['acc_id'] is None:
            print("NOT logged!")
            return render_template("login_page.html")    
        
        print("logged!")
        return redirect('/pick')
    else:
        return render_template("login_page.html")


# 캐릭터 픽창
@app.route('/pick')
def pick_page():
    # 현재 계정의 유저 캐릭터들을 모두 조회(최대 4개 가정)
    # 각 계정의 유저 캐릭터의 STAT 정보 호출
    # 호출된 각 유저 캐릭터 정보는 템플릿 변수로 전송
    # 로그인되어 있지 않으면 로그인창(/login)으로 리다이렉트

    character_info_list = [None, None, None, None]
    
    if personal_info_cash['acc_id'] is None:
        return redirect("/login")
    
    query = (f"""
                select stat.character_id, job, stat._level
                from usercharacter
                join stat on usercharacter.character_id = stat.character_id 
                and usercharacter.acc_id = '{personal_info_cash['acc_id']}';
            """)

    cursor.execute(query)
    for idx, data in enumerate(cursor):
        character = {
            'name': data[0],
            'job' : data[1],
            'level' : data[2]
        }

        personal_info_cash['character_list'][idx] = character

    return render_template("pick_page.html", character_info_list=personal_info_cash['character_list'])


# 캐릭터 세부 정보 조작
@app.route('/pick/<int:character_id>')
def detail_page(character_id):
    # 해당 계정의 해당 캐릭터에 대한 인벤토리, 스킬셋, stat 정보를 모두 불러옴.
    # 로그인이 되지 않았으면 로그인창으로 리다이렉트
    # 모든 정보를 템플릿 변수를 통해 보여줌
    # character 리스트 캐시의 정보(name, job, level)를 활용한다.
    # 가져와야할 정보 1. 캐릭터가 가지고 있는 아이템과 아이템 TYPE from INVENTORY, ITEM
    # 가져와야할 정보 2. 캐릭터의 스탯 from STAT
    # 가져와야할 정보 3. 캐릭터의 스킬셋 from CHACRACTERSKILL

    if personal_info_cash['acc_id'] is None:
        return redirect('/login')
    
    query = (f"""
            SELECT 

        """)
    cursor.execute(query)


    return render_template("detail_page.html")


if __name__ == "__main__":
    app.run(debug=True)