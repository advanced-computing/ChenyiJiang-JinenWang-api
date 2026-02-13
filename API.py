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

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/data', methods=['GET'])
def list_records():
    # 1. 复制一份数据，以免修改原始数据
    results = df.copy()

    # 2. 过滤 (Filtering)
    # 遍历 URL 中的参数，如果在 CSV 列名中，就进行过滤
    for key, value in request.args.items():
        if key in results.columns:
            # 注意：这里的数据类型可能需要转换，CSV读取通常是数字，但URL参数是字符串
            # 为了简单起见，这里假设做字符串比较，或者你可以尝试转换类型
            results = results[results[key].astype(str) == value]

    # 3. 分页 (Pagination - Limit & Offset)
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    if limit:
        results = results[offset : offset + limit]
    else:
        results = results[offset:]

    # 4. 格式化输出 (Format: JSON vs CSV)
    output_format = request.args.get('format', 'json').lower()

    if output_format == 'csv':
        # 使用 Pandas 的 to_csv
        csv_output = results.to_csv(index=False)
        # 创建响应对象，设置正确的 Content-Type
        return Response(
            csv_output,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=data.csv"}
        )
    
    else: # 默认为 JSON
        # 使用 Pandas 的 to_json
        # orient='records' 会生成 [{"id":1...}, {"id":2...}] 的格式
        json_output = results.to_json(orient='records')
        return Response(json_output, mimetype='application/json')
    

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