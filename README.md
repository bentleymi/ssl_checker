
Copyright 2022 Splunkable LLC

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

# ssl_checker
Packaged and distributed for public consumption here -> https://splunkbase.splunk.com/app/3172/

THIS APP WORKS ON SPLUNK CLOUD, ENTERPRISE AND LIGHT - BUT NOT UNIVERSAL/LIGHT FORWARDERS

Does not work on Universal Forwarders / Light Forwarders
Requires Splunk's built in Python 3 and OpenSSL binaries / libraries
Tested on Generic AWS Linux

#Installation Instructions

1st - Install the app, and restart Splunk
2nd - Setup your own Splunk searches, alerts, dashboards (see index=main by default)

#Troubleshooting:

Be sure the python scripts in /bin are executable ("chmod +x /path/to/ssl_checker/bin/.py")
Be sure to restart Splunk after configuration (Enables scripted inputs)
Check for logged errors ("index=_internal log_level=err OR log_level=warn ssl_checker")
Contact the author via contact on splunkbase or by tagging @jkat54 on answers.splunk.com

#Bug Reporting & Code Contributions:
https://github.com/bentleymi/ssl_checker

Change Log v4.1.0:
-The cloud compatible version:
--Updated example dashboard to address jQuery vuln
--Changed to fully automated, just install and profit now
--Removed setup page and ability to manually specify locaitons of certs to scan
--Additional python3 & cloud compatibility fixes
--Added app manifest to define workloads
--Added sc_admin permission to view/edit

Change Log v4.0.2:
-Updated example dashboard
-Fixed bug in setup.xml

Change Log v4.0.1:
Successfully implemented python3 compatibility

Change Log v4.0:
Failed attempt at python3 compatiblity


Change Log v3.1:

Fixed issue with certs on caPaths not being correctly detected in automated detection mode
Added better Instructions to setup.xml
Removed index name from "Certificate Expiration Overview" dashboard underlying search

Change Log v3.0:

Added Automatic Discovery Mode
Added Certificate Expiration Overview dashboard
Changed default CRON schedules to 0 0 * * from * * * *

Change Log v2.0:

Added ssl.conf file & REST endpoints for managing SSL certificates
Added props.conf to force DATETIME_CONFIG = CURRENT
Added setup.xml for enabling inputs and setting paths to certificates on both Window & Linux systems
Changed interval to every minute on all inputs but they are disabled by default

Change Log v1.01:

Disabled inputs by default
Changed interval to 0 0 * * * on all inputs
Disabled logging of duplicate data to _internal index via splunk.mining.dcutil
