from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# 数据库连接（直接用）
def get_db():
    return mysql.connector.connect(
        host='8.137.92.155',
        port=4306,
        user='fly_app_user',
        password='Flyappuser@321',
        database='fly_mysql'
    )

# 1. 用户消费统计
@app.route('/api/user-stats')
def user_stats():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT
        users.id,
        users.username,
        COUNT(orders.id) AS order_count,
        IFNULL(SUM(orders.total_price), 0) AS total_spent
    FROM users
    LEFT JOIN orders ON users.id = orders.user_id
    GROUP BY users.id, users.username
    ORDER BY total_spent DESC
    """
    cursor.execute(sql)
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(results)

# 2. 商品销量排行
@app.route('/api/product-rankings')
def product_rankings():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT
        products.name,
        products.price,
        products.stock,
        IFNULL(SUM(orders.quantity), 0) AS sold_quantity,
        IFNULL(SUM(orders.total_price), 0) AS revenue
    FROM products
    LEFT JOIN orders ON products.id = orders.product_id
    GROUP BY products.id, products.name, products.price, products.stock
    ORDER BY sold_quantity DESC
    """
    cursor.execute(sql)
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(results)

# 3. 单个用户的订单详情
@app.route('/api/user-orders/<int:user_id>')
def user_orders(user_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT
        orders.id AS order_id,
        products.name AS product_name,
        orders.quantity,
        orders.total_price,
        orders.order_date
    FROM orders
    INNER JOIN products ON orders.product_id = products.id
    WHERE orders.user_id = %s
    ORDER BY orders.order_date DESC
    """
    cursor.execute(sql, (user_id,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
