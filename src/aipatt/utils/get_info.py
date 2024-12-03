import os
import psutil
import socket
import requests
import platform
from datetime import datetime

def get_date_time():
    """
    Returns the current date and time in the desired format.
    """
    now = datetime.now()
    return now.strftime("%d %B %Y, %I:%M %p")

def bytes_to_gb(bytes_size):
    """
    Convert bytes to GB.
    """
    return round(bytes_size / (1024 * 1024 * 1024), 2)

def get_system_info() -> dict:
    """
    Get system information such as OS, version, CPU, memory, disk, and network.
    """
    system_info = {
        "os_name": platform.system(),
        "os_version": platform.release(),
        "cwd": os.getcwd(),
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_info": get_memory_info(),
        "disk_info": get_disk_info(),
        "network_info": get_network_info(),
    }
    return system_info

def get_memory_info() -> dict:
    """
    Get memory usage information (total, available, used, free, etc.) in GB/MB.
    """
    memory = psutil.virtual_memory()
    return {
        "total": bytes_to_gb(memory.total),
        "available": bytes_to_gb(memory.available),
        "used": bytes_to_gb(memory.used),
        "free": bytes_to_gb(memory.free),
        "percent": memory.percent
    }

def get_disk_info() -> dict:
    """
    Get disk usage information based on the platform (Windows, macOS, Linux).
    """
    if platform.system() == "Windows":
        disk_path = "C:/"
    else:
        disk_path = "/"
    
    disk_info = psutil.disk_usage(disk_path)
    return {
        "total": bytes_to_gb(disk_info.total),
        "used": bytes_to_gb(disk_info.used),
        "free": bytes_to_gb(disk_info.free),
        "percent": disk_info.percent
    }

def get_network_info() -> dict:
    """
    Get the IP address for both Ethernet and Wi-Fi interfaces across all platforms.
    """
    net_info = psutil.net_if_addrs()
    network_info = {}

    for iface, addrs in net_info.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                if platform.system() == "Linux":
                    if iface.startswith("en") or iface.startswith("wlan"):
                        network_info[iface] = addr.address
                elif platform.system() == "Windows":
                    if "Ethernet" in iface or "Wi-Fi" in iface:
                        network_info[iface] = addr.address
                elif platform.system() == "Darwin":
                    if iface.startswith("en") or "wlan" in iface:
                        network_info[iface] = addr.address
                else:
                    network_info[iface] = addr.address

    return network_info

def get_location() -> dict:
    """
    Get the real-time location (IP-based) of the device using the ipinfo.io.
    """
    try:
        ip_info_url = 'https://ipinfo.io/json'
        response = requests.get(ip_info_url)
        location_data = response.json()
        
        city = location_data.get('city', 'Unknown')
        region = location_data.get('region', 'Unknown')
        country = location_data.get('country', 'Unknown')
        ip = location_data.get('ip', 'Unknown')
        loc = location_data.get('loc', 'Unknown')
    except Exception:
        pass
    return city, region, country, ip, loc

def print_system_info():
    """
    Prints the system and location information in a narrative sentence format.
    """
    try:
        dt = f"The current Date & Time is: {get_date_time()}."

        system_info = get_system_info()

        os = f"The operating system is {system_info['os_name']}, version {system_info['os_version']}."
        cd = f"The current working directory is '{system_info['cwd']}'."
        si = f"The system has {system_info['cpu_count']} CPU cores, and currently, the CPU usage is {system_info['cpu_percent']}%."
        
        memory_info = system_info['memory_info']
        mi =(f"The total memory is {memory_info['total']} GB, with {memory_info['available']} GB available. "
            f"{memory_info['used']} GB of memory is in use, and {memory_info['free']} GB is free. "
            f"Memory usage is at {memory_info['percent']}%.")
        
        disk_info = system_info['disk_info']
        di =(f"The total disk space is {disk_info['total']} GB, with {disk_info['used']} GB used and {disk_info['free']} GB free. "
            f"Disk usage is at {disk_info['percent']}%.")
        
        network_info = system_info.get("network_info", {})
        if network_info:
            for iface, ip in network_info.items():
                ni = f"The IP address for the {iface} interface is {ip}."
        else:
            pass

        city, region, country, ip, loc = get_location()
        li = f"The current Geolocation is approximately {loc}. and the public IP address is {ip}."
        gli = f"The current location is {city}, {region}, {country}."
    except Exception:
        pass
    return f"{dt}\n{os}\n{cd}\n{si}\n{mi}\n{di}\n{ni}\n{li}\n{gli}"

def info():
    return print_system_info()
