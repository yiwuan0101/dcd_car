from pywebio.output import *

# 异常处理
def show_msg():
    popup('误触请关闭', [put_text("不要回答不要回答不要回答!"), put_buttons(['关闭'], onclick=lambda _: close_popup())])


def tips_c():
    toast('操作成功', position='right', color='#2188ff', duration=0, onclick=show_msg)


def tips_w():
    toast('操作失败', position='right', color='#2188ff', duration=0, onclick=show_msg)