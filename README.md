# unit-python-sdk

This library provides a python wrapper to [Unit's API](https://docs.unit.co/#introduction).

## Documentation
See https://docs.unit.co/

## Installation

    pip install unit-python-sdk

## Usage
Creating Business Application
```python
    import os
    from unit import Unit
    from unit.models import *
    from unit.models.application import CreateBusinessApplicationRequest
    
    token = os.environ.get("token")
    api_url = os.environ.get("api_url")

    unit = Unit(api_url, token)

    request = CreateBusinessApplicationRequest(
        name="Acme Inc.",
        address=Address("1600 Pennsylvania Avenue Northwest",
                        "Washington", "CA", "20500", "US"),
        phone=Phone("1", "9294723497"), state_of_incorporation="CA", entity_type="Corporation", ein="123456789",
        officer=Officer(full_name=FullName("Jone", "Doe"), date_of_birth=date.today() - timedelta(days=20 * 365),
                        address=Address("950 Allerton Street",
                                        "Redwood City", "CA", "94063", "US"),
                        phone=Phone("1", "2025550108"), email="jone.doe@unit-finance.com", ssn="000000005"),
        contact=BusinessContact(full_name=FullName(
            "Jone", "Doe"), email="jone.doe@unit-finance.com", phone=Phone("1", "2025550108")),
        beneficial_owners=[
            BeneficialOwner(
                FullName("James", "Smith"), date.today() -
                timedelta(days=20*365),
                Address("650 Allerton Street",
                        "Redwood City", "CA", "94063", "US"),
                Phone("1", "2025550127"), "james@unit-finance.com", ssn="574567625"),
            BeneficialOwner(FullName("Richard", "Hendricks"), date.today() - timedelta(days=20 * 365),
                            Address("470 Allerton Street",
                                    "Redwood City", "CA", "94063", "US"),
                            Phone("1", "2025550158"), "richard@unit-finance.com", ssn="574572795")
        ]
    )
    
    application = unit.applications.create(request).data
    print(application.id)
```

Fetching a customer

```python
    import os
    from unit import Unit

    token = os.environ.get("token")
    api_url = os.environ.get("api_url")

    unit = Unit(api_url, token)
    customer = unit.customers.list().data[0]
    print(customer.id)
```

## Retrying API Requests
API requests can fail for many reasons, from network components failures, API rate limits, timeouts or service incidents.
<br> Create requests without idempotency key won't trigger the retry mechanism, so we recommend to pass an idempotency key where applicable. 

You can read about retries here: https://docs.unit.co/#retries. <br>

the default amount of retries is 0. <br>Unit initialization with retries:
```python
    import os
    from unit import Unit

    token = os.environ.get("token")
    api_url = os.environ.get("api_url")

    unit = Unit(api_url, token, retries=3)
```

## Request Timeouts
Every HTTP request issued by the SDK has a per-attempt timeout (default: 120 seconds).
This prevents calls from hanging indefinitely if a connection stalls during a Unit API
outage. The previous `timeout` argument is still honored — it now controls the **total
retry budget** for the backoff loop, while the new `request_timeout` argument controls
the **per-attempt** HTTP timeout passed to `requests`.

```python
    unit = Unit(api_url, token, retries=3, timeout=120, request_timeout=120)
```

`requests.exceptions.Timeout` and `requests.exceptions.ConnectionError` are now retried
the same way 4xx/5xx retryable responses are. The one exception is `post_create` calls:
they will only be retried on network exceptions when an `idempotencyKey` is present in
the request body — otherwise the exception bubbles up immediately to avoid the risk of
double-processing.
