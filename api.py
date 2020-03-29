from json import load, dumps
import falcon

with open('data.json') as f:
    data = load(f)['records']


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


app = falcon.API()
things = CovidResource()
app.add_route('/', things)
