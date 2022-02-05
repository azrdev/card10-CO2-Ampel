# Ampel

This app will show you current CO2 concentration (ppm) and the Index for Air Quality of your environment, and light LEDs accordingly, like a traffic light.

This is not based on anything seriously scientific but it could be taken as a clue you need to ventilate the room.

Based on [@schneider's work](https://git.card10.badge.events.ccc.de/card10/firmware/-/merge_requests/380) for presenting [BME680 sensors](https://git.card10.badge.events.ccc.de/card10/hardware/-/raw/master/datasheets/bosch/BST-BME680-DS001.pdf) to Epicardium and Pycardium API.
Also based on [C10VID - Demo for the BSEC air quality sensors](https://github.com/ketsapiwiq/c10vid)

This is a card10 app (CCCamp badge).

`bsec_enable = true` has to be in your `card10.cfg`.

You will need to flash firmware >= v1.17 according to the card10 documentation.

