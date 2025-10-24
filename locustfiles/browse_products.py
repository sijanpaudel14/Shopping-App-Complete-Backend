from locust import HttpUser, task, between, events
from random import choice


# Global lists to store actual IDs
PRODUCT_IDS = []
COLLECTION_IDS = []


# @events.test_start.add_listener
# def on_test_start(environment, **kwargs):
#     """Fetch actual IDs before test starts"""
#     from store.models import Product, Collection

#     global PRODUCT_IDS, COLLECTION_IDS
#     PRODUCT_IDS = list(Product.objects.values_list('id', flat=True)[:100])
#     COLLECTION_IDS = list(Collection.objects.values_list('id', flat=True))

#     print(
#         f"Loaded {len(PRODUCT_IDS)} product IDs and {len(COLLECTION_IDS)} collection IDs")


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    # ✅ Hardcode actual IDs from your database
    PRODUCT_IDS = [905, 288, 660, 737, 520, 864, 604, 615, 257, 438, 
                   394, 436, 679, 51, 924, 939, 127, 790, 903, 750]
    COLLECTION_IDS = [7, 3, 4, 1, 2, 10, 6, 8, 5, 9]

    @task(2)
    def view_products(self):
        print("===============Viewing Products=================")
        collection_id = choice(self.COLLECTION_IDS)
        self.client.get(
            f"/store/products/?collection_id={collection_id}",
            name="/store/products/"
        )

    @task(4)
    def view_product_details(self):
        print("===============Viewing Product Details=================")
        product_id = choice(self.PRODUCT_IDS)
        self.client.get(
            f"/store/products/{product_id}/",
            name="/store/products/[id]/"
        )

    @task(1)
    def add_to_cart(self):
        print("===============Adding Product to Cart=================")
        product_id = choice(self.PRODUCT_IDS)
        self.client.post(
            f"/store/carts/{self.cart_id}/items/",
            name="/store/carts/items/",
            json={"product_id": product_id, "quantity": 1}
        )

    def on_start(self):
        print("===============Creating Cart=================")
        response = self.client.post("/store/carts/")
        self.cart_id = response.json().get("id")
