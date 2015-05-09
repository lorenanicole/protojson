import flask
import json
import addressbook_pb2

app = flask.Flask(__name__)


class GLOBAL:
    book_pb = addressbook_pb2.AddressBook(
        contacts=[
            addressbook_pb2.Contact(
                first_name='Alice',
                last_name='Bertram',
                phone_numbers=[
                    addressbook_pb2.Phone(type=addressbook_pb2.MOBILE, number='123'),
                    addressbook_pb2.Phone(type=addressbook_pb2.LANDLINE, number='567'),
                ],
            )
        ],
    )
    book_dict = {
        'contacts': [
            {'first_name': 'Alice',
             'last_name': 'Bertram',
             'phone_numbers': [
                 {'type': 'MOBILE', 'number': '123'},
                 {'type': 'LANDLINE', 'number': '567'},
             ]
            },
        ],
    }


@app.route('/api/json/full', methods=['GET', 'POST'])
def json_full():
    if flask.request.method == 'POST':
        GLOBAL.book_dict = json.loads(flask.request.data)
    elif flask.request.method == 'GET':
        return json.dumps(GLOBAL.book_dict)


@app.route('/api/pb/full', methods=['GET', 'POST'])
def pb_full():
    if flask.request.method == 'POST':
        GLOBAL.book_pb.ParseFromString(flask.request.data)
    elif flask.request.method == 'GET':
        return GLOBAL.book_pb.SerializeToString()


@app.route('/api/json/search-by-name', methods=['GET'])
def json_search_by_name():
    # e.g. curl 127.1:5000/api/pb/search-by-name?name="alice"
    name = flask.request.args.get('name')
    result = []

    for x in GLOBAL.book_dict.get('contacts', []):
        if name in x['first_name'] or name in x['last_name']:
            result.append(x)

    return json.dumps(result)


@app.route('/api/pb/search-by-name', methods=['GET'])
def pb_search_by_name():
    # e.g. curl 127.1:5000/api/pb/search-by-name?name="alice"
    name = flask.request.args.get('name')
    result = addressbook_pb2.SearchResult()

    for x in GLOBAL.book_pb.contacts:
        if name in x.first_name or name in x.last_name:
            result.contacts.extend([x])

    return result.SerializeToString()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
