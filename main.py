from flask import Flask, render_template, redirect, request;
import mysql.connector 

app = Flask(__name__)
cnx = mysql.connector.connect(user='root', password='1234', host='127.0.0.1', database='maplestory') 
cursor = cnx.cursor()

personal_info_cache = {
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
    # 로그인되어 있으면 pick 창으로 리다이렉트
    # GET 방식일 때 로그인 화면 보여주기
    # 로그인 정보가 맞지 안으면 로그인 화면으로 다시 렌더
    # 로그인 정보가 맞으면 /pick 창으로 리다이렉트

    if personal_info_cache['acc_id'] is not None:
        return redirect('/pick')

    if request.method == 'POST':
        login_id = request.form['ID']
        login_password = request.form['PASSWORD']

        query = (f"""SELECT ACC_ID, NAME, EMAIL, PASSWORD
                    from USERACCOUNT
                    where ACC_ID = '{login_id}' and PASSWORD = '{login_password}'
                """)
        cursor.execute(query)

        for data in cursor:
            personal_info_cache['acc_id'] = data[0]
            personal_info_cache['email'] = data[1]
            personal_info_cache['name'] = data[2]
            personal_info_cache['password'] = data[3]

        if personal_info_cache['acc_id'] is None:
            print("NOT logged!")
            return render_template("login_page.html")
        
        print("logged!")
        return redirect('/pick')
    else:
        return render_template("login_page.html")


# 회원가입 화면
@app.route('/signup', methods=['POST', 'GET'])
def sign_page():
    if request.method == 'POST':
        signup_name = request.form['NAME']
        signup_id = request.form['ID']
        signup_email = request.form['EMAIL']
        signup_password = request.form['PASSWORD']

        query = (f"""
                INSERT INTO USERACCOUNT VALUES(
                    '{signup_id}',
                    '{signup_name}',
                    '{signup_email}',
                    '{signup_password}'
                );
                """)
        cursor.execute(query)
        cnx.commit()
        print('sign up!')
        return redirect('/login')
    else:
        return render_template('sign_page.html')

# 캐릭터 픽창
@app.route('/pick')
def pick_page():
    # 현재 계정의 유저 캐릭터들을 모두 조회(최대 4개 가정)
    # 각 계정의 유저 캐릭터의 STAT 정보 호출
    # 호출된 각 유저 캐릭터 정보는 템플릿 변수로 전송
    # 로그인되어 있지 않으면 로그인창(/login)으로 리다이렉트

    character_info_list = [None, None, None, None]
    
    if personal_info_cache['acc_id'] is None:
        return redirect("/login")
    
    query = (f"""
                select stat.character_id, job, stat._level
                from usercharacter
                join stat on usercharacter.character_id = stat.character_id 
                and usercharacter.acc_id = '{personal_info_cache['acc_id']}';
            """)

    cursor.execute(query)
    for idx, data in enumerate(cursor):
        character = {
            'name': data[0],
            'job' : data[1],
            'level' : data[2]
        }

        personal_info_cache['character_list'][idx] = character
    
    query = ("select * from JOBLIST;")
    cursor.execute(query)
    job_list = []
    for data in cursor:
        job_list.append(data[0])

    return render_template("pick_page.html", character_info_list=personal_info_cache['character_list'], acc_name=personal_info_cache['acc_id'], job_list = job_list)


# 캐릭터 세부 정보 조작
@app.route('/pick/<int:character_id>')
def detail_page(character_id):
    # 캐릭터 리스트는 0부터 시작, character_id는 1부터 시작
    # 따라서 리스트에서 받아오려면 1씩 빼주어야 한다.
    # 만들다보니까 이렇게 레거시가 되었지만 그냥 수정하지 않음

    # 해당 계정의 해당 캐릭터에 대한 인벤토리, 스킬셋, stat 정보를 모두 불러옴.
    # 로그인이 되지 않았으면 로그인창으로 리다이렉트
    # 모든 정보를 템플릿 변수를 통해 보여줌
    # character 리스트 캐시의 정보(name, job, level)를 활용한다.
    # 가져와야할 정보 1. 캐릭터가 가지고 있는 아이템과 아이템 TYPE from INVENTORY, ITEM
    # 가져와야할 정보 2. 캐릭터의 스탯 from STAT
    # 가져와야할 정보 3. 캐릭터의 스킬셋 from CHACRACTERSKILL
    # 가져와야할 정보 4. 캐릭터 생성시 직업 Select 폼을 위한 직업 리스트

    if personal_info_cache['acc_id'] is None:
        return redirect('/login')
    
    ch_acc = personal_info_cache['acc_id']
    ch_name = personal_info_cache['character_list'][character_id-1]['name']
    ch_level = personal_info_cache['character_list'][character_id-1]['level']
    ch_job = personal_info_cache['character_list'][character_id-1]['level']
    
    ch_str = 5
    ch_dec = 5
    ch_dec = 5
    ch_int = 5
    ch_luk = 5
    ch_hp = 100
    ch_mp = 100

    ch_skill_list = []
    ch_item_list = []

    query = (f"""
            select skill, skilllevel from CHARACTERSKILL
            where character_id = '{ch_name}';
        """)
    cursor.execute(query)

    for data in cursor:
        ch_skill_list.append({
            'skill_title': data[0],
            'skill_level': data[1]
        })
    
    query = (f"""
            select item.item_name, item_type
            from INVENTORY join ITEM
            on inventory.item_name = item.item_name and character_id='{ch_name}';
        """)
    cursor.execute(query)

    for data in cursor:
        ch_item_list.append({
            'item_name': data[0],
            'item_type': data[1]
        })
    
    query = (f"""
            select * from stat
            where character_id = '{ch_name}';
        """)
    cursor.execute(query)

    for data in cursor:
        ch_level = data[1]
        ch_str = data[2]
        ch_dec = data[3]
        ch_int = data[4]
        ch_luk = data[5]
        ch_hp = data[6]
        ch_mp = data[7]

    return render_template("detail_page.html", template = {
        '_idx' : character_id,
        '_acc' : ch_acc,
        '_name' : ch_name,
        '_level' : ch_level,
        '_job' : ch_job,
        '_str' : ch_str,
        '_dec' : ch_dec,
        '_int' : ch_int,
        '_luk' : ch_luk,
        '_hp' : ch_hp,
        '_mp' : ch_mp,
        '_item_list' : ch_item_list,
        '_skill_list' : ch_skill_list
    })

# 캐릭터 생성
@app.route('/create-character', methods=['POST', 'GET'])
def create_page():
    # 로그인이 안되어 있으면 로그인창으로 리다이렉트
    # POST method이면 request 입력폼의 정보들로 DB 해당 계정에서 캐릭터 생성
    # 캐릭터 생성 완료 후 해당 캐릭터의 DETAIL 페이지로 리다이렉트

    def isPossible_create_character():
        for character in personal_info_cache['character_list']:
            if character is None:
                return True
        return False

    if personal_info_cache['acc_id'] is None:
        return redirect('/login')
    
    if isPossible_create_character():
        if request.method == 'POST':
            ch_name = request.form['NAME']
            ch_job = request.form['JOB']

            query = (f'INSERT INTO USERCHARACTER VALUES("{ch_name}","{ch_job}","{personal_info_cache["acc_id"]}");')
            cursor.execute(query)

            query = (f'INSERT INTO STAT(CHARACTER_ID,_LEVEL) VALUES("{ch_name}",1);')
            cursor.execute(query)

            query = (f'INSERT INTO characterskill(CHARACTER_ID,SKILL) SELECT "{ch_name}",SKILL FROM SKILLLIST WHERE JOB="{ch_job}"')
            cursor.execute(query)
            cnx.commit()
    
    return redirect('/pick')




# 캐릭터 삭제
@app.route('/delete/<int:character_id>')
def delete_request(character_id):
    # 캐릭터 리스트는 0부터 시작, character_id는 1부터 시작
    # 따라서 리스트에서 받아오려면 1씩 빼주어야 한다.
    # 만들다보니까 이렇게 레거시가 되었지만 그냥 수정하지 않음
    # DB에서 삭제 완료후 (/pick)화면으로 리다이렉트
    # 삭제 완료시엔 personel_info_cache의 캐릭터 리스트에서도 제거해야함!
    if personal_info_cache['acc_id'] is None:
        return redirect('/login')

    query = (f"DELETE FROM USERCHARACTER WHERE CHARACTER_ID='{personal_info_cache['character_list'][character_id-1]['name']}';")
    cursor.execute(query)
    cnx.commit()
    personal_info_cache['character_list'][character_id-1] = None

    return redirect('/pick')

@app.route('/logout')
def logout_request():
    if personal_info_cache['acc_id'] is None:
        return redirect('/login')
    
    personal_info_cache['acc_id'] = None

    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)