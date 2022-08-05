dkkt-project
---

This project built for Capstone Project in FPT University.

This Project was built for Cloud pentesting (Azure specificed) purpose.

What will this tool do?
---
- Active scanning on that web site to get all resource like (links, phones, emails)
- Using [cloud_enum](https://github.com/initstring/cloud_enum) (optimized) to brute force other resource (thread = 10)
- Export collected data to report (html/txt)
- Following [Oh365UserFinder](https://github.com/dievus/Oh365UserFinder) -> build password spraying
- Using [cs_suite](https://github.com/SecurityFTW/cs_suite) (maintained) to overall pentesting Azure resource

Disclaimer
---
**This project is built for education purpose. Any problem is user own risk.**

Requirement
---
- Operating System OSX or Linux only
- Python version 3.5 or above (working well on Python3.10)
- python3-pip
- jq
- azure-cli version 2.32 or above
Installation
---
```sh
sudo apt-get install jq
sudo apt-get install python3-pip
pip install -r requirements.txt
sudo apt-get install azure-cli=2.34.1-1~buster (Kali Distribution)
```

How to use
---
```sh
python3 dkkt-project.py
```
In here you will have option `-q` which will not show the banner. When the script activated. There is an option table, chose and give the required information from it.

```
==========================================================
     _ _    _    _                        _           _
  __| | | _| | _| |_      _ __  _ __ ___ (_) ___  ___| |_
 / _` | |/ / |/ / __|____| '_ \| '__/ _ \| |/ _ \/ __| __|
| (_| |   <|   <| ||_____| |_) | | | (_) | |  __/ (__| |_
 \__,_|_|\_\_|\_\\__|    | .__/|_|  \___// |\___|\___|\__|
                         |_|           |__/
==========================================================

# Note: Every company will have their own model, so this
project built to make for demonstration.
# Disclaimer: This tools make for education purpose, any
problem will be your own risk.

----------------------------------------------------------


Option 1: Reconnaissance the targeted website
Option 2: DNS Scanning
Option 3: Data extracting (web application)
Option 4: Password spraying
Option 5: Overall pentesting
Option 6: Exit

>> Enter your option: 
```

Reference
---

- cloud_enum - https://github.com/initstring/cloud_enum
- Oh365UserFinder - https://github.com/dievus/Oh365UserFinder
- cs-suite - https://github.com/SecurityFTW/cs-suite
