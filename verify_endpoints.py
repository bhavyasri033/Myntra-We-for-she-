import urllib.request
import json
import sys

def test_endpoint(url, expected_count=None, check_keys_present=None, check_keys_absent=None, custom_assert=None):
    print(f"Testing Endpoint: {url} ...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print("  SUCCESS!")
            
            if expected_count is not None:
                if not isinstance(data, list):
                    print(f"  CRITICAL ERROR: Expected list representation, got {type(data)}!")
                    sys.exit(1)
                if len(data) != expected_count:
                    print(f"  CRITICAL ERROR: Expected count {expected_count}, got {len(data)}!")
                    sys.exit(1)
                print(f"  [OK] Returned exact count: {len(data)}")
                
            if isinstance(data, list) and len(data) > 0:
                item = data[0]
            elif isinstance(data, list) and len(data) == 0:
                item = {}
            else:
                item = data
                
            if check_keys_present:
                for k in check_keys_present:
                    if k not in item:
                        print(f"  CRITICAL ERROR: Key '{k}' is missing from response!")
                        print(f"  Item keys: {list(item.keys())}")
                        sys.exit(1)
                print(f"  [OK] Validated keys present: {check_keys_present}")
                
            if check_keys_absent:
                for k in check_keys_absent:
                    if k in item:
                        print(f"  CRITICAL ERROR: Key '{k}' was found in response but should be absent!")
                        sys.exit(1)
                print(f"  [OK] Validated keys absent: {check_keys_absent}")
                
            if custom_assert:
                custom_assert(data)
                print("  [OK] Custom assertion passed.")
            print("  --------------------------------------")
    except Exception as e:
        print(f"  FAILED: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Test 1: Fetch all products (unfiltered)
    test_endpoint("http://localhost:8000/products", expected_count=3)
    
    # Test 2: GET /states (Check dynamic state exploration list count & schemas)
    def assert_states_count(data):
        states_names = [s["name"] for s in data]
        print(f"  Available states: {states_names}")
        if "Telangana" not in states_names:
            print("  CRITICAL ERROR: Telangana is missing from states directory!")
            sys.exit(1)
    test_endpoint(
        "http://localhost:8000/states",
        expected_count=9,  # Telangana, AP, Tamil Nadu, Kerala, Karnataka, Rajasthan, Bihar, Maharashtra, UP
        check_keys_present=["id", "name", "image", "shopping_hub_count"],
        check_keys_absent=["_id"],
        custom_assert=assert_states_count
    )
    
    # Test 3: GET /shopping-hubs (check list formatting - should use id, not _id, and have no region)
    test_endpoint(
        "http://localhost:8000/shopping-hubs", 
        expected_count=14, 
        check_keys_present=["id", "name", "state", "description", "banner_image", "categories", "store_count", "featured"],
        check_keys_absent=["_id", "region"]
    )
    
    # Test 4: GET /shopping-hubs with state filter
    test_endpoint("http://localhost:8000/shopping-hubs?state=Telangana", expected_count=3)
    
    # Test 5: GET /shopping-hubs?featured=true
    test_endpoint("http://localhost:8000/shopping-hubs?featured=true", expected_count=9)
    
    # Test 6: GET /shopping-hubs/hyd
    test_endpoint(
        "http://localhost:8000/shopping-hubs/hyd",
        check_keys_present=["id", "name", "cover_image", "latitude", "longitude", "created_at"],
        check_keys_absent=["_id", "region"]
    )
    
    # Test 7: GET /shopping-hubs/hyd/stores (Check relation mapping and privacy filter)
    test_endpoint(
        "http://localhost:8000/shopping-hubs/hyd/stores",
        expected_count=5, # South India, RS Brothers, Chandana Brothers, KLM, Kalanjali
        check_keys_present=["_id", "name", "shopping_hub_id"],
        check_keys_absent=["trust_score", "google_rating", "review_count"]
    )
    
    # Test 8: GET /shopping-hubs?search=Hyd (Query parameter partial search)
    def assert_hyd_featured_first(data):
        if data[0]["name"] != "Hyderabad":
            print(f"  CRITICAL ERROR: Expected Hyderabad first, got '{data[0]['name']}'")
            sys.exit(1)
    test_endpoint(
        "http://localhost:8000/shopping-hubs?search=Hyd",
        expected_count=1,
        check_keys_present=["id", "name"],
        check_keys_absent=["_id", "region"],
        custom_assert=assert_hyd_featured_first
    )
    
    # Test 9: GET /shopping-hubs/search?query=vij (Path partial search)
    test_endpoint(
        "http://localhost:8000/shopping-hubs/search?query=vij",
        expected_count=1,
        check_keys_present=["id", "name"],
        check_keys_absent=["_id", "region"]
    )
    
    print("\nALL STATE-FIRST EXPLORATION AND SHOPPING HUB SERVICE VERIFICATIONS PASSED SUCCESSFULLY!")
