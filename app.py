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
        radius = 5000

        print(f'{API_KEY}')

        events = requests.get(f'https://app.ticketmaster.com/discovery/v2/events.json?geoPoint={geoPoint}&radius={radius}&unit=km&apikey={API_KEY}')
    
        print(f'https://app.ticketmaster.com/discovery/v2/events.json?geoPoint={geoPoint}&radius={radius}&unit=km&apikey={API_KEY}')
        events = events.json()
        if '_embedded' in events:
            events = events['_embedded']['events']
            eventsNames = [{'name': event['name'], 'image': event['images'][0]['url'], 'distance': event['distance'], 'city': event['_embedded']['venues'][0]['city']['name'], 'date': event['dates']['start']['localDate'], 'hour': None} if 'localTime' not in event['dates']['start'] else {'name': event['name'], 'image': event['images'][0]['url'], 'distance': event['distance'], 'city': event['_embedded']['venues'][0]['city']['name'], 'date': event['dates']['start']['localDate'], 'hour': event['dates']['start']['localTime']} for event in events]
        else:
            return {'description': 'ERROR'}, 500
        
        formatedEvents = {}
        for event in eventsNames:
            if f"{event['name']} {event['city']}" in formatedEvents:
                formatedEvents[f"{event['name']} {event['city']}"]["dates"].append({
                    "hour": event['hour'],
                    "date": event['date']
                })
            else:
                formatedEvents[f"{event['name']} {event['city']}"] = {
                    'name': event['name'],
                    'image': event['image'],
                    'city': event['city'],
                    'distance': event['distance'],
                    'dates': [{'hour': event['hour'], 'date': event['date']}]
                }
        print(formatedEvents)
        
        return formatedEvents, 200

@app.route('/events')
def events():
    return render_template('events.html',)


if __name__ == "__main__":
    app.run(debug=True)