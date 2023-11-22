import requests, re, ipaddress
from colorama import init, Fore

init(autoreset=True)

INVALID_IP_FORMAT = 1
INVALID_IP_ADDRESS = 2

def get_location(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Error:", e)
        return None
    except ValueError as e:
        print(Fore.RED + "Error decoding JSON response:", e)
        return None

def generate_google_maps_link(latitude, longitude):
    return f"https://www.google.com/maps?q={latitude},{longitude}"

def validate_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
        return True, None
    except ValueError:
        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip):
            return False, INVALID_IP_ADDRESS
        return False, INVALID_IP_FORMAT

def main():
    try:
        while True:
            ip_address = input("Enter IP address: ")
            
            if ip_address.lower() == 'exit':
                break
            
            is_valid_ip, error_code = validate_ip_address(ip_address)
            
            if not is_valid_ip:
                if error_code == INVALID_IP_FORMAT:
                    print(Fore.RED + "Invalid IP address. Error Code:", INVALID_IP_FORMAT)
                elif error_code == INVALID_IP_ADDRESS:
                    print(Fore.RED + "Invalid IP address. Error Code:", INVALID_IP_ADDRESS)
                continue

            location_data = get_location(ip_address)
            if location_data is not None:
                print("IP Address:", Fore.GREEN + location_data.get("ip", "N/A"))
                print("Hostname:", Fore.CYAN + location_data.get("hostname", "N/A"))
                print("City:", Fore.YELLOW + location_data.get("city", "N/A"))
                print("Region:", Fore.YELLOW + location_data.get("region", "N/A"))
                print("Country:", Fore.BLUE + location_data.get("country", "N/A"))
                print("Location:", Fore.MAGENTA + location_data.get("loc", "N/A"))
                print("Organization:", Fore.CYAN + location_data.get("org", "N/A"))

                loc = location_data.get("loc", "").split(",")
                if len(loc) == 2:
                    latitude, longitude = loc
                    maps_link = generate_google_maps_link(latitude, longitude)
                    print("Google Maps Link:", Fore.BLUE + maps_link)
                else:
                    print("Google Maps Link:", Fore.RED + "N/A")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
