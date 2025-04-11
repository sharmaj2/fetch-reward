import math
from datetime import datetime
from app.models import Receipt

# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


def calculate_points(receipt: Receipt) -> int:

    # logger.info("Retailer: %s", receipt.retailer)
    # logger.info("Total: %s", receipt.total)
    # logger.info("Items: %s", receipt.items)
    # logger.info("Purchase Date: %s", receipt.purchaseDate)
    # logger.info("Purchase Time: %s", receipt.purchaseTime)
        
    points = 0

    # Rule 1: 1 point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in receipt.retailer)

    # logger.info("Rule 1: %s", points)

    # Rule 2: 50 points if total is a round dollar amount with no cents
    try:
        total = float(receipt.total)
        if total.is_integer():
            points += 50

            # logger.info("Rule 2: %s", points)
    except ValueError:
        pass

    # Rule 3: 25 points if total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25
        # logger.info("Rule 3: %s", points)

    # Rule 4: 5 points for every two items
    points += (len(receipt.items) // 2) * 5

    # logger.info("Rule 4: %s", points)

    # Rule 5: For each item, if trimmed description length is a multiple of 3
    for item in receipt.items:
        desc = item.shortDescription.strip()
        # logger.info("item desc and length %s %s", {desc}, {len(desc)})
        if len(desc) % 3 == 0:
            try:
                price = float(item.price)
                bonus = math.ceil(price * 0.2)
                # logger.info("bonus %s", {bonus})
                points += bonus

                # logger.info("Rule 5: %s", points)
            except ValueError:
                continue

    # Rule 6: 5 points if total > 10.00
    # Note: The rule below is intentionally *not implemented* following the points given in examples.
    # if total > 10.00:
    #     points += 5
    #     logger.info("Rule 6: %s", points)

    # Rule 7: 6 points if purchase day is odd
    try:
        purchase_date = receipt.purchaseDate
        if isinstance(purchase_date, str):
            purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d").date()
        if purchase_date.day % 2 == 1:
            points += 6
            # logger.info("Rule 7: %s", points)
    except Exception:
        pass

    # Rule 8: 10 points if time is between 14:00 and 16:00
    try:
        purchase_time = receipt.purchaseTime
        if isinstance(purchase_time, str):
            purchase_time = datetime.strptime(purchase_time, "%H:%M").time()
        if 14 <= purchase_time.hour < 16:
            points += 10
            # logger.info("Rule 8: %s", points)
    except Exception:
        pass

    return points
