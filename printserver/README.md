# Biller Print Server

Start server:

    cd /home/pi/server/
    python server.py

## Install server

Start with Raspbian, install these:

* cups: Driver for printing pdfs
* xhtml2pdf: HTML to pdf converter
* pip: Python installation tool


```
apt-get install cups cups-pdf python-cups
apt-get install python-pip python-dev
pip install xhtml2pdf
```

## Install printer

Add user 'pi' to group 'lpadmin' and restart cups service

    sudo usermod -a -G lpadmin pi
    service cups restart

## Optional

    apt-get update

avahi: Bonjour service that will recognize the printer in the network.

    apt-get install avahi-daemon