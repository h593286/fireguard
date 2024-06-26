from datetime import UTC, datetime
import sys
import schedule
import time

from src.broker.publisher import Publisher
from src.broker.api_client import ApiClient
cities = [
  {
    "city": "Oslo", 
    "lat": "59.9133", 
    "lng": "10.7389", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Oslo", 
    "capital": "primary", 
    "population": "1064235", 
    "population_proper": "709037"
  }, 
  {
    "city": "Bergen", 
    "lat": "60.3894", 
    "lng": "5.3300", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Vestland", 
    "capital": "admin", 
    "population": "267117", 
    "population_proper": "267117"
  }, 
  {
    "city": "Stavanger", 
    "lat": "58.9700", 
    "lng": "5.7314", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Rogaland", 
    "capital": "admin", 
    "population": "237369", 
    "population_proper": "129300"
  }, 
  {
    "city": "Sandnes", 
    "lat": "58.8517", 
    "lng": "5.7361", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Rogaland", 
    "capital": "minor", 
    "population": "237369", 
    "population_proper": "58694"
  }, 
  {
    "city": "Trondheim", 
    "lat": "63.4297", 
    "lng": "10.3933", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Trøndelag", 
    "capital": "minor", 
    "population": "194860", 
    "population_proper": "194860"
  }, 
  {
    "city": "Sandvika", 
    "lat": "59.8833", 
    "lng": "10.5167", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Viken", 
    "capital": "minor", 
    "population": "115543", 
    "population_proper": "115543"
  }, 
  {
    "city": "Kristiansand", 
    "lat": "58.1472", 
    "lng": "7.9972", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Agder", 
    "capital": "minor", 
    "population": "113737", 
    "population_proper": "113737"
  }, 
  {
    "city": "Drammen", 
    "lat": "59.7378", 
    "lng": "10.2050", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Viken", 
    "capital": "minor", 
    "population": "109416", 
    "population_proper": "109416"
  }, 
  {
    "city": "Asker", 
    "lat": "59.8331", 
    "lng": "10.4392", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Viken", 
    "capital": "minor", 
    "population": "61523", 
    "population_proper": "61523"
  }, 
  {
    "city": "Tønsberg", 
    "lat": "59.2981", 
    "lng": "10.4236", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Vestfold og Telemark", 
    "capital": "minor", 
    "population": "57794", 
    "population_proper": "57794"
  }, 
  {
    "city": "Skien", 
    "lat": "59.2081", 
    "lng": "9.5528", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Vestfold og Telemark", 
    "capital": "admin", 
    "population": "55513", 
    "population_proper": "55513"
  }, 
  {
    "city": "Bodø", 
    "lat": "67.2827", 
    "lng": "14.3751", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Nordland", 
    "capital": "admin", 
    "population": "52803", 
    "population_proper": "52803"
  }, 
  {
    "city": "Ålesund", 
    "lat": "62.4740", 
    "lng": "6.1582", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Møre og Romsdal", 
    "capital": "minor", 
    "population": "52163", 
    "population_proper": "52163"
  }, 
  {
    "city": "Moss", 
    "lat": "59.4592", 
    "lng": "10.7008", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Viken", 
    "capital": "minor", 
    "population": "50290", 
    "population_proper": "50290"
  }, 
  {
    "city": "Arendal", 
    "lat": "58.4608", 
    "lng": "8.7664", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Agder", 
    "capital": "admin", 
    "population": "45509", 
    "population_proper": "45509"
  }, 
  {
    "city": "Lørenskog", 
    "lat": "59.8989", 
    "lng": "10.9642", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Viken", 
    "capital": "minor", 
    "population": "44693", 
    "population_proper": "44693"
  }, 
  {
    "city": "Tromsø", 
    "lat": "69.6828", 
    "lng": "18.9428", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Troms og Finnmark", 
    "capital": "admin", 
    "population": "38980", 
    "population_proper": "38980"
  }, 
  {
    "city": "Haugesund", 
    "lat": "59.4464", 
    "lng": "5.2983", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Rogaland", 
    "capital": "minor", 
    "population": "37444", 
    "population_proper": "37444"
  }, 
  {
    "city": "Molde", 
    "lat": "62.7375", 
    "lng": "7.1591", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Møre og Romsdal", 
    "capital": "admin", 
    "population": "32002", 
    "population_proper": "32002"
  }, 
  {
    "city": "Askøy", 
    "lat": "60.4667", 
    "lng": "5.1500", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Vestland", 
    "capital": "", 
    "population": "29816", 
    "population_proper": "29816"
  }, 
  {
    "city": "Hamar", 
    "lat": "60.7945", 
    "lng": "11.0679", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Innlandet", 
    "capital": "admin", 
    "population": "27947", 
    "population_proper": "27947"
  }, 
  {
    "city": "Oppegård", 
    "lat": "59.7925", 
    "lng": "10.7903", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Viken", 
    "capital": "", 
    "population": "27394", 
    "population_proper": "27394"
  }, 
  {
    "city": "Rygge", 
    "lat": "59.3747", 
    "lng": "10.7147", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Viken", 
    "capital": "minor", 
    "population": "16145", 
    "population_proper": "16145"
  }, 
  {
    "city": "Steinkjer", 
    "lat": "64.0148", 
    "lng": "11.4954", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Trøndelag", 
    "capital": "admin", 
    "population": "12985", 
    "population_proper": "12985"
  }, 
  {
    "city": "Randaberg", 
    "lat": "59.0017", 
    "lng": "5.6153", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Rogaland", 
    "capital": "minor", 
    "population": "11454", 
    "population_proper": "11454"
  }, 
  {
    "city": "Lommedalen", 
    "lat": "59.9500", 
    "lng": "10.4667", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Viken", 
    "capital": "", 
    "population": "11200", 
    "population_proper": "11200"
  }, 
  {
    "city": "Barbu", 
    "lat": "58.4664", 
    "lng": "8.7781", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Agder", 
    "capital": "", 
    "population": "6787", 
    "population_proper": "6787"
  }, 
  {
    "city": "Tiller", 
    "lat": "63.3550", 
    "lng": "10.3790", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Trøndelag", 
    "capital": "", 
    "population": "3595", 
    "population_proper": "3595"
  }, 
  {
    "city": "Kolbotn", 
    "lat": "59.8112", 
    "lng": "10.8000", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Viken", 
    "capital": "minor", 
    "population": "", 
    "population_proper": ""
  }, 
  {
    "city": "Lillestrøm", 
    "lat": "59.9500", 
    "lng": "11.0833", 
    "country": "Norway", 
    "iso2": "NO", 
    "admin_name": "Viken", 
    "capital": "minor", 
    "population": "", 
    "population_proper": ""
  }
]


importing = False

# last time is how long the last import took. This is used to adjust the sleeping time for the api.
last_time = 0

client = ApiClient()

publisher = Publisher()
def import_data_and_publish():
    print("running import at",datetime.now(UTC))
    errors = []
    global importing
    if not importing:
        start = time.time()
        importing = True
        publisher.connect()
        for city in cities:
            try:
                name = city['city']
                firerisks = client.get_data_for_city(name)
                try:
                    for risk in firerisks:
                        publisher.publish(name, f'{{"timestamp":"{risk["timestamp"]}", "ttf":"{risk["ttf"]}"}}')
                except BaseException as e:
                    print(e)
            except BaseException as e:
                print(e)
                errors.append(e)
        publisher.disconnect()
        importing = False
        last_time = time.time() - start
        print(f"import complete, used {last_time} seconds. {len(errors)} errors occured", flush=True)
    
schedule.every(120).seconds.do(import_data_and_publish)

def run_scheduling():
    while True:
        schedule.run_pending()
        next_run = schedule.next_run()
        wait_time = 1
        if next_run is not None:
            wait_time = (next_run - datetime.now(next_run.tzinfo)).seconds - 1
        print("next run at", schedule.next_run(), "waiting", wait_time, "seconds")
        sys.stdout.flush()
        time.sleep(max(wait_time, 1))