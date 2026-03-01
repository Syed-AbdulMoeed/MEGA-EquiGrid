from flask import Flask, render_template, request
from logic import get_equity_analysis 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    img_data = None
    error_msg = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        state = request.form.get('state')
        query = f"{city}, {state}, USA"
        
        # Trigger the logic
        img_data = get_equity_analysis(query)
        
        if img_data is None:
            error_msg = "Could not generate map. Please check city/state spelling."

    return render_template('index.html', img_data=img_data, error_msg=error_msg)

if __name__ == '__main__':
    app.run(debug=True)