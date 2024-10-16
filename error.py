from pywebio.output import *
from pywebio.session import *

def page_error():
    run_js("""
    document.body.style.backgroundImage = "url('https://s2.loli.net/2024/09/11/DVbcPGqJYO2jH6v.jpg')";
    document.body.style.backgroundSize = "cover";
    """)
    toast('账号或密码错误')
    put_buttons(['重新登陆'],[lambda: go_app('index',False)]).style("position:absolute; top:50px ;right:700px;")

if __name__ == '__main__':
    page_error()
