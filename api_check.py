import requests
import logging

logging.basicConfig(
    filename='health_check.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def check_api(url):
    try:
        response = requests.get(url, timeout=5)
        
        # Check if there were redirects
        if response.history:
            redirect_count = len(response.history)
            if redirect_count > 3:
                logging.warning(f"Many redirects for {url}: {redirect_count} hops")
            else:
                logging.info(f"API OK with {redirect_count} redirect(s): {url} -> {response.url}")
        
        # Check final response status - Only 2xx and 3xx are considered healthy
        if 200 <= response.status_code < 400:  # 2xx (Success) or 3xx (Redirect) = OK
            if 200 <= response.status_code < 300:
                logging.info(f"API OK: {url} - Status: {response.status_code}")
            else:  # 3xx range
                logging.info(f"API OK (Redirect): {url} - Status: {response.status_code}")
        else:  # 4xx or 5xx = Not healthy
            if 400 <= response.status_code < 500:
                logging.error(f"Client Error: {url} - Status: {response.status_code}")
            elif response.status_code >= 500:
                logging.error(f"Server Error: {url} - Status: {response.status_code}")
            else:
                # This catches any other unexpected status codes (1xx, etc.)
                logging.warning(f"Unexpected status: {url} - Status: {response.status_code}")
            
    except requests.exceptions.TooManyRedirects:
        logging.error(f"Too many redirects: {url}")
    except requests.RequestException as e:
        logging.error(f"Error reaching {url}: {e}")

# Replace with your actual API endpoints
check_api("https://api.upcitemdb.com/prod/trial/lookup")
