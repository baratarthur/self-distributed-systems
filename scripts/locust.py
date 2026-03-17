import random
from locust import FastHttpUser, task, constant_throughput, tag

class SocialMediaUser(FastHttpUser):
    # Fix: constant_throughput(1) results in 1 req/sec. 
    # For 10 req/sec per user, use 10.
    wait_time = constant_throughput(1) 
    
    def on_start(self):
        """
        Called when a virtual user starts. 
        Good for initializing session-specific data.
        """
        self.user_id = random.randint(1, 1000)

    @tag('write')
    @task(1)
    def write_post(self):
        # Using a context manager allows for better error handling/grouping
        with self.client.post("/post", 
                             json={"content": "foo", "userId": self.user_id}, 
                             name="/posts", catch_response=True) as response:
            if response.status_code != 201:
                response.failure(f"Post failed with status: {response.status_code}")

    @tag('read')
    @task(9)
    def view_items(self):
        # name parameter groups URLs with dynamic IDs into one entry in the UI
        self.client.get(f"/feed/{self.user_id}", name="/feed/[id]")