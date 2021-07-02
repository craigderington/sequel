import os
import sys
import logging
import random
import config
import requests
import logging
from database import db_session as db
from models import Dealer, Customer, Address, Location
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
                    dealer_id=random.choice(dealers_ids),
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
    pass

def get_customer_order_details():
    pass

def get_customer_order_shipping():
    pass
