from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbhomework  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분(화면보기)
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분_주문하기(post)
@app.route('/order', methods=['POST'])
def save_order():
    name_receive = request.form['name_give']
    product_receive = request.form['product_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']
    resolution_receive = request.form['resolution_give']

    # DB에 삽입할 doc 만들기
    doc = {
        'name': name_receive,
        'product': product_receive,
        'address': address_receive,
        'phone': phone_receive,
        'resolution': resolution_receive
    }

    # homework에  doc 저장하기
    db.homework.insert_one(doc)
    # 성공 여부
    return jsonify({'result': 'success'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def read_orders():
    # 1. DB에서 리뷰 정보 모두 가져오기
    orders = list(db.homework.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
