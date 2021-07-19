import requests
import PySimpleGUI as sg
import pyautogui as pgui  # 欲しいFontがあったため
import csv

# 定数
ORDER_NAME = '-------------------------------------------'
BEVERAGE_LINE = '----------------------'
TEMPERATURE_LINE = '--------'
BEVERAGE_COUNT = 0
TEMPERATURE_COUNT = 0
LINE_MESSAGE = [' ','<ORDER>', '-', '-', '-']
API_TOKEN = ''
API_URL = ''

# csvファイルからapiトークンとurlを取得
with open('api_key.csv') as f:
    reader = csv.reader(f)
    tmp_ary = [row for row in reader]
    count = 0
    for data in tmp_ary[1]:   
        count += 1
        if count == 2:
            API_TOKEN = data
        elif count == 3:
            API_URL = data

# 関数定義
def order_name(name):
    if LINE_MESSAGE[2] != None:
        del LINE_MESSAGE[2]
    window['orderName'].update(ORDER_NAME)
    window['orderName'].update(name)
    LINE_MESSAGE.insert(2,name)
    pass

def order_beverage(beverage):  
    if LINE_MESSAGE[3] != None:
        del LINE_MESSAGE[3]
    window['orderBeverage'].update(BEVERAGE_LINE)
    LINE_MESSAGE.insert(3, beverage)
    window['orderBeverage'].update(beverage)
    pass

def order_temp(temperature):
    if LINE_MESSAGE[4] != None:
        del LINE_MESSAGE[4]
    window['orderTemp'].update(TEMPERATURE_LINE)
    LINE_MESSAGE.insert(4, temperature)
    window['orderTemp'].update(temperature)
    pass

def delete_elements():
    window['inputName'].update('')
    window['orderName'].update(ORDER_NAME)
    window['orderBeverage'].update(BEVERAGE_LINE)
    window['orderTemp'].update(TEMPERATURE_LINE)
    LINE_MESSAGE = [' ','<ORDER>', '-', '-', '-']
    pass

def pop_up(message):
    sg.popup(message, font=('Times New Roman', 14))

def send_line(notification_message):
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(API_URL, headers = headers, data=data)

# お気に入りのデザインテーマ
sg.theme('DarkAmber')

# ウィンドウ構成
layout = [ [sg.Text('Name',font=('Times New Roman',14)), 
            sg.InputText(default_text='', key='inputName',
                         size=(20,4),
                         font=('Times New Roman',14)),
            sg.Button('OK',key='nameOk',font=('Times New Roman', 14),size=(3,1))],
           [sg.Text('Beverage', font=('Times New Roman',14))],
           [sg.Button('CAFE LATTE', key='cafeLatte', 
                      font=('Times New Roman',14)), 
            sg.Button('BLACK', key='blackCoffee', 
                      font=('Times New Roman',14)), 
            sg.Button('CAFE AU LAIT', key='cafeAuLait', 
                      font=('Times New Roman',14))],
           [sg.Text('Temperature', font=('Times New Roman',14))],
           [sg.Button('COLD', key='ice', font=('Times New Roman',14)),
            sg.Button('HOT', key='hot', font=('Times New Roman',14))],
           [sg.Text('+++++++++++++++++')],
           [sg.Text('<order details>', font=('Times New Roman',14))],
           [sg.Text(ORDER_NAME, key='orderName')],
           [sg.Text(BEVERAGE_LINE, key='orderBeverage',
            font=('Times New Roman',14))],
           [sg.Text(TEMPERATURE_LINE, key='orderTemp',
                    font=('Times New Roman',14))],
           [sg.Text('+++++++++++++++++')],
           [sg.Button('ORDER', key='submit', font=('Times New Roman',14)),
            sg.Button('CANCEL', key='cancel', font=('Times New Roman',14))]        
         ]
window = sg.Window('Coffee order', layout)

# イベントループ
while True:
    count = 0
    event, values = window.Read()

    if event == sg.WIN_CLOSED:
        break
    
    if event == 'nameOk':
        count += 1
        order_name(values['inputName'])
        
    if event == 'cafeLatte':
        order_beverage('CAFE LATTE')
        BEVERAGE_COUNT += 1
    elif event == 'blackCoffee':
        order_beverage('BLACK COFFEE')
        BEVERAGE_COUNT += 1
    elif event == 'cafeAuLait':
        order_beverage('CAFE AU LAIT')
        BEVERAGE_COUNT += 1
    
    if event == 'ice':
        order_temp('COLD')
        TEMPERATURE_COUNT += 1
    elif event == 'hot':
        order_temp('HOT')
        TEMPERATURE_COUNT += 1
    
    if event == 'submit':
        # LINEにメッセージを送るが、何か要素を選択していなかったときに警告文を出す。
        if BEVERAGE_COUNT == 0 and TEMPERATURE_COUNT >= 1: 
            pop_up('Choice the beverage')
        elif BEVERAGE_COUNT >= 1 and TEMPERATURE_COUNT == 0:
            pop_up('Choice the temperature')
        elif BEVERAGE_COUNT == 0 and TEMPERATURE_COUNT == 0:
            pop_up('Choice the beverage, temperature')
        else:
            send_line('\r\n'.join(LINE_MESSAGE))         
            pop_up('Ordered.')
    
    if event == 'cancel':
        delete_elements()
        


window.close()