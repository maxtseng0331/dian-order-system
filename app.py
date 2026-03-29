from flask import Flask, render_template, request
from menu_data import menu

app = Flask(__name__)

# 全域變數：暫存已選擇的主食
current_order = []

@app.route('/')
def index():
    # 每次回到首頁時，清空購物車（這樣重新點餐才不會重複加在一起）
    global current_order
    current_order = []
    return render_template('index.html')

@app.route('/category/<type>')
def show_category(type):
    # 分類邏輯：篩選名稱包含「飯」或「麵」的項目
    filtered_menu = {name: info for name, info in menu.items() if type in name}
    return render_template('category.html', category=type, items=filtered_menu)

@app.route('/add_to_order', methods=['POST'])
def add_to_order():
    selected = request.form.getlist('dish')
    next_step = request.form.get('next_step')
    
    global current_order
    current_order.extend(selected)

    if next_step == 'continue':
        # 回到首頁讓你選另一個分類，但這次不經過 index() 以免清空訂單
        # 改用一個簡單的頁面或是直接 render 大按鈕
        return render_template('index.html') 
    else:
        # 前往加購區
        selected_menu_info = {name: menu[name] for name in current_order}
        return render_template('sides.html', selected_items=selected_menu_info)

@app.route('/checkout', methods=['POST'])
def checkout():
    mains = request.form.getlist('main_dishes')
    sides = request.form.getlist('side_dishes')
    
    main_total = sum(menu[m]['price'] for m in mains)
    side_total = len(sides) * 30 
    total = main_total + side_total
    
    # 這裡改成回傳剛才建立的 result.html
    return render_template('result.html', 
                           mains=mains, 
                           sides=sides, 
                           total_price=total, 
                           menu=menu) # 傳入 menu 才能在 HTML 抓主餐價格
if __name__ == '__main__':
    app.run(debug=True)