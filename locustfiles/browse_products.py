# Browse Products
from locust import HttpUser, task, between
from random import randint

# Define a user behavior for browsing products


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # Simulate user wait time between tasks

    @task(2)
    def view_products(self):
        print("===============Viewing Products=================")
        # Simulate browsing a product with a random ID
        collection_id = randint(2, 6)
        self.client.get(
            f"/store/products/?collection_id={collection_id}",
            name="/store/products/"
        )
# Note: In a real-world scenario, you would want to ensure that the collection IDs
# being accessed actually exist in the database. This is a simplified example.

    @task(4)
    def view_product_details(self):
        print("===============Viewing Product Details=================")
        product_id = randint(1, 10)
        self.client.get(
            f"/store/products/{product_id}/",
            name="/store/products/[id]/"
        )

    @task(1)
    def add_to_cart(self):
        print("===============Adding Product to Cart=================")
        product_id = randint(1, 10)
        self.client.post(
            f"/store/carts/{self.cart_id}/items/",
            name="/store/carts/items/",
            json={"product_id": product_id, "quantity": 1}
        )

    def on_start(self):
        print("===============Creating Cart=================")
        # This method is called when a simulated user starts
        # Create a new cart for the user
        response = self.client.post("/store/carts/")
        self.cart_id = response.json().get("id")  # Store the cart ID for future use
