import sqlalchemy
import json
import random
import sys
import config
import database
import logging
import time
from tasks import get_dealers, get_dealer_customers, get_dealer_customer_addresses
from datetime import datetime, timedelta
from models import Dealer, Customer, Address, Location, Product, \
    ProductType, Order, OrderDetail, OrderShipping


logger = logging.getLogger("MAIN")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
MQL = config.Config().QUERY_LIMIT


class Workload(object):
    """
    A database workload runner
    :params db_session
    :return query
    """

    def init_db(self):
        self.db = database.db_session()
        self.today = datetime.now().strftime("%c")
        try:
            database.init_db()
            logger.info("Database Initialized on: {}".format(self.today))
        except sqlalchemy.exc.SQLAlchemyError as err:
            logger.critical("Database initialization failure.: {}".format(str(err)))
            sys.exit(1)
    
    def populate_data(self):
        get_dealers()
        get_dealer_customers()
        get_dealer_customer_addresses()
    
    def run_workload(self):
        self.populate_data()
        self.show_dealers()
        self.show_dealer_customers()
        self.show_dealer_customer_addr()
    
    def show_dealers(self):
        dealers = self.db.query(Dealer).limit(MQL).all()
        for dealer in dealers:
            logger.info("Dealer: {}".format(dealer.name))
        logger.info("{} Total Dealer Records".format(str(len(dealers))))
    
    def show_dealer_customers(self):
        customers = self.db.query(Customer).limit(MQL).all()
        for c in customers:
            logger.info("Customer {} Record: {} {}".format(c.id, c.first_name, c.last_name))
        logger.info("{} Total Dealer Customer Records".format(str(len(customers))))

    def show_dealer_customer_addr(self):
        addr = self.db.query(Address).limit(MQL).all()
        for a in addr:
            logger.info("Customer ID: {} Address Record.  LatLong: {}/{}".format(str(a.id), str(a.latitude), str(a.longitude)))
        logger.info("{} Total Customer Address Records".format(str(len(addr))))

    def show_dealer_product_types(self):
        pass
    
    def show_dealer_products(self):
        pass
    
    def show_customer_orders(self):
        pass
    
    def show_customer_order_shipping(self):
        pass


if __name__ == "__main__":
    try:
        runner = Workload()
        logger.info("Starting up database workload runner with default params.")
        runner.init_db()
        logger.info("Create database schema.  Please wait...")
        time.sleep(5)
        start = time.time()

        try:
            logger.info("Populating table data, this will only take a minute.")
            # start populating data
            runner.populate_data()
            logger.info("Starting database workload runner.  Max queries set to: {}".format(str(MQL)))
            
            while True:
                # run the workload
                runner.run_workload()
                logger.warning("Sleeping for 5 seconds, resuming in 4, 3, 2, 1...")
                time.sleep(5.0)
                # break

        except sqlalchemy.exc.SQLAlchemyError as db_err:
            logger.critical("Database exception: {}".format(str(db_err)))

    except Exception as e:
        logger.critical("Application exception occurred: {}".format(str(e)))
