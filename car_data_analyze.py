from dcd_chart import *

from pywebio import start_server
from pywebio.output import put_row, put_buttons, put_column
from pywebio.session import go_app
from pywebio.output import *

def page_1():
    put_row([
        None,
        put_column([
            put_row([
                put_buttons([
                    '市场分布', '汽车颜色', '热度分析', '汽车系列', '里程分析'
                ], [
                    lambda: used_car_market(),
                    lambda: color(),
                    lambda: heat(),
                    lambda: car_series(),
                    lambda: kmcount(),

                ])
            ], size='auto auto'),
            put_row([
                put_buttons([
                     '汽车年限', '排量分析', '电车市场', '保值率图','取消显示'
                ], [

                    lambda: car_time(),
                    lambda: car_turbo(),
                    lambda: car_ele(),
                    lambda: hedging_ratio(),
                    lambda: clear('pie_chart')
                ])
            ], size='auto auto')
        ], size='auto 100%'),
        None
    ], size='%30 %40 %30')
    put_button(label='返回',onclick=lambda:go_app('page_2',False)).style("position:absolute; top:20px ;right:30px;")

# if __name__ == '__main__':
#     page_1()