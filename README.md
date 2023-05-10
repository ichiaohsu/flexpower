# Trades API

In directory `/apis` contains the trades APIs to get/create trades. 

## Requirements

Python >= 3.10

## Installation

To run the server, there are some dependencies necessary. Install them with `apis/requirements.txt`:

```bash
pip3 install -r requirements.txt
```

## Usage

### Setup

The server uses a simple sqlite database. Before running it, a environment variable `DATABASE_URL` should be set to indicate where is the sqlite db. In `apis` folder there is an example db `trades.db`. The server could be started immediately with the example db. To use it, make sure you are in root directory, **not in** `apis`, set `export DATABASE_URL=sqlite:///apis/trades.db`

### Migration

If you're using custom db file, it's necessary to migrate it first. This project uses `alembic` to migrate new database. It requires `DATABASE_URL` to denote the db file, so make sure to set it correctly. Then also under root directory, flexpower, run 
```bash
alembic -c apis/alembic.ini upgrade head
```

### Run locally
Use `uvicorn` to serve the APIs locally:
```bash
uvicorn apis.main:app --reload
```
The local server could be reach at http://localhost:8000. See how to organize your requests with OpenAPI documents at http://localhost:8000/doc.


### Run with docker-compose
This projects comes with a docker-compose setup so you could easily build the service first and start it with:
```bash
docker-compose up --build trades
```
If you already have the image, ignore the `--build` argument here.

The server will be available at http://localhost:8000. The docker-compose also takes care of the migrations, and mount the example db `trades.db` to proper location, so you should have up-to-date schema to work with. To change the database and its corresponding, check the settings in [docker-compose.yaml](docker-compose.yaml)
```docker-compose
  trades:
    build: 
      context: ./apis
    image: trades
    depends_on:
      - migrations
    environment:
      DATABASE_URL: sqlite:///./trades.db
    ports:
      - 8000:8000
    volumes:
      - ./apis/trades.db:/code/trades.db

  migrations:
    build: 
      context: ./apis
    image: trades
    environment:
      DATABASE_URL: sqlite:///./trades.db
    entrypoint: sh -c "alembic -c apis/alembic.ini upgrade head"
    volumes:
      - ./apis/trades.db:/code/trades.db
```
Remember to set volumes and `DATABASE_URL` in both `trades` and `migrations` sections. They use the same Docker image under the hood.

# Workflows

In `workflows` directory it provides two scripts to import trades data from CSV files, and generate the report with specific `trader_id` and `delivery_day`.

They depends on the API server, so make sure to start a API server beforehand.

## Installation
There is a independent `requirements.txt` come with `workflows`:
```bash
pip3 install -r workflows/requirements.txt
```

In fact, `import_trades.py` only depends on `requests`, so you could simply install it through `pip install requests`. For `generate_report.py`, it requires extra dependency `tabulate`.

## Usage

### import trades

`import_trades.py` comes with help. Simply do `python workflows/import_trades.py -h` you could see:
```bash
usage: import_trades.py [-h] [--api-url URL] [--path PATH]

generate report

options:
  -h, --help     show this help message and exit
  --api-url URL  The trades API URL
  --path PATH    the csv source path
```
You could there are two arguments you could set:
1. `--api-url`(optional): the API url of trades server. It defaults to http://localhost:8000. Set it if you have different configuration set it with `--api-url={YOUR SERVER URL}`
2. `--path`(optional): The absolute folder contains source CSV files. This script will walk through all the CSV files under this path. It defaults to `workflows/sources`. 

So if you don't set any of the arguments and do 
```bash
python workflows/import_trades.py
```
It will try to import all the csv files in `workflows/sources` with API server running at http://localhost:8000.

### generate reports
`generate_report.py` generates PnL report for specific trader on a single day. It also comes with help. Simply do `python workflows/generate_report.py --help`:
```bash
usage: generate_report.py [-h] [--api-url URL] --trader-id TRADER_ID --delivery-day DELIVERY_DAY

generate report

options:
  -h, --help            show this help message and exit
  --api-url URL         The trades API URL
  --trader-id TRADER_ID
                        Unique id of a trader
  --delivery-day DELIVERY_DAY
                        Day on which the energy has to be delivered in local time.
```
There are three arguments:
1. `--api-url`(optional): the API url of trades server. It also defaults to http://localhost:8000. Set it if you have different configuration set it with `--api-url={YOUR SERVER URL}`.
2. `--trader-id`(required): The trader id the report is for.
3. `--delivery-day`(required): The day the report is for. The format is `%Y-%m-%d`. e.g. "2023-02-28"

Use the API server with example db, you could generate the report with following:
```bash
python workflows/generate_report.py --trader-id trader_2 --delivery-day 2023-02-28
```
The result looks like
```bash
Hour       Number of Trades    Total BUY [MW]    Total Sell [MW]    PnL [Eur]
-------  ------------------  ----------------  -----------------  -----------
9 - 10                    1                 0                 57        -4446
20 - 21                   1                18                  0          612
Total                     2                18                 57        -3834
```

# Dashboard
In `/dashboard` there is a React application that also generate the report in a HTML page. You could run it locally or with docker-compose.

## Installation
You need to install node package before using
```bash
cd dashboard
npm install
```

## Usage

### Configure
It requires `REACT_APP_API_HOST` to indicate where is the backend server. In local environment, you could set it directly through `export REACT_APP_API_HOST=http://localhost:8000`, or recommended with an .env file. Modify `dashboard/.env.development` for local test. Production settings is in `dashboard/.env.production`. Set it corresondingly before build the project.

### Run with npm
With environment variable set, you could start the local dashboard
```bash
npm start
```
The dashboard will running at http://localhost:3000. Try to type the trader id and pick a date, and generate the report by pressing the **Generate** button. Since our example db only has data on `2023-02-28`, the datepicker is default to this day.

### Run with docker-compose
docker-compose will run a dashboard as well. Before doing that, remember to modify the `REACT_APP_API_HOST` to a desired setting in `/dashboard/.env.production`. Then
```bash
docker-compose up --build
```
This will start both dashboard and trades API. The dashboard will be hosted at port 80 by nginx. Visit the dashboard at http://localhost.
