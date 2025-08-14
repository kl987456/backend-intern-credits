import requests

BASE_URL = "http://127.0.0.1:8000/api/credits"

def ensure_test_user():
    """Create a test user if not exists, return user_id."""
    payload = {"email": "test@example.com", "name": "Test User"}
    r = requests.post(f"{BASE_URL}/dev/create-user", json=payload)
    if r.status_code in (200, 201):
        data = r.json()
        print("✅ Dev user:", data)
        return data["user_id"]
    print("❌ Unexpected error creating user:", r.status_code, r.text)
    raise SystemExit(1)

def run_flow():
    user_id = ensure_test_user()

    print("1) Get credits")
    r = requests.get(f"{BASE_URL}/{user_id}")
    print(r.status_code, r.json())

    print("2) Add credits +10")
    r = requests.post(f"{BASE_URL}/{user_id}/add", json={"amount": 10})
    print(r.status_code, r.json())

    print("3) Deduct credits -5")
    r = requests.post(f"{BASE_URL}/{user_id}/deduct", json={"amount": 5})
    print(r.status_code, r.json())

    print("4) Reset credits")
    r = requests.patch(f"{BASE_URL}/{user_id}/reset")
    print(r.status_code, r.json())

if __name__ == "__main__":
    run_flow()
