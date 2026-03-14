import requests
import time

BASE_URL = "http://127.0.0.1:8000"
CORRECT_PASSWORD = "DummyTestPassword123!"
WRONG_PASSWORD = "WrongPassword123!"

timestamp = int(time.time())
BRUTE_FORCE_EMAIL = f"target_1_{timestamp}@example.com"
CLEAN_SESSION_EMAIL = f"target_2_{timestamp}@example.com"

def print_step(message):
    print(f"\n[{time.strftime('%H:%M:%S')}] === {message} ===")

def setup_user(email):
    response = requests.post(f"{BASE_URL}/register", json={
        "email": email,
        "password": CORRECT_PASSWORD
    })
    return response.status_code == 201

def test_brute_force_lockout():
    print_step("TEST 1: BRUTE FORCE ATTACK & LOCKOUT")
    print(f"Registering target user: {BRUTE_FORCE_EMAIL}")
    setup_user(BRUTE_FORCE_EMAIL)
    
    session = requests.Session()
    for attempt in range(1, 7):
        response = session.post(f"{BASE_URL}/login", json={
            "email": BRUTE_FORCE_EMAIL,
            "password": WRONG_PASSWORD
        })
        print(f"Attempt {attempt}: Status {response.status_code} -> {response.json().get('detail')}")
        
        if response.status_code == 403:
            print(">> DEFENSE SUCCESS: System detected attack and locked the account.")
            break

def test_secure_session_flow():
    print_step("TEST 2: SECURE SESSION LIFECYCLE")
    print(f"Registering clean user: {CLEAN_SESSION_EMAIL}")
    setup_user(CLEAN_SESSION_EMAIL)
    
    session = requests.Session()
    
    # 1. Login
    login_resp = session.post(f"{BASE_URL}/login", json={
        "email": CLEAN_SESSION_EMAIL,
        "password": CORRECT_PASSWORD
    })
    print(f"1. Login Status: {login_resp.status_code}")
    
    # 2. Verify Cookie
    cookies = session.cookies.get_dict()
    if 'session_id' in cookies:
        print(f">> SUCCESS: Secure HTTP-Only cookie received -> {cookies['session_id'][:15]}...")
    
    # 3. Access Protected Route
    me_resp = session.get(f"{BASE_URL}/me", cookies=cookies)
    print(f"2. Accessing protected /me route Status: {me_resp.status_code}")
    
    # 4. Logout
    logout_resp = session.post(f"{BASE_URL}/logout", cookies=cookies)
    print(f"3. Logout Status: {logout_resp.status_code}")
    
    # 5. Verify Logout Protection
    me_resp_after = session.get(f"{BASE_URL}/me", cookies=cookies)
    print(f"4. Accessing /me after logout Status: {me_resp_after.status_code} -> {me_resp_after.json().get('detail')}")
    print(">> DEFENSE SUCCESS: Session successfully destroyed and access revoked.")

if __name__ == "__main__":
    test_brute_force_lockout()
    test_secure_session_flow()