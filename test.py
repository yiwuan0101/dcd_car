# -*- coding: gbk -*-
import pymysql
from pywebio import *
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio import start_server
from pyecharts import options as o
from pyecharts.charts import Geo,Bar,WordCloud,Pie,Line
from pyecharts.globals import ChartType,ThemeType


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

    put_button(label='用户登陆', onclick=lambda: go_app('index', False)).style(
        "position:absolute; top:50px ;right:10px;")
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
    sql_ad = "select user_id,user_password,user_name from users where user_id = '%s'and user_password = '%s';" % (
    user_id, user_password)

    cursor.execute(sql_ad)
    con.commit()
    result = cursor.fetchall()

    if result is None or len(result) == 0:
        toast('账号或密码错误')
        # print("失败")
        go_app('page_error', False)
    elif result[0][2] is None:
        toast('您不是管理员')
        # print("失败")
        go_app('page_error', False)
    else:
        go_app('main_root', False)

    pass


def main_root():
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
        put_buttons(['查找', '插入', '删除', '更改', '刷新', '退出'],
                    onclick=[lambda: find_car(),
                             lambda: insert(),
                             lambda: delete(),
                             lambda: update(),
                             lambda: refresh(),
                             lambda: go_app('index', False)]),

        None  # Right empty space to center
    ], size='28% 44% 28%')
    # Adjust these percentages to control the centering

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
        buttons[6].style.backgroundColor = 'rgba(33, 150, 243, 0.5)'; 
        buttons[6].style.color = 'white';
    """)

    pass


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
                    '汽车年限', '排量分析', '电车市场', '保值率图', '取消显示'
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
    put_button(label='返回', onclick=lambda: go_app('page_2', False)).style("position:absolute; top:20px ;right:30px;")


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


# 可视化函数
def used_car_market():
    # 获取连接
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')

    # 查
    cursor = con.cursor()

    sql1 = "SELECT d.up_place,COUNT(*) from dcd_car d  GROUP BY d.up_place ORDER BY count(*) desc LIMIT 20;"

    cursor.execute(sql1)
    jieguos = cursor.fetchall()

    a = (
        Geo()
        .add_schema(maptype='china')
        .add('二手车市场量', jieguos,
             type_=ChartType.EFFECT_SCATTER)
        .set_series_opts(label_opts=o.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=o.VisualMapOpts,
            title_opts=o.TitleOpts(title='二手车市场分布图')
        )
    )

    # 在 PyWebIO 中显示图表
    with use_scope('pie_chart', clear=True):
        put_html(a.render_notebook())


def hedging_ratio():
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')

    # 查
    cursor = con.cursor()

    sql3 = '''SELECT 
        car_name, 
    		round((guide_price-now_price)/guide_price,3) AS baozhilv
    FROM
        dcd_car
    WHERE DATEDIFF(CURDATE(), STR_TO_DATE(CONCAT(up_date, '-01'), '%Y-%m-%d')) BETWEEN 365 and 365*2
    ORDER BY baozhilv desc
    LIMIT 10
    ;
    '''

    cursor.execute(sql3)
    baozhi = cursor.fetchall()

    car_names = [item[0] for item in baozhi]
    baozhilv_values = [item[1] for item in baozhi]

    # 创建柱状图
    b = (
        Bar(init_opts=o.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(car_names)  # 添加x轴数据（汽车名称）
        .add_yaxis("保值率", baozhilv_values, category_gap="80%")  # 添加y轴数据（保值率），设置柱子之间的间隔
        .set_global_opts(
            title_opts=o.TitleOpts(title="不同汽车的保值率情况"),
            yaxis_opts=o.AxisOpts(name="保值率"),
            xaxis_opts=o.AxisOpts(name="汽车名称", axislabel_opts={"rotate": 45})  # 旋转x轴标签，防止重叠
        )
        .set_series_opts(
            label_opts=o.LabelOpts(is_show=True, position="top")  # 在柱子顶部显示标签
        )
    )
    with use_scope('pie_chart', clear=True):
        put_html(b.render_notebook())


def heat():
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')
    cursor = con.cursor()

    sql4 = '''SELECT car_name,count(*)
        from dcd_car
        GROUP BY car_name
        ORDER BY count(*) desc
        limit 0,20;
        '''

    cursor.execute(sql4)
    brandsum = cursor.fetchall()

    # print(brandsum)

    w = (
        WordCloud()
        .add(series_name='热度', data_pair=brandsum, word_size_range=[23, 67])
        .set_global_opts(
            title_opts=o.TitleOpts(
                title='热度分析',
                title_textstyle_opts=o.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=o.TooltipOpts(is_show=True)
        )
    )
    with use_scope('pie_chart', clear=True):
        put_html(w.render_notebook())


def color():
    # 获取连接
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')

    # 查
    cursor = con.cursor()

    sql5 = '''SELECT outer_colour,count(*)
    from dcd_car
    GROUP BY outer_colour
    ORDER BY count(*) desc;

    '''

    cursor.execute(sql5)
    color = cursor.fetchall()

    # 准备数据
    colors = [item[0] for item in color]
    counts = [item[1] for item in color]

    # 创建玫瑰图
    p1 = (
        Pie(init_opts=o.InitOpts(theme=ThemeType.LIGHT))
        .add(
            series_name="汽车颜色分布",
            data_pair=[list(z) for z in zip(colors, counts)],
            radius=["30%", "75%"],  # 设置内径和外径
            label_opts=o.LabelOpts(is_show=True, position="outside")
        )
        .set_global_opts(
            title_opts=o.TitleOpts(title="不同颜色汽车的分布情况", pos_left="center", pos_top="50%")
        )
        .set_series_opts(
            tooltip_opts=o.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"),
            label_opts=o.LabelOpts(formatter="{b}: {c}")
        )
    )
    with use_scope('pie_chart', clear=True):
        put_html(p1.render_notebook())


def kmcount():
    # 获取连接
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')

    # 查
    cursor = con.cursor()

    sql6 = '''SELECT
    CASE 
    	WHEN km BETWEEN 0 and 3 THEN '00-03'
    	WHEN km BETWEEN 3 and 6 THEN '03-06'
    	WHEN km BETWEEN 6 and 9 THEN '06-09'
    	WHEN km BETWEEN 9 and 12 THEN '09-12'
    	WHEN km BETWEEN 12 and 15 THEN '12-15'
    	ELSE
    		'15+'
    END as km_group,count(*) as count
    from dcd_car 
    GROUP BY km_group
    order by km_group;
    '''

    cursor.execute(sql6)
    km_groups = cursor.fetchall()

    # 准备数据
    km_ranges = [item[0] for item in km_groups]
    counts = [item[1] for item in km_groups]

    # 创建折线图
    l = (
        Line(init_opts=o.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(km_ranges)
        .add_yaxis("汽车数量", counts, is_smooth=True)
        .set_global_opts(
            title_opts=o.TitleOpts(title="不同里程组的汽车数量分布"),
            xaxis_opts=o.AxisOpts(name="里程组"),
            yaxis_opts=o.AxisOpts(name="汽车数量")
        )
        .set_series_opts(
            label_opts=o.LabelOpts(is_show=True)
        )
    )
    with use_scope('pie_chart', clear=True):
        put_html(l.render_notebook())


def car_series():
    # 获取连接
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')

    # 查
    cursor = con.cursor()

    sql2 = '''SELECT
    CASE
         WHEN car_name like '%宝马%' THEN '宝马系列'
    	 WHEN car_name like '%奔驰%' THEN '奔驰系列'
    	 WHEN car_name like '%奥迪%' THEN '奥迪系列'
    	 ELSE '其他系列'
    END as brand,count(*) as count
    from dcd_car
    GROUP BY brand;'''

    cursor.execute(sql2)
    bba = cursor.fetchall()

    p = Pie()
    p.add('品牌', bba)
    with use_scope('pie_chart', clear=True):
        put_html(p.render_notebook())


def car_time():
    con = pymysql.connect(
        host='localhost',
        port=3306,
        db='car',
        user='root',
        password='021019lx'
    )

    # 查
    cursor = con.cursor()

    sql3 = '''# 过户次数为0次的市场二手车的使用时间情况
    SELECT case
    when DATEDIFF(CURDATE(),up_date) < 365 then '0-1年'
    when DATEDIFF(CURDATE(),up_date) < 365*2 then '1-2年'
    when DATEDIFF(CURDATE(),up_date) < 365*3 then '2-3年'
    when DATEDIFF(CURDATE(),up_date) < 365*4 then '3-4年'
    when DATEDIFF(CURDATE(),up_date) < 365*5 then '4-5年'
    when DATEDIFF(CURDATE(),up_date) < 365*6 then '5-6年'
    when DATEDIFF(CURDATE(),up_date) < 365*7 then '6-7年'
    when DATEDIFF(CURDATE(),up_date) < 365*8 then '7-8年'
    when DATEDIFF(CURDATE(),up_date) < 365*9 then '8-9年'
    else '9年以上' end as use_years,round(count(*)/1562,2) as percent
    from dcd_car
    where fre = 0
    GROUP BY use_years 
    ORDER BY use_years
    '''

    cursor.execute(sql3)
    nianxian = cursor.fetchall()

    keep_time = [item[0] for item in nianxian]
    kt = [item[1] for item in nianxian]

    # 创建柱状图
    t = (
        Bar(init_opts=o.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(keep_time)  # 添加x轴数据（持有时间）
        .add_yaxis("转手率", kt, category_gap="80%")  # 添加y轴数据（占有率），设置柱子之间的间隔
        .reversal_axis()  # 列转行
        .set_global_opts(
            title_opts=o.TitleOpts(title="各年限汽车转手情况"),
            yaxis_opts=o.AxisOpts(name="占有比率"),
            xaxis_opts=o.AxisOpts(name="年限", axislabel_opts={"rotate": 45})  # 旋转x轴标签，防止重叠
        )
        .set_series_opts(
            label_opts=o.LabelOpts(is_show=True, position="top")  # 在柱子顶部显示标签
        )
    )
    with use_scope('pie_chart', clear=True):
        put_html(t.render_notebook())


def car_turbo():
    # 获取连接
    con = pymysql.connect(
        host='localhost',
        port=3306,
        db='car',
        user='root',
        password='021019lx'
    )

    # 查
    cursor = con.cursor()

    sql5 = '''SELECT
      CASE
        WHEN turbo = 0 THEN '电车'
        ELSE '油车'
      END AS gp,
      CASE
    		when turbo = 0 then '0'
        WHEN turbo BETWEEN 0 and 1.5 THEN '<=1.5'
        WHEN turbo > 1.5 THEN '>1.5'
      END AS turbo_group,
      COUNT(*) AS count
    FROM dcd_car
    GROUP BY gp, turbo_group;
    '''

    cursor.execute(sql5)
    color = cursor.fetchall()

    # 准备数据
    turbo = [item[1] for item in color]
    counts = [item[2] for item in color]

    # 创建玫瑰图
    p = (
        Pie(init_opts=o.InitOpts(theme=ThemeType.LIGHT))
        .add(
            series_name="汽车排量占比",
            data_pair=[list(z) for z in zip(turbo, counts)],
            radius=["30%", "75%"],  # 设置内径和外径
            label_opts=o.LabelOpts(is_show=True, position="outside")
        )
        .set_global_opts(
            title_opts=o.TitleOpts(title="不同排量汽车的分布情况", pos_left="center", pos_top="50%"),
            legend_opts=o.LegendOpts(orient="vertical", pos_left="left")
        )
        .set_series_opts(
            tooltip_opts=o.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"),
            label_opts=o.LabelOpts(formatter="{b}: {c}")
        )
    )
    with use_scope('pie_chart', clear=True):
        put_html(p.render_notebook())


def car_ele():
    con = pymysql.connect(
        host='localhost',
        port=3306,
        db='car',
        user='root',
        password='021019lx'
    )

    # 查
    cursor = con.cursor()

    sql4 = '''SELECT car_name,count(*) as count
    from dcd_car
    WHERE case 
    	when turbo = 0 then "电车"
    	when turbo <> 0 then "油车"
    	end = "电车"
    GROUP BY car_name
    ORDER BY count desc;
    '''

    cursor.execute(sql4)
    brandsum = cursor.fetchall()

    w = (
        WordCloud()
        .add(series_name='热度', data_pair=brandsum, word_size_range=[23, 67])
        .set_global_opts(
            title_opts=o.TitleOpts(
                title='热度分析',
                title_textstyle_opts=o.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=o.TooltipOpts(is_show=True)
        )
    )
    with use_scope('pie_chart', clear=True):
        put_html(w.render_notebook())


def page_error():
    run_js("""
    document.body.style.backgroundImage = "url('https://s2.loli.net/2024/09/11/DVbcPGqJYO2jH6v.jpg')";
    document.body.style.backgroundSize = "cover";
    """)
    toast('账号或密码错误')
    put_buttons(['重新登陆'], [lambda: go_app('index', False)]).style("position:absolute; top:50px ;right:700px;")


def shuru_login():
    user_id = 0
    user_password = ''
    inputs = input_group('登陆', [
        input('账号', type=TEXT, name='user_id', required=True),
        input('密码', type=PASSWORD, name='user_password', required=True),
        actions(buttons=[
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

    put_button(label='管理员登陆', onclick=lambda: go_app('check_admin', False)).style(
        "position:absolute; top:50px ;right:10px;")
    run_js("""
        var buttons = document.getElementsByTagName('button');
        buttons[0].style.backgroundColor = 'rgba(33, 150, 243, 0.5)'; 
        buttons[0].style.color = 'white';
    """)

    val = chuli_login()
    con = pymysql.connect(host='localhost', port=3306, db='car', user='root', password='021019lx')
    cursor = con.cursor()
    sql_ad = "select user_id,user_password,user_name from users where user_id = '%s'and user_password = '%s';" % (
    user_id, user_password)

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
        go_app('page_error', False)

    elif result[0][2] is not None:
        go_app('main_root', False)

    elif result[0][0] == user_id and result[0][1] == user_password:
        toast('登陆成功')
        # print("成功")
        go_app('page_2', False)
    else:
        toast('操作错误')
        # print("操作失败")
        go_app('page_error', False)

    return 0


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


# 异常处理
def show_msg():
    popup('误触请关闭', [put_text("不要回答不要回答不要回答!"), put_buttons(['关闭'], onclick=lambda _: close_popup())])


def tips_c():
    toast('操作成功', position='right', color='#2188ff', duration=0, onclick=show_msg)


def tips_w():
    toast('操作失败', position='right', color='#2188ff', duration=0, onclick=show_msg)


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
        put_buttons(['查询', '分析', '退出'],
                    onclick=[lambda: find_car(),
                             lambda: go_app('page_1', False),
                             lambda: go_app('index', False)]),
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
    start_server(
        {'index': check_user, 'page_1': page_1, 'page_2': main_users, 'page_error': page_error, 'main_root': main_root,
         'check_admin': check_admin, }, auto_open_webbrowser=True)