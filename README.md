# River Trail Alerts

Periodically scraping the [River Trail Status Page](https://www.theforks.com/events/skating-trail-and-park-conditions) to find out whether or not each segment is open. If there is a change, a notification will be sent out via your chosen method.

To deploy and test in your AWS account (assuming you've [set up your AWS credentials in your AWS CLI already](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)):

```
# Create a virtual environment and install Python dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Serverless Framework and plugins
npm install -g serverless
npm install

# Deploy to your AWS account and invoke Lambda function
sls deploy
sls invoke --function update
```

