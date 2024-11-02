# Beacon (AP Imposter)
Beacon is a simple program that I put together in order to practice using beacon frames within networking. This application simply broadcasts the information you provide it and then all nearby devices can see that a new wireless access point has become available. When attempting to connect to this network you will be met with failure as it is not currently configured to handle network traffic, however, this may come in future.
# Application Usage
## Issues:
- There were issues during development regarding the choice of interface. If not **specifically** defined then the application will have trouble determining which interface the beacon frames are going to be transmitted from. This is not by my design, but due to one of the dependancies of this tool.
## Support:
Currently, this tool is only supported on **Linux** as it uses implementations that are only available on **Linux**. Support for **Windows** is planned and will be implemented in future.
## Requirements:
- Scapy Library
```
python -m pip install ./requirements.txt
```
## Summary:
This application in its current state is virtually harmless, however, I **DO NOT** condone the malicious use of this software unless you have been given **EXPLICIT** concent from any parties involved. In future, a version of this software may become available that supports the handling of network traffic on that access point.