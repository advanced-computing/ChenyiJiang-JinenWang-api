from flask import Flask, request, Response, jsonify, make_response
import pandas as pd
import csv
import io

app = Flask(__name__)

# 加载 CSV 数据到 Pandas DataFrame
# 假设你的文件名为 data.csv
df = pd.read_csv('data.csv')

@app.route('/')
def index():
    return "Welcome to my API! Check the README for usage."


@app.route('/data', methods=['GET'])
def list_records():
    # 1. 复制数据
    results = df.copy()

    # 2. 智能过滤 (基于你的 loans_A_labeled.csv)
    # 遍历 URL 里的所有参数 (比如 ?country=Peru&sector=Food)
    for key, value in request.args.items():
        # 跳过控制参数，只处理数据列名
        if key in ['limit', 'offset', 'format']:
            continue
            
        # 只有当参数名确实是 CSV 里的列名时才过滤
        if key in results.columns:
            # 核心技巧：把 DataFrame 这一列临时转成字符串 (astype(str)) 再对比
            # 这样既能处理文本 (Peru)，也能处理数字 (575)，不会报错
            results = results[results[key].astype(str) == value]

    # 3. 分页 (Pagination)
    try:
        limit = int(request.args.get('limit', 10000)) # 默认给个大数，或者默认10
        offset = int(request.args.get('offset', 0))
    except ValueError:
        limit = 10000
        offset = 0
    
    # 检查切片是否越界，虽然 Python 切片越界不会报错，但逻辑上要注意
    if offset < len(results):
        results = results[offset : offset + limit]
    else:
        results = results[0:0] # 如果 offset 太大，返回空

    # 4. 格式化输出 (CSV / JSON)
    output_format = request.args.get('format', 'json').lower()

    if output_format == 'csv':
        return Response(
            results.to_csv(index=False),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=data.csv"}
        )
    else:
        # JSON 格式
        return Response(results.to_json(orient='records'), mimetype='application/json')
    

@app.route('/data/<id>', methods=['GET'])
def get_record(id):
    # 假设 ID 列名为 'id'，请根据你的 CSV 实际列名修改
    # 注意类型转换：如果 CSV 里 id 是数字，需要把 url 里的 id 转为 int
    try:
        # 尝试将 ID 转为与 DataFrame 一致的类型 (通常是 int)
        lookup_id = int(id)
    except ValueError:
        lookup_id = id
        
    record = df[df['id'] == lookup_id]
    
    if record.empty:
        return jsonify({"error": "Record not found"}), 404
    
    # 返回单条记录的 JSON
    return Response(record.to_json(orient='records'), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)