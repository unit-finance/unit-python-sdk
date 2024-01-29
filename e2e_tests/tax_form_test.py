import os
from unit import Unit
from unit.models.codecs import DtoDecoder
from unit.models.returnAch import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def test_get_list_tax_form():
    response = client.tax_forms.list()
    for t in response.data:
        assert t.type == "taxForm"


def test_tax_form_dto():
    json_response = {
        "type": "taxForm",
        "id": "1",
        "attributes": {
            "formType": "1099-INT",
            "taxYear": "2023"
        },
        "relationships": {
            "customer": {
                "data": {
                    "type": "customer",
                    "id": "10"
                }
            },
            "account": {
                "data": {
                    "type": "account",
                    "id": "1000"
                }
            }
        }
    }

    tax_form = DtoDecoder.decode(json_response)
    tax_form_dict = json.loads(json.dumps(tax_form, default=lambda o: o.__dict__, sort_keys=True, indent=4))

    assert sorted(json_response) == sorted(tax_form_dict)


def test_get_tax_form():
    response = client.tax_forms.list()
    for t in response.data:
        assert t.type == "taxForm"
        tax_form = client.tax_forms.get(t.id).data
        assert t.id == tax_form.id
        assert t.type == tax_form.type
        assert t.attributes.get("formType") == tax_form.attributes.get("formType")


def test_get_tax_form_pdf():
    response = client.tax_forms.list()
    for t in response.data:
        assert t.type == "taxForm"
        tax_form_pdf = client.tax_forms.get_pdf(t.id).data
        assert tax_form_pdf
