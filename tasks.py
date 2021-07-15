import os
import sys
import logging
import random
import config
import requests
import logging
from datetime import datetime, timedelta
from database import db_session as db
from models import Dealer, Customer, Address, Location, ProductType, Product, CustomerOrder, \
    OrderDetail, OrderShipping
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("TASKS")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("tasks.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
cfg = config.Config()


def get_dealers():
    """ Generate Mock Data from API Endpoint """
    API_PATH = "dealer.json"
    method = "GET"
    hdr = {"Content-Type": "application/json", "User-Agent": "SEQUEL"}
    params = None
    cnt = 0

    try:
        r = requests.request(
            method,
            cfg.BASE_URL + API_PATH + cfg.API_KEY,
            headers=hdr,
            params=params
        )
        # logger.info("{}{}{}".format(cfg.BASE_URL, API_PATH, cfg.API_KEY))
        if r.status_code == 200:
            resp = r.json()
            for i in resp:
                dealer = Dealer(
                    name=i["name"],
                    dealer_code=i["dealer_code"],
                )
                # save to database
                db.add(dealer)
                db.commit()
                db.flush()
                cnt += 1
                logger.info("Dealer Record Added: {}:{}".format(str(dealer.id), i["name"]))

            # log the total records added
            logger.info("Total Records Processed: {}".format(str(cnt)))

        else:
            logger.info("MockAPI returned status code: {}".format(str(r.status_code)))

    except requests.exceptions.HTTPError as http_err:
        logger.info("HTTP Error: {}".format(str(http_err)))

    return cnt


def get_dealer_customers():
    """ Populate the Dealer Customer List """
    API_PATH = "customer.json"
    method = "GET"
    hdr = {"Content-Type": "application/json", "User-Agent": "SEQUEL"}
    params = None
    cnt = 0

    try:
        r = requests.request(
            method,
            cfg.BASE_URL + API_PATH + cfg.API_KEY,
            headers=hdr,
            params=params
        )

        if r.status_code == 200:
            resp = r.json()
            dealers = db.query(Dealer).limit(cfg.QUERY_LIMIT).all()
            dealer_ids = [dealer.id for dealer in dealers]
            for r in resp:
                nc = Customer(
                    dealer_id=random.choice(dealer_ids),
                    first_name=r["first_name"],
                    last_name=r["last_name"],
                    email=r["email"],
                    status=True
                )

                # save to database
                try:
                    db.add(nc)
                    db.commit()
                    db.flush()
                    cnt += 1
                    logger.info("Customer Added:{}: {} {}".format(str(nc.id), r["first_name"], r["last_name"]))

                except SQLAlchemyError as db_err:
                    logger.critical("Database Error: {}".format(str(db_err)))

            # log totals
            logger.info("{} Total Customers Created".format(str(cnt)))

        else:
            logger.warning("API status code: {}".format(str(r.status_code)))

    except requests.exceptions.HTTPError as err:
        logger.critical("HTTP Connection Error: {}".format(str(err)))

    return "{} Customers Loaded".format(str(cnt))


def get_dealer_customer_addresses():
    """ Generate Mock Customer Address Data from API Endpoint """
    API_PATH = "customer_address.json"
    method = "GET"
    hdr = {"Content-Type": "application/json", "User-Agent": "SEQUEL"}
    params = None
    cnt = 0

    try:
        r = requests.request(
            method,
            cfg.BASE_URL + API_PATH + cfg.API_KEY,
            headers=hdr,
            params=params
        )
        # logger.info("{}{}{}".format(cfg.BASE_URL, API_PATH, cfg.API_KEY))
        if r.status_code == 200:
            resp = r.json()
            customers = db.query(Customer).limit(cfg.QUERY_LIMIT).all()
            customer_ids = [c.id for c in customers]
            for addr in resp:
                nca = Address(
                    customer_id=random.choice(customer_ids),
                    street=addr["street"],
                    city=addr["city"],
                    state=addr["state"],
                    zip_code=addr["zip_code"],
                    latitude=addr["latitude"],
                    longitude=addr["longitude"],
                    status=True
                )
                # save to the database
                try:
                    db.add(nca)
                    db.commit()
                    db.flush()
                    logger.info("Customer {} Address Added: {} {}".format(str(nca.id), str(addr["latitude"]), str(addr["longitude"])))
                    cnt += 1
                except SQLAlchemyError as db_err:
                    logger.critical("Database Error: {}".format(str(db_err)))

            # log the totals
            logger.info("{} Total Customer Address Records Created".format(str(cnt)))

        else:
            logger.warning("API status code: {}".format(str(r.status_code)))

    except requests.exceptions.HTTPError as err:
        logger.warning("HTTP Connection Error: {}".format(str(err)))


def get_dealer_locations():
    """ Get the Dealer Location Mock Data from API Endpoint"""
    API_PATH = "dealer_location.json"
    method = "GET"
    hdr = {"Content-Type": "application/json", "User-Agent": "SEQUEL"}
    params = None
    cnt = 0

    try:
        r = requests.request(
            method,
            cfg.BASE_URL + API_PATH + cfg.API_KEY,
            headers=hdr,
            params=params
        )

        if r.status_code == 200:
            resp = r.json()
            dealers = db.query(Dealer).limit(cfg.QUERY_LIMIT).all()
            dealer_ids = [d.id for d in dealers]

            for loc in resp:
                location = Location(
                    dealer_id=random.choice(dealer_ids),
                    address=loc["address"],
                    active=True
                )

                db.add(location)
                db.commit()
                db.flush()
                cnt += 1
                logger.info("Dealer ID: {} Location Addded: {}".format(str(location.id), loc["address"]))
            logger.info("{} Total Dealer Locations Addedd".format(str(cnt)))
        else:
            logger.warning("API status code: {}".format(str(r.status_code)))

    except requests.exceptions.HTTPError as e:
        logger.info(e)

    return cnt


def get_dealer_product_types():
    """ Get Dealer Product Types Mock Data from API Endpoint """
    API_PATH = "dealer_product_type.json"
    method = "GET"
    hdr = {"Content-Type": "application/json", "User-Agent": "SEQUEL"}
    params = None
    cnt = 0

    try:
        r = requests.request(
            method,
            cfg.BASE_URL + API_PATH + cfg.API_KEY,
            headers=hdr,
            params=params
        )

        if r.status_code == 200:
            resp = r.json()
            dealers = db.query(Dealer).limit(cfg.QUERY_LIMIT).all()
            dealer_ids = [d.id for d in dealers]

            for p in resp:
                dpt = ProductType(
                    dealer_id=random.choice(dealer_ids),
                    name=p["name"],
                    active=True
                )
                # save to the database
                try:
                    db.add(dpt)
                    db.commit()
                    db.flush()
                    cnt += 1
                    logger.info("Product Type ID: {} Addded".format(str(dpt.id)))

                except SQLAlchemyError as err:
                    logger.critical("Database Error: {}".format(str(err)))
            logger.info("{} Total Product Types Created".format(str(cnt)))
        else:
            logger.warning("API status code: {}".format(str(r.status_code)))

    except requests.exceptions.HTTPError as e:
        logger.warning("HTTP Connection Error: {}".format(str(e)))

    return cnt


def get_dealer_products():
    """ Get Dealer Product Mock Data from API Endpoint """
    API_PATH = "dealer_products.json"
    method = "GET"
    hdr = {"Content-Type": "application/json", "User-Agent": "SEQUEL"}
    params = None
    cnt = 0

    try:
        r = requests.request(
            method,
            cfg.BASE_URL + API_PATH + cfg.API_KEY,
            headers=hdr,
            params=params
        )

        if r.status_code == 200:
            resp = r.json()
            dealers = db.query(Dealer).limit(cfg.QUERY_LIMIT).all()
            pt = db.query(ProductType).all()
            ids = [d.id for d in dealers]
            pids = [p.id for p in pt]

            for p in resp:
                product = Product(
                    dealer_id=random.choice(ids),
                    product_type_id=random.choice(pids),
                    name=p["name"],
                    description=p["description"],
                    item_price=p["item_price"],
                    active=True,
                    location=None
                )
                # save to the database
                try:
                    db.add(product)
                    db.commit()
                    db.flush()
                    cnt += 1
                    logger.info("Product ID: {} added for Dealer ID: {}".format(str(product.id), str(product.dealer_id)))

                except SQLAlchemyError as db_err:
                    logger.info("Database Error: {}".format(str(db_err)))

            # log the totals
            logger.info("{} Total Dealer Products Created".format(str(cnt)))
        else:
            logger.warning("API status code: {}".format(str(r.status_code)))

    except requests.exceptions.HTTPError as http_err:
        logger.warning("HTTP Connection Error: {}".format(str(http_err)))

    return cnt


def get_customer_orders():
    """ Get Customer Order Mock Data from API Endpoint """
    API_PATH = "customer_order.json"
    method = "GET"
    hdr = {"Content-Type": "application/json", "User-Agent": "SEQUEL"}
    params = None
    cnt = 0

    try:
        r = requests.request(
            method,
            cfg.BASE_URL + API_PATH + cfg.API_KEY,
            headers=hdr,
            params=params
        )
        if r.status_code == 200:
            resp = r.json()
            customers = db.query(Customer).limit(cfg.QUERY_LIMIT).all()
            ids = [{"customer_id": c.id, "dealer_id": c.dealer_id} for c in customers]
            for r in resp:
                for c in ids:
                    r.update(c)
                    # add a new customer order
                    nco = CustomerOrder(
                        dealer_id=r["dealer_id"],
                        customer_id=r["customer_id"],
                        order_number=r["order_number"],
                        order_date=datetime.now(),
                        order_status=r["order_status"]
                    )
                    # save to database
                    db.add(nco)
                    db.commit()
                    db.flush()
                    logger.info("Customer ID: {} order completed successfully".format(str(r["customer_id"])))
                    cnt += 1

    except requests.exceptions.HTTPError as http_error:
        logger.info("HTTP Error: {}".format(str(http_error)))

    return cnt


def get_customer_order_details():
    """ Get the Order Detail with Products and Price."""
    hdr = {"Content-Type": "application/json", "User-Agent": "SEQUEL"}
    method = "GET"
    params = None
    cnt = 0
    API_PATH = "/customer_order_detail.json"

    try:
        r = requests.request(
            method,
            cfg.BASE_URL + API_PATH + cfg.API_KEY,
            headers=hdr,
            params=params
        )

        if r.status_code == 200:
            resp = r.json()
            orders = db.query(CustomerOrder).limit(cfg.QUERY_LIMIT).all()
            order_ids = [o.id for o in orders]
            products = db.query(Product).limit(cfg.QUERY_LIMIT).all()
            product_ids = [p.id for p in products]
            for n in resp:
                cod = OrderDetail(
                    order_id=random.choice(order_ids),
                    order_product_id=random.choice(product_ids),
                    order_product_quantity=int(n["order_product_quantity"]),
                    order_product_item_price=float(n["order_product_item_price"]),
                    order_line_item_total=float(n["order_product_quantity"] * n["order_product_item_price"])
                )
                # save to the database
                db.add(cod)
                db.commit()
                db.flush()
                logger.info("Customer Order Detail Updated: {}".format(str(cod.id)))
                cnt += 1
        else:
            logger.info("API returned status code: {}".format(str(r.status_code)))

    except requests.exceptions.HTTPError as http_err:
        logger.warning("HTTP Error: {}".format(str(http_err)))

    return cnt


def get_customer_order_shipping():
    hdr = {"Content-Type": "application/json", "User-Agent": "SEQUEL"}
    API_PATH = "/customer_order_shipping.json"
    method = "GET"
    params = None
    cnt = 0

    try:
        r = requests.request(
            method,
            cfg.BASE_URL + API_PATH + cfg.API_KEY,
            headers=hdr,
            params=params
        )

        if r.status_code == 200:
            resp = r.json()
            orders = db.query(Customer.id, CustomerOrder.id, OrderDetail.id, Address.id).filter(
                Customer.id == CustomerOrder.customer_id,
                CustomerOrder.id == OrderDetail.order_id,
                Customer.id == Address.customer_id
            ).limit(cfg.QUERY_LIMIT).all()

            # create a dictionary of the address ids and orders id to merge with the response data
            ids = [{"address_id": o[3], "order_id": o[1], "order_detail_id": o[2]} for o in orders]

            for item in resp:
                for n in ids:
                    item.update(n)
                    # create a new customer shipping record
                    cos = OrderShipping(
                        address_id=item["address_id"],
                        order_id=item["order_id"],
                        order_detail_id=item["order_detail_id"],
                        shipping_date=datetime.strptime(item["shipping_date"] + " 12:00:00", "%m/%d/%Y %H:%M:%S"),
                        shipping_status=item["shipping_status"],
                        shipping_tracking_number=item["shipping_tracking_number"],
                        shipping_carrier=item["shipping_carrier"],
                        shipping_delivered=item["shipping_delivered"],
                        shipping_final_disposition=item["shipping_final_disposition"]
                    )

                    # save to the database
                    db.add(cos)
                    db.commit()
                    db.flush()
                    cnt += 1
                    logger.info("Shipping Customer Order: {}".format(str(item["order_id"])))
        else:
            logger.info("API call returned HTTP Status Code: {}".format(str(r.status_code)))
        
    except requests.exceptions.HTTPError as http_err:
        logger.info("HTTP Error: {}".format(str(http_err)))

    return cnt


def get_order_number(customer_id):
    """ Generate a random customer order number """
    return str(customer_id) + "-" + str(random.randint(2000000, 3000000))
