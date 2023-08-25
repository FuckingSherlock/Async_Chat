import logging as lg
from datetime import date

lg.basicConfig(
    filename=str(date.today())+'_server.log',
    encoding='utf-8',
    format="%(asctime)s %(levelname)-10s %(module)s %(message)s",
    level=lg.INFO
)
