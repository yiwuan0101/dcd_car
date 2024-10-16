from data_process import *
from unusual_process import *
from operate_data import find_car

def main_users():
    # 背景图
    run_js("""
    document.body.style.backgroundImage = "url('https://s2.loli.net/2024/09/11/DVbcPGqJYO2jH6v.jpg')";
    document.body.style.backgroundSize = "cover";
    """)

    # 标题
    put_row([
        None,
        put_html(
            '<div style="text-align: center; color: #008080; font-weight: 700"> <h1> 懂车帝车辆信息管理系统 </h1> </div>'),
        None
    ], size='28% 44% 28%')

    # 按钮
    put_row([
        None,  # Left empty space to center
        # put_column([
        #
        # ], size='auto'),
        put_buttons(['查询',  '分析' , '退出'],
                    onclick=[lambda: find_car(),
                             lambda: go_app('page_1',False),
                             lambda:go_app('index',False)]),
        None  # Right empty space to center
    ], size='38% 50% 28%')  # Adjust these percentages to control the centering

    # 按钮样式
    run_js("""
        var buttons = document.getElementsByTagName('button');
        buttons[0].style.backgroundColor = 'rgba(33, 150, 243, 0.5)'; 
        buttons[0].style.color = 'white';
        buttons[1].style.backgroundColor = 'rgba(33, 150, 243, 0.5)'; 
        buttons[1].style.color = 'white';
        buttons[2].style.backgroundColor = 'rgba(33, 150, 243, 0.5)';  
        buttons[2].style.color = 'white';
        buttons[3].style.backgroundColor = 'rgba(33, 150, 243, 0.5)'; 
        buttons[3].style.color = 'white';
        buttons[4].style.backgroundColor = 'rgba(33, 150, 243, 0.5)'; 
        buttons[4].style.color = 'white';
        buttons[5].style.backgroundColor = 'rgba(33, 150, 243, 0.5)'; 
        buttons[5].style.color = 'white';
    """)

    pass

if __name__ == '__main__':
    main_users()