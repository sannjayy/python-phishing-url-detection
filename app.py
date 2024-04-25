from flask import Flask, request, render_template
from featureExtractor import featureExtraction
from pycaret.classification import load_model, predict_model

model = load_model('model/phishingdetection')

def predict(url):
    data = featureExtraction(url)
    result = predict_model(model, data=data)
    prediction_score = result['prediction_score'][0]  
    prediction_label = result['prediction_label'][0] 
    
    return {
        'prediction_label': prediction_label,
        'prediction_score': prediction_score * 100,
    }
    
    
    
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        url = request.form["url"]
        data = predict(url)
        return render_template('index.html', url=url, data=data )
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)