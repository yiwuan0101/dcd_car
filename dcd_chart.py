from pyecharts import options as o
from pyecharts.charts import Geo,Bar,WordCloud,Pie,Line
from pyecharts.globals import ChartType,ThemeType
import pymysql
from pywebio.output import *

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
