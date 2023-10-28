# Lazy DNS Recon

Lazy DNS Recon is a Python script designed to automate various DNS reconnaissance and information gathering tasks. It utilizes the Selenium WebDriver to interact with web services, conduct Google searches with specific queries related to the target domain, and gather information from various online tools.

## Features

- Automated DNS reconnaissance for a specified domain.
- Utilizes Google search to find specific information related to the target domain.
- Gathers information from various online tools and services.
- Implements random user-agent for web requests.
- Interacts with the dnstwister service to find similar-looking domain names that could be used for phishing attacks.

## Requirements

- Python 3.x
- Selenium WebDriver
- Firefox Browser and GeckoDriver

## Installation

1. Clone the repository:

   ```bash
   [git clone https://github.com/pentestfunctions/lazydnsrecon](https://github.com/pentestfunctions/lazydnsrecon.git)
   cd lazydnsrecon
   ```
Install the required Python packages:

```bash
pip install -r requirements.txt
```

Make sure you have Firefox and GeckoDriver installed on your system.

Usage
```bash
python lazydnsrecon.py -d <target_domain>
```

-d, --domain: Specify the target domain for DNS reconnaissance.

Example
```bash
python lazydnsrecon.py -d example.com
```
