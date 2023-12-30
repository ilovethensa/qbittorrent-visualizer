# qBittorrent Visualizer

This is a Docker container that generates an interactive map visualizing the geographic locations of peers connected to a qBittorrent server.

## Usage

### Build the Docker Image

```bash
docker build -t qbittorrent-visualizer .
```
### Run the Docker Container

Replace the environment variable values and volume mount paths as needed.

```bash
docker run -it \
    -e QBITTORRENT_HOST=<YOUR_QBITTORRENT_HOST> \
    -e QBITTORRENT_PORT=<YOUR_QBITTORRENT_PORT> \
    -e QBITTORRENT_USERNAME=<YOUR_QBITTORRENT_USERNAME> \
    -e QBITTORRENT_PASSWORD=<YOUR_QBITTORRENT_PASSWORD> \
    -v /path/to/your/ip2location/db:/db/DB.BIN \
    -p 9435:9435 \
    qbittorrent-visualizer
```
### Access the Visualizer

Once the container is running, you can access the visualizer by opening your web browser and navigating to:
```
http://<ip>:9435
```