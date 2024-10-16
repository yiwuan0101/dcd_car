from bs4 import BeautifulSoup
from selenium import webdriver
import time
import openpyxl

def changes(row):
    row_current = {
        58451 : '0',
        58685: '1',
        58352: '2',
        58402: '3',
        58412: '4',
        58524: '5',
        58411: '6',
        58622: '7',
        58696: '8',
        58568: '9',
    }
    new_current = ''
    for i in row:
        try:
            pro_current = row_current[ord(i)]
        except:
            pro_current = i
        new_current = new_current+pro_current

    return new_current


workbook = openpyxl.Workbook()
sheet = workbook.active
workbook.save('cardi_test.xlsx')
for j in range(40):
    try:
        driver = webdriver.Firefox()
        url = f'https://www.dongchedi.com/usedcar/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-1-{j}-x-x-x-x-x'

        # time.sleep(3)
        driver.get(url)

        # 使用浏览器隐式等待3秒
        # driver.implicitly_wait(2)

        chushi = driver.page_source  # 通过浏览器 解析获取网页信息
        soup = BeautifulSoup(chushi, 'html.parser')

        kuais = soup.select('#__next > div.tw-flex > div.new-main.new > div > div > div.jsx-2898915557.wrap > ul > li')
        for okuai in kuais:
        #     # print(okuai.text)
        #     # print('\n')
            car_link = 'https://www.dongchedi.com'+okuai.a['href']
            # print(car_link)

        # car_link = 'https://www.dongchedi.com/usedcar/14525346'
            driver.get(car_link)
            # driver.implicitly_wait(3)

            in_edge = driver.page_source
            in_soup = BeautifulSoup(in_edge, 'html.parser')
            car_name = in_soup.find('span', {'class':'jsx-1166026127 line-1 tw-flex-1'}).text
            car_name = car_name.split(' ')[0]
            print(car_name)

            xqkuais = in_soup.find_all('p',{'class':'car-archives_value__3YXEW'})
            up_place = xqkuais[0].text
            source_car = xqkuais[1].text
            fre = xqkuais[2].text
            fre = fre[0:1] # 取次数前的数字，如0次取0
            up_data = xqkuais[3].text
            up_data = up_data.replace('年','-').replace('月','-01') #数据清洗，将其转为data格式
            displacement = xqkuais[4].text
            displacement = displacement.replace('L', '').replace('T', '')
            gearbox = xqkuais[5].text
            maintenance = xqkuais[6].text
            out_color = xqkuais[7].text
            in_color = xqkuais[8].text
            current = in_soup.find('p', {'class':'jsx-1166026127 tw-text-color-red-500 tw-font-semibold tw-text-20 xl:tw-text-24 tw-leading-32 xl:tw-leading-36 font-zmQZz5CrbrbHudeQ'}).text
            current = changes(current) # 对数据使用changes函数字体解密
            current = current.replace('','') #替掉价格中的汉字
            guide_price = in_soup.find('p',{'class':'jsx-1166026127 tw-text-color-gray-800'}).text
            guide_price = guide_price.replace('新车指导价：','').replace('万','')
            # kils = in_soup.find_all('p', {'class': 'jsx-1166026127 tw-text-14 tw-leading-22'})
            # print(kils)
            # kil = kils[1].text
            # print(kils[1])
            kil = driver.find_element(by='xpath',value='//*[@id="__next"]/div/div[2]/div/div[2]/div[2]/div[5]/div/div[2]/p[1]').text
            kil = changes(kil)
            kil = kil.replace('','')
            workbook = openpyxl.load_workbook('cardi_test.xlsx')
            sheet = workbook.active
            sheet = workbook['Sheet']
            sheet.append([car_name,up_data, up_place,source_car,fre,displacement,gearbox,maintenance,out_color,in_color,current, guide_price, kil])
            workbook.save('cardi_test.xlsx')
            # print(up_place)
            # print(source_car)
            # print(fre)
            # print(up_data)
            # print(displacement)
            # print(gearbox)
            # print(maintenance)
            # print(out_color)
            # print(in_color)
            # print(current)
            # print(guide_price)
            # print(kil)

        time.sleep(2)


    finally:
        driver.quit()