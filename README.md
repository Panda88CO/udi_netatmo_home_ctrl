
# Netatmo Weather Station NodeServer

Netatmo Weather Station NodeServer for PG3, PG3x
MIT license.

This node server integrated the Netatmo Weather Station. You will need account access to your Netatmo via the Netatmo Developer API https://dev.netatmo.com.  Log in and select My Apps and then Create  Fill in info and press save - This exposes a client ID and client secret. 
Start the node server under PG3 - go to configuration and enter client ID and client Secret.  Then restart.   First time you do this you should see a text box asking to authendicate.  Press the authendicate button - you should be taken to a new webpage where you login using you Netatmo id and password (used to generate the clientID etc).  Then press accept and you will be returned to the PG3 interface. 
After running a little the differnt main netatmo under the account should be listed in configuration.  By default all are active.  If you do not want one station included set the value to 0
Restart and you should be up and running

Good luck

## Installation

1. Backup Your ISY in case of problems!
2. Go to the Polyglot Store in the UI and install.
3. Add NodeServer in PG3x - NOTE PG3 is not supported as OAuth library does not work on PG3 
   Got ton configuration and enter clientId and client secret (see above)
   Restart
   Authendicate if asked
   Select weather stations to be used in configuration (1 for enable, 0 for disable)
   Restart node server
   Go to Admin console 

### Node Settings
The settings for this node are:

#### Short Poll
   * Query Weather Station instantaneous data. The default is 5 minutes - sends a heart beat as well 0->1 or 1 -> 0
#### Long Poll
   * Query Weather Station all data. Netatmo data is updated every 15 min or so.  The default is 30 minutes.

#### ClientID
   * Your Netatmo App Client ID

#### ClientSecret
   * Your Netatmo App Client Secret

#### TEMP_UNIT
   * C (default) of F

#### Diffetn Weather stations
   * Weather stations associated with teh account are listed - 1 to include 0 to disable 

## Requirements

   * PG3x ver 3.2.18 or greater
   * UDI_interfae 3.1.1 or greater


# Release Notes
code somewhat based on original NEtatmoWeather node server (depreciated due to new authendication methods)

- 0.1.0 02/07/2024
   - Initial version published to github - 
