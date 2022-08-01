DKKT-Project
---

This project built for Capstone Project in FPT University.
This Project built for azure scanning purpose.

What will this tool do?
---
Active scanning on that web site to get all resource like (links, phones, emails)

Using [Cloud Enum](https://github.com/initstring/cloud_enum) (optimized) to brute force other resource (thread = 10)

Export to html or txt

Disclaimer
---
**This project is built for education purpose. Any problem is user own risk.**

Requirement
---
Python version 3.5 or above

Installation
---
```sh
pip install -r requirements.txt
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
Option 3: Password spraying
Option 4: Extract data (HTML/TXT)
Option 5: Exit

>> Enter your option: 
```

