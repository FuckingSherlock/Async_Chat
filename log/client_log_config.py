import logging as lg
from datetime import date

client_log = lg.basicConfig(
    filename=str(date.today())+'_client.log',
    encoding='utf-8',
    format="%(asctime)s %(levelname)-10s %(module)s %(message)s",
    level=lg.INFO
)
