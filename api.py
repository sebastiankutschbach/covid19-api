from json import load, dumps
import falcon
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


app = falcon.API()
covid = CovidResource()
app.add_route('/', covid)
