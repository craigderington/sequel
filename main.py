import argparse
import sqlalchemy
import json
import random
import sys
import config
import database
import logging
import time
from tasks import get_dealers, get_dealer_customers, get_dealer_customer_addresses, \
    get_dealer_locations, get_dealer_product_types, get_dealer_products, get_customer_orders, \
    get_customer_order_details, get_customer_order_shipping
from datetime import datetime, timedelta
from models import Dealer, Customer, Address, Location, Product, \
    ProductType, CustomerOrder, OrderDetail, OrderShipping


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
        get_dealer_locations()
        get_dealer_product_types()
        get_dealer_products()
        get_customer_orders()
        get_customer_order_details()
        get_customer_order_shipping()


    def run_workload(self):
        self.populate_data()
        self.show_dealers()
        self.show_dealer_customers()
        self.show_dealer_customer_addr()
        self.show_dealer_product_types()
        self.show_dealer_products()
        self.show_customer_orders()
        self.show_customer_order_detail()
        self.show_customer_order_shipping()


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
        pt = self.db.query(ProductType).all()
        for p in pt:
            logger.info("Dealer {} Product Type: {}".format(str(p.dealer_id), str(p.name)))
        logger.info("{} Total Product Type Records".format(str(len(pt))))


    def show_dealer_products(self):
        products = self.db.query(Product).limit(MQL).all()
        for p in products:
            logger.info("Dealer Product: {}".format(str(p.name)))
        logger.info("{} Total Dealer Products.".format(str(len(products))))


    def show_customer_orders(self):
        orders = self.db.query(CustomerOrder).limit(MQL).all()
        for o in orders:
            logger.info("Customer {} Order {} placed on {}".format(str(o.customer_id), str(o.order_number), str(o.order_date)))
        logger.info("{} Total Customer Orders.".format(str(len(orders))))

    def show_customer_order_detail(self):
        order_detail = self.db.query(OrderDetail).limit(MQL).all()
        for order in order_detail:
            logger.info("Customer Order Detail: {}".format(str(order.order_id)))
        logger.info("{} Total Customer Order Detail".format(str(len(order_detail))))

    def show_customer_order_shipping(self):
        shipped = self.db.query(OrderShipping).all()
        for order in shipped:
            logger.info("Customer Order Shipping Status: {} on {}".format(str(order.id), order.shipping_date))
        logger.info("{} Total Orders Shipped".format(str(len(shipped))))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, help="The length of time to run the workload, in minutes.")
    parser.add_argument("--database", type=str, help="Database type option, MySQL or SQLite3")
    parser.add_argument("--limit", type=int, help="Query limit in integer, i.e. 500")
    
    try:
        args = parser.parse_args()
        duration = int(args.duration * 60)
        try:
            runner = Workload()
            logger.info("Starting up database workload runner with default params.")
            runner.init_db()
            logger.info("Create database schema.  Please wait...")
            time.sleep(5)
            start_time = time.time()

            try:
                logger.info("Populating table data, this will only take a minute.")
                # start populating data
                runner.populate_data()
                logger.info("Starting database workload runner.  Max queries set to: {}".format(str(MQL)))
                
                while True:
                    current_time = time.time()
                    # run the workload
                    runner.run_workload()
                    logger.warning("Sleeping for 5 seconds, resuming in 4, 3, 2, 1...")
                    time.sleep(5.0)
                    
                    if args.duration:
                        if (current_time - start_time) <= duration:
                            break

            except sqlalchemy.exc.SQLAlchemyError as db_err:
                logger.critical("Database exception: {}".format(str(db_err)))

        except Exception as e:
            logger.critical("Application exception occurred: {}".format(str(e)))

    except argparse.ArgumentTypeError as ate:
        logger.critical("Argument Error: {}".format(str(ate)))
        sys.exit(1)
