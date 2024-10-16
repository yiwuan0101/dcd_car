from login import *



def check_admin():
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

    put_button(label='用户登陆',onclick=lambda:go_app('index',False)).style("position:absolute; top:50px ;right:10px;")
    run_js("""
        var buttons = document.getElementsByTagName('button');
        buttons[0].style.backgroundColor = 'rgba(33, 150, 243, 0.5)'; 
        buttons[0].style.color = 'white';
    """)

    val = chuli_login()
    user_id = val[0]
    user_password = val[1]
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')
    cursor = con.cursor()
    sql_ad = "select user_id,user_password,user_name from users where user_id = '%s'and user_password = '%s';" %(user_id,user_password)

    cursor.execute(sql_ad)
    con.commit()
    result = cursor.fetchall()

    if result is None or len(result) == 0:
        toast('账号或密码错误')
        # print("失败")
        go_app('page_error',False)
    elif result[0][2] is None:
        toast('您不是管理员')
        # print("失败")
        go_app('page_error',False)
    else:
        go_app('main_root',False)

    pass

if __name__ == '__main__':
    check_admin()