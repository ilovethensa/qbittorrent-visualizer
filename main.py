#!/usr/bin/env python3
import qbittorrentapi
import os
import IP2Location
import folium
import schedule
import time

# Set your environment variables for connection information
qbittorrent_host = os.environ.get("QBITTORRENT_HOST")
qbittorrent_port = int(os.environ.get("QBITTORRENT_PORT"))
qbittorrent_username = os.environ.get("QBITTORRENT_USERNAME")
qbittorrent_password = os.environ.get("QBITTORRENT_PASSWORD")
ip2location_db_path = "/db/DB.BIN"

def log(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{current_time}] {message}")

def run_script():
    try:
        log("Script execution started.")
        conn_info = dict(
            host=qbittorrent_host,
            port=qbittorrent_port,
            username=qbittorrent_username,
            password=qbittorrent_password,
        )
        database = IP2Location.IP2Location(ip2location_db_path)

        def get_gps_from_ip(ip):
            rec = database.get_all(ip)
            return rec.latitude, rec.longitude

        def extract_ips(peers_dict):
            ips = []
            for peer_info in peers_dict.get('peers', {}).values():
                ip = peer_info.get('ip')
                if ip:
                    ips.append(ip)
            return ips

        qb = qbittorrentapi.Client(**conn_info)

        # Get all torrent hashes
        torrents_info = qb.torrents_info()
        ipArray = []
        ipGPSArray = []

        for torrent in torrents_info:
            info = qb.sync.torrentPeers(torrent_hash=torrent.hash)
            for ip in extract_ips(info):
                ipArray.append(ip)

        for ip in ipArray:
            info = get_gps_from_ip(ip)
            ipGPSArray.append(info)

        # Create a folium map centered at the mean of the ipGPSArray
        map_center = [
            sum([float(lat) for lat, lon in ipGPSArray]) / len(ipGPSArray),
            sum([float(lon) for lat, lon in ipGPSArray]) / len(ipGPSArray)
        ]
        mymap = folium.Map(location=map_center, zoom_start=2)

        # Add markers to the map
        for i, (lat, lon) in enumerate(ipGPSArray):
            folium.Marker([float(lat), float(lon)], popup=f'Location {i + 1}').add_to(mymap)

        # Save the map to an HTML file
        mymap.save('/app/index.html')
        log("Page generated successfully.")
    except Exception as e:
        log(f"Error during script execution: {str(e)}")

# Run the script once immediately
run_script()

# Schedule the script to run every 10 minutes
schedule.every(10).minutes.do(run_script)

log("Scheduler started.")

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
