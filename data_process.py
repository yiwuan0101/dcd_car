from pywebio import *
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import pymysql
# 输入输出处理
def shuru1():
    inputs = input_group(
        label='请输入车号',
        inputs=[
            input('车号:', name='car_id', type=TEXT),
        ])
    return inputs


def chuli1():
    val = shuru1()
    globals().update(val)
    return car_id


def shuru2():
    inputs = input_group(
        label='依次输入车号，车名，上牌日期，上牌地点，颜色，当前价格，指导价，公里数',
        inputs=[
            input('车号', name='car_id', type=TEXT),
            input('车名', name='car_name', type=TEXT),
            input('上牌日期', name='up_date', type=DATE),
            input('上牌地点', name='up_place', type=TEXT),
            input('颜色', name='outer_colour', type=TEXT),
            input('当前价格', name='now_price', type=TEXT),
            input('指导价', name='guide_price', type=TEXT),
            input('公里数', name='km', type=TEXT)
        ])
    return inputs


def chuli2():
    val = shuru2()
    globals().update(val)
    return  car_id, car_name, up_date, up_place, outer_colour, now_price, guide_price, km


def shuru3():
    inputs = input_group(
        label='请输入车名',
        inputs=[
            input('车名', name='car_name', type=TEXT)
        ])
    return inputs


def chuli3():
    val = shuru3()
    globals().update(val)
    return car_name