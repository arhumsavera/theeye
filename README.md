# The Eye

This repo provides endpoints to record "events" of different categories. It is implemented using Django 3.x

### Instructions to run

* Install docker and docker-compose
* Clone the repository with `git clone https://github.com/arhumsavera/theeye.git`
* Populate your .env file at the project root. Sample for reference.
* Run with `docker-compose up --build `
* Once everything is running, You can login at http://localhost:8000/api/v1/login/
* GET or POST data at http://localhost:8000/api/v1/events/ 

You can check out the various endpoints by going to either of 
* http://localhost:8000/swagger/
* http://localhost:8000/redoc/

For events: ` /api/v1/events/ `

*  supports GET and POST
*  Supports query params like GET /api/v1/events/?category=page%20interaction

```
GET /api/v1/events/
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "page interaction",
            "name": "cta click",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
                "element": "chat bubble"
            },
            "timestamp": "2021-01-01T09:15:27.243860Z"
        }
    ]
}
```


Available fields to query include:
1. A specific session
2. A specific category
3. A specific time range


Event's which are deeemed invalid due to either missing fields or errors in specific payload validation are accesible at `GET /api/v1/errors/`

* Searching error events is possible via Session ID

```
GET /api/v1/errors/?session_id=e2085be5-9137-4e4e-80b5-f1ffddc25423
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "error": {
                "missingfields": [
                    "name"
                ]
            },
            "received": "{'session_id': 'e2085be5-9137-4e4e-80b5-f1ffddc25423', 'category': 'page interaction', 'data': {'host': 'www.consumeraffairs.com', 'path': '/', 'element': 'chat bubble'}, 'timestamp': '2021-01-01 09:15:27.243860'}",
            "created_at": "2021-10-21T23:39:21.866740Z"
        }
    ]
}
```
In addition, You can query for sessions based on the type of error such as `GET /api/v1/errors/?missingfields=category`


Basic auth is provided via `dj-rest-auth`. For convenience, `docker-compose.yml` file will create a default super user which you can provide credentials for in your .env file. Only authorized user's are able to create and retrive data. Session based authorizaton is also enabled along with Token based for convenience. 

### Notes

Based on the requirements provided in the assesment README, the following design choices were made:

* Since we have multiple events from the same session we don't need it as our primary key and can get awat with a simple table to just store the incoming data
* Since it's still pretty open about what the payload looks like, the safest bet was to use a JSON field without over complicating the schema.
* This will be a write heavy application, so we should avoid too many indexes.
* This application assumed a session ID will always be provided and a v4 UUID
* Datetime will be provided by different applications in a consistent format.
  * Sample ` GET api/v1/events/?start_datetime=2026-10-03T19:00:00 `

* Based on provided test data we can have multiple events for the same session ID and timestamp

To avoid over engineering, The `FailedEvent` table simply stores the incoming failed request along with information related to the time of arrival ("for cases like incorrect timestamps") and list's of missing fields that are expected. Another option would be to either use just one table for both and mark them as failed|success but for our first version it adds complexity in retrieval. Similarly, if we wanted to store all fields individually, both Event and FailedEvent could inherit from a base model and have different rules for validation.


Some simple validation functions are included to demonstrate how variable payload validation can be extended for different types. Right now, as a simple example we just assume to always have a fixed set of fields for some chosen events and check the incoming payload's content accordingly.




Since we expect a high volume of requests, the task of adding data to the database is offloaded via Celery workers and using RabbitMQ as our broker.
