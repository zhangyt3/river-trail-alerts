# River Trail Alerts

Right now there's just a Python script to scrape the [River Trail Status Page](https://www.theforks.com/events/skating-trail-and-park-conditions)
to find out whether or not each segment is open.

Usage:

```
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python scrape.py
```

The output should look something like:

```
Rink Under the Canopy is closed
Hockey Rink at CN Stage is closed
Crokicurl is closed
Trails near CN Stage is closed
Trails across rail bridge is closed
Upper Trails is closed
The Forks Port Rink is closed
The Forks Port to Queen Elizabeth Way is closed
Queen Elizabeth Way to Churchill Drive is closed
Churchill Drive to St. Vital Bridge is closed
The Forks Port to Donald Street is closed
Donald Street to Legislature is closed
Legislature to Osborne Bridge is closed
Osborne Bridge to Hugo Docks is closed
The Forks Port Access Ramp is closed
The Forks Port Stairs is closed
Donald is closed
Osborne is closed
Hugo Docks is closed
Queen Elizabeth Way is closed
Balsam Place is closed
St. Vital Bridge is closed
