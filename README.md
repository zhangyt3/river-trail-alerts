# River Trail Alerts

Scraping the [River Trail Status Page](https://www.theforks.com/events/skating-trail-and-park-conditions)
to find out whether or not each segment is open.

You can run `handler.py` as a regular Python script:

```
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python handler.py
```

To deploy and test in your AWS account (assuming you've [set up your AWS credentials in your AWS CLI already](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)):

```
sls deploy

sls invoke --function update
```
