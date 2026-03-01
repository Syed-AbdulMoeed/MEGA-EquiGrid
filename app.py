from functools import lru_cache

from flask import Flask, jsonify, render_template, request
import us
import zipcodes

from logic import get_equity_analysis

app = Flask(__name__)


STATE_OPTIONS = sorted(
    [(st.name, st.abbr) for st in us.states.STATES_AND_TERRITORIES],
    key=lambda item: item[0],
)


@lru_cache(maxsize=64)
def get_cities_for_state(state_abbr):
    rows = zipcodes.filter_by(state=state_abbr)
    cities = set()
    for row in rows:
        city = (row.get("city") or "").strip()
        if city:
            cities.add(city)
    return sorted(cities)


@app.route('/', methods=['GET', 'POST'])
def index():
    img_data = None
    error_msg = None
    selected_state = request.form.get("state", "")
    selected_city = request.form.get("city", "")
    
    if request.method == 'POST':
        if not selected_state or not selected_city:
            error_msg = "Please select state first, then city."
        else:
            state_name = us.states.lookup(selected_state).name
            img_data = get_equity_analysis(selected_city, state_name)
            if img_data is None:
                error_msg = "Could not generate map. Please try another city."

    return render_template(
        'index.html',
        img_data=img_data,
        error_msg=error_msg,
        state_options=STATE_OPTIONS,
        selected_state=selected_state,
        selected_city=selected_city,
    )


@app.get("/api/cities")
def api_cities():
    state_abbr = request.args.get("state", "").strip().upper()
    state_obj = us.states.lookup(state_abbr)
    if not state_obj:
        return jsonify({"cities": [], "error": "Invalid state."}), 400
    return jsonify({"cities": get_cities_for_state(state_obj.abbr)})


if __name__ == '__main__':
    app.run(debug=True)
