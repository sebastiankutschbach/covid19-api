from json import load, dumps
import falcon
from falcon.http_status import HTTPStatus
import wget


def readJson(file):
    with open(file) as f:
        return load(f)['records']


data = readJson('data.json')


class CovidResource(object):
    def on_get(self, req, res):
        country = req.params.get('country', None)
        date = req.params.get('date', None)
        filtered_data = data
        if country:
            filtered_data = [
                r for r in filtered_data if r['geoId'] == country]
        if date:
            filtered_data = [
                r for r in filtered_data if r['dateRep'] == date]
        res.body = dumps(filtered_data)

    def on_post(self, req, res):
        global data
        file = wget.download(
            'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/', out='new_data.json')
        data = readJson(file)


class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')


app = falcon.API(middleware=[HandleCORS()])
covid = CovidResource()
app.add_route('/', covid)
