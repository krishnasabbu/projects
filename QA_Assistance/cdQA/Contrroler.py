import joblib
from flask import Flask, request, jsonify


app = Flask(__name__)

cdqa_pipeline=joblib.load('./models/bert_wells_qa_latest.joblib')

@app.route("/chat", methods=["GET"])
def chat():
    query = request.args.get("q")
    prediction = cdqa_pipeline.predict(query=query)
    return jsonify(
        query=query, answer=prediction[0], title=prediction[1], paragraph=prediction[2]
    )
    
app.run(host='127.0.0.1', port=5001)
