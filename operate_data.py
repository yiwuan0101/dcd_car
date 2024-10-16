from data_process import *
from unusual_process import *
from admin_logined import *
# 查找

def find_car():
    val = chuli3()
    car_name = val[0]
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')
    cursor = con.cursor()
    sql3 = f"select car_id,car_name,up_date,up_place,outer_colour,now_price,guide_price,km from dcd_car where car_name like '%{car_name}%';"

    try:
        cursor.execute(sql3)
        con.commit()
        result = cursor.fetchall()
        popup('查找', [put_table(result,
                                 header=['车号', '车名', '上牌日期', '上牌地点', '颜色', '当前价格(W)', '指导价(W)',
                                         '公里数(W)']), put_buttons(['关闭'], onclick=lambda _: close_popup())])
    except:
        tips_w()
    cursor.close()
    con.close()
    return 0


# 插入
def insert():
    val = shuru2()
    globals().update(val)
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')
    cursor = con.cursor()
    car_id1 = int(car_id)
    now_price1 = float(now_price)
    guide_price1 = float(guide_price)
    km1 = float(km)
    sql2 = "insert into dcd_car(car_id,car_name,up_date,up_place,outer_colour,now_price,guide_price,km) values ('%d','%s','%s','%s','%s','%f','%f','%f');" % (
        car_id1, car_name, up_date, up_place, outer_colour, now_price1, guide_price1, km1)
    try:
        cursor.execute(sql2)
        result = cursor.fetchall()
        con.commit()
        tips_c()
    except:
        tips_w()

    cursor.close()
    con.close()
    return 0


# 删除
def delete():
    val = chuli1()
    car_id = val
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')
    cursor = con.cursor()
    sql1 = "delete from dcd_car where car_id='%s';" % (car_id)
    try:
        cursor.execute(sql1)
        result = cursor.fetchall()
        con.commit()
        tips_c()
    except:
        tips_w()
    cursor.close()
    con.close()
    return 0


# 更新
def update():
    val = chuli2()
    car_id = val[0]
    car_name = val[1]
    up_date = val[2]
    up_place = val[3]
    outer_colour = val[4]
    now_price = val[5]
    guide_price = val[6]
    km = val[7]
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')
    cursor = con.cursor()
    car_id1 = int(car_id)
    now_price1 = float(now_price)
    guide_price1 = float(guide_price)
    km1 = float(km)
    sql4 = "update dcd_car set car_id='%s',car_name='%s',up_date='%s',up_place='%s',outer_colour='%s',now_price='%s',guide_price='%s',km='%s' where car_id='%s';" % (
        car_id1, car_name, up_date, up_place, outer_colour, now_price1, guide_price1, km1, car_id1)
    try:
        cursor.execute(sql4)
        result = cursor.fetchall()
        con.commit()
        tips_c()
    except:
        tips_w()
    return 0

# 刷新
def refresh():
    try:
        run_js('window.location.reload()')
        main_root()
        tips_c()
    except:
        tips_w()
    return 0