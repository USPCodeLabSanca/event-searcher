from flask import Flask, render_template, request
import geohash2
import requests
import os

app  = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == 'POST':
        data = request.get_json()
        
        geoPoint = geohash2.encode(float(data['latitude']), float(data['longitude']), precision=9)
        API_KEY = os.environ['API_KEY']
        
        radius = 100

        events = requests.get(f'https://app.ticketmaster.com/discovery/v2/events.json?geoPoint={geoPoint}&radius={radius}&unit=km&apikey={API_KEY}')
        print(f'https://app.ticketmaster.com/discovery/v2/events.json?geoPoint={geoPoint}&radius={radius}&unit=km&apikey={API_KEY}')
        
        events = events.json()
        if '_embedded' in events:
            events = events['_embedded']['events']
            eventsNames = [{'name': event['name'], 'url': event['url']} for event in events]
        else:
            return {'description': 'ERROR'}, 500
        print(eventsNames)
        
        return eventsNames, 200
    return {'oi':'123'}


if __name__ == "__main__":
    app.run(debug=True)