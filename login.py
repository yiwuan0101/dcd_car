from error import *
from car_data_analyze import *
from admin_logined import *
from user_logined import *
from admin_login import *


def shuru_login():
    user_id = 0
    user_password = ''
    inputs = input_group('登陆', [
    input('账号', type=TEXT, name='user_id', required=True),
    input('密码', type=PASSWORD, name='user_password', required=True),
    actions( buttons=[
        {'label': '登陆', 'value': 'save'},
        {'label': '重置', 'type': 'reset', 'color': 'warning'},
    ], name='action'),
])
    return inputs


def chuli_login():
    val = shuru_login()
    globals().update(val)

    return user_id, user_password

def check_user():
    run_js("""
    document.body.style.backgroundImage = "url('https://s2.loli.net/2024/09/11/DVbcPGqJYO2jH6v.jpg')";
    document.body.style.backgroundSize = "cover";
    """)

    put_row([
        None,
        put_html(
            '<div style="text-align: center; color: #008080; font-weight: 700"> <h1> 懂车帝车辆信息管理系统 </h1> </div>'),
        None
    ], size='28% 44% 28%')

    put_button(label='管理员登陆',onclick=lambda :go_app('check_admin',False)).style("position:absolute; top:50px ;right:10px;")
    run_js("""
        var buttons = document.getElementsByTagName('button');
        buttons[0].style.backgroundColor = 'rgba(33, 150, 243, 0.5)'; 
        buttons[0].style.color = 'white';
    """)

    val = chuli_login()
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')
    cursor = con.cursor()
    sql_ad = "select user_id,user_password,user_name from users where user_id = '%s'and user_password = '%s';" %(user_id,user_password)

    cursor.execute(sql_ad)
    con.commit()
    result = cursor.fetchall()
    # print(result)
    # print(result[0][0])
    # print(result[0][1])
    # print(user_id)
    # print(user_password)
    # print(type(result[0][0]))
    # print(type(result[0][1]))
    # print(type(user_id))
    # print(type(user_password))
    if result is None or len(result) == 0:
        toast('账号或密码错误')
        # print("失败")
        go_app('page_error',False)

    elif result[0][2] is not None:
        go_app('main_root',False)

    elif result[0][0]==user_id and result[0][1]==user_password:
        toast('登陆成功')
        # print("成功")
        go_app('page_2',False)
    else:
        toast('操作错误')
        # print("操作失败")
        go_app('page_error',False)

    return 0



if __name__ == '__main__':
    start_server({'index': check_user, 'page_1': page_1, 'page_2': main_users, 'page_error': page_error,'main_root': main_root,'check_admin':check_admin,}, auto_open_webbrowser=True)
    # check_user()