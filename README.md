# pychan
A self-hosted 4Chan frontend server that makes browsing 4Chan on mobile devices far easier! It still has many features planned and lots of new stuff on the way. I originally wrote this program in Go using the built-in `net/http` library however I've re-written it in Python for ease-of-development. The original project can be found here: [gochan](https://github.com/alex-ogden/gochan). It doesn't appear to have slowed down the program at all, being that the limitations will almost always be your network speed (for downloading images) and your disk read/write (same reason).

### Why?
PyChan was made to address a few issues I have as a 4Chan user:
* 4Chan doesn't have an app for iOS and any app developed for iOS is taken down after a certain time once Apple catches on. Yes, I am aware of Sigma, it's a great app but it's not 4Chan-focused - I also hate the Reddit-style approach to thread-layout.
* If used through a mobile web-browser, 4Chan looks pretty bad. It's a site built with Desktop use in mind. There have been some improvements recently but I still find it cumbersome to use on mobile.

PyChan addresses these issues by building in a mobile-first manner:
* A nice user interface, buttons and text which is big enough for mobile and a decent colour scheme (dark/light mode switcher at the top of each page).
* Ability to add PyChan to your homescreen with PWA capabilities built-in, this means that it acts just like a regular app would once opened from the homescreen (no browser interface, just the app). To do this see the following (wordy) guide:

[How to add a website to home screen on iOS and Android](https://techwiser.com/how-to-add-a-website-to-home-screen-on-ios-and-android/)

### Installation and Configuration
Installation is purposefully very easy. It's recommended to use the `build-and-run.sh` script to run the program, passing either `docker` or `local` as the first and only parameter. You can also use the the included `docker-compose.yml` file to run the program, however running using Python is also possible.

Clone the repo and enter the PyChan directory within the repo:
```bash
git clone https://github.com/alex-ogden/pychan.git
cd pychan
```

Now run the server
```bash
python3.10 run.py
```

You can optionally redirect logs to /dev/null by appending `&> /dev/null` to the `python3.10 run.py` command. You can also adjust the port and host address in `run.py` to your liking.

Images that are downloaded (see known issues below) will be stored in `pychan/static/images`.

#### Build Docker Image
To build the docker image, clone the repo and enter the root:
```bash
git clone https://github.com/alex-ogden/pychan.git
cd pychan
```

Now, build the docker image
```bash
CONTAINER_NAME="pychan"
docker build -t "${CONTAINER_NAME}" .
```

#### Run Compose
Once the image has built successfully, you can start up the compose service using the provided `docker-compose.yml` file.

```bash
docker compose up -d
```

Docker Compose will automatically create a volume and mount it to the container to hold the images downloaded by PyChan (see known issues below)

You should now be able to access PyChan at:
```
http://localhost:4433
```
Ammend the address and port to suit your setup and when connecting from another device.

### Troubleshooting
Everything should work correctly, however if something does go wrong, see the logs raised by the service using either `docker logs ${CONTAINER_NAME}` or by running the executable and ensuring logs are fed to stdout/stderr or to a file.

### Known Issues

##### Thread/Board Images:
Due to limitations of the 4Chan read-only API, it's not possible to reference images via URL (using `i.4cdn.org`) - this is a CORS issue. If you want to try using a CORS proxy feel free however I've not had much luck so far. Due to this, PyChan needs to pre-download the images to the filesystem before loading a thread/board. This can cause slowdowns on slow connections or in threads with many high-res images however the download process is handled via a python concurrency library so it's about as fast as it can be. It will clear all downloaded images before loading a new thread or board so you shouldn't have a problem with disk usage.

##### Read-Only:
PyChan is a read-only application. Currently you cannot post to boards or reply to anything. This is, again, a limitation of the 4Chan API (the API itself is specifically stated as being read-only). It's hard to get around this problem due to the Captcha system 4Chan has in place, meaning it takes more than a POST/PUT request to post or reply. This is done on purpose and protects the site from spam/bots. 
