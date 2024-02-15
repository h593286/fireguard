import json
import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def form_display():
    with open('cities.json', 'r') as json_file:
        data = json.load(json_file)

    dropdown_html = '<select name="city">'
    for city_info in data:
        city_name = city_info['city']
        dropdown_html += f'<option value="{city_name}">{city_name}</option>'
    dropdown_html += '</select>'

    return f'''
        <form action="http://127.0.0.1:5001/get_firerisk_city" method="get">
            {dropdown_html}
            <input type="submit" value="Get FireRisk"/>
        </form>
        <form action="http://127.0.0.1:5001/get_firerisk_coordinates" method="get">
            <input type="text" name="lat" placeholder="Latitude"/>
            <input type="text" name="lng" placeholder="Longitude"/>
            <input type="submit" value="Get FireRisk"/>
        </form>
    '''


if __name__ == '__main__':
    app.run(debug=True, port=5000) #FOR LOCAL
