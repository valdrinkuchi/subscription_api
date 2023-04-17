# Subscription API

## Technology stack

### Backend

- [Python](https://www.python.org/) 3.10
- [Django Framework](https://www.djangoproject.com/) 4.2
- [Django Rest Framework](https://www.django-rest-framework.org/) 3.14
- [PostgreSQL](https://www.postgresql.org/) for using as SQL database

### Development

- [decouple](https://pypi.org/project/python-decouple/) to load environment variables from .env into ENV

### Deployment

- [Docker](https://www.docker.com/)

## Getting started

### Development installation

1. Clone the repo locally:

```bash
git clone git@github.com:valdrinkuchi/subscription_api.git
cd subscription_api
```

2. Install the app locally:

```bash
pipenv shell
pipenv install

or
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Setup Database. The `seed.py` file has dummy data to get started.

```bash
python manage.py migrate
python manage.py seed
```

4. Start the application locally:

```bash
python manage.py runserver
```

### Running tests

1. Run tests:

```bash
python manage.py test
```

### Api-Overview

1. Create, Update and Delete a Customer:

   ```python
   GET: 0.0.0.0:8000/api/v1/customers/
   POST: 0.0.0.0:8000/api/v1/customers/
   PATCH: 0.0.0.0:8000/api/v1/customers/:id
   DELETE: 0.0.0.0:8000/api/v1/customers/:id
   {
    "name": "test@test.com",
    "identifier": "e43f556c-69b3-4476-bd23-83fe66c46da2"
   }
   ```

2. Create, Update and Delete a Subscriptions:

   ```python
   GET: 0.0.0.0:8000/api/v1/subscriptions
   POST: 0.0.0.0:8000/api/v1/subscriptions
   PATCH: 0.0.0.0:8000/api/v1/subscriptions/:id
   DELETE: 0.0.0.0:8000/api/v1/subscriptions/:id
   {
    'customer': 1,
    'start_date': "2022-01-01",
    'end_date': "2022-12-31",
    'billing_cycle': 1,
    'price': 5
    }
   ```
3. Retrieve accumulated subsription price for a specific month for a individual customer:

   ```python
   GET: 0.0.0.0:3000/api/v1/customers/1/accumulated-price?month=4
   ```

4. Retrieve accumulated subsription price for a specific month for all customers:

   ```python
   GET: 0.0.0.0:3000/api/v1/accumulated-price-list/?month=4
   ```
### Examples

In the `seed.py` there are 3 customers created, 10 Subscriptions that are billed monthly for each customer
and 15 subscriptions that are billed quarterly.
