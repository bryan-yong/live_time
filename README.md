# live_time
LiveTime Notifications

This tool was developed so that whenever ticket is created with any keyphrases as the subject it will send an alert out.
Tool is not meant to be sold or monetarized and just solely for use of those on the Desktop Support team for better productivity.

How the tool works:
- Opens a browser window for automated test software
- Logs in to LiveTime account
- Navigates to main queue
- Scans queue for tickets with subjects containing key phrases
- - If ticket meeting requirement is found send an alert
- - If no ticket is found idle set amount of time and refresh to scan again
- Any triggered alerts will store triggered ticket and compare queue with cache to not send repeat alerts
- This should all be controlled with a while loop to run x amount of time
- time python library is imported to control how long the script runs

Removed URL leading to ticketing system as it is used by my organization.
