# OSINT Toolkit – Tools

This document contains the OSINT tools supported or planned for integration into the OSINT Toolkit.

> **Note:** The OSINT Toolkit launches or references third-party tools. These tools belong to their respective developers and are subject to their own licenses and terms of use.

---

## Table of Contents

* [Username](#username)
* [OSINT Frameworks](#osint-frameworks)
* [Domain & DNS](#domain--dns)
* [Metadata](#metadata)
* [Accounts](#accounts)
* [Network](#network)
* [Additional Tools](#additional-tools)
* [License Information](#license-information)
* [Security and Responsible Use](#security-and-responsible-use)
* [Adding New Tools](#adding-new-tools)

---

# Username

## Sherlock

**Category:** Username OSINT
**Purpose:** Searches for a username across many publicly accessible websites.

**Typical uses:**

* Searching for public profiles
* Finding username reuse
* Comparing usernames across different platforms

**Example:**

```bash
sherlock username
```

**Project:**
https://github.com/sherlock-project/sherlock

**License:** MIT

---

# OSINT Frameworks

## SpiderFoot

**Category:** OSINT Automation
**Purpose:** Automates the collection and correlation of publicly available information.

**Typical uses:**

* Domains
* IP addresses
* Public profiles
* DNS information
* Infrastructure
* General OSINT research

**Example:**

```bash
spiderfoot -l 127.0.0.1:5001
```

**Project:**
https://github.com/smicallef/spiderfoot

**License:** GPL-2.0

---

## Recon-ng

**Category:** OSINT Framework
**Purpose:** A modular framework for structured OSINT research.

**Typical uses:**

* Domain research
* Public information gathering
* Modular reconnaissance
* Structured results

**Start:**

```bash
recon-ng
```

**Project:**
https://github.com/lanmaster53/recon-ng

**License:** GPL-3.0

---

# Domain & DNS

## theHarvester

**Category:** Domain OSINT
**Purpose:** Collects publicly available information related to domains.

**Typical information:**

* Publicly discoverable email addresses
* Hostnames
* Domains
* Search engine results

**Example:**

```bash
theHarvester -d example.com -b bing
```

**Project:**
https://github.com/laramies/theHarvester

**License:** MIT

---

## Amass

**Category:** Domain Reconnaissance
**Purpose:** Discovers publicly observable relationships between domains, subdomains, and infrastructure.

**Example:**

```bash
amass enum -passive -d example.com
```

**Project:**
https://github.com/owasp-amass/amass

**License:** Apache-2.0

---

## WHOIS

**Category:** Domain Information
**Purpose:** Retrieves publicly available domain registration information.

**Example:**

```bash
whois example.com
```

**Information:**
https://www.iana.org/whois

---

## dig

**Category:** DNS
**Purpose:** Performs DNS queries for publicly available DNS records.

**Examples:**

```bash
dig example.com
dig MX example.com
dig TXT example.com
```

**Documentation:**
https://bind9.readthedocs.io/

---

# Metadata

## ExifTool

**Category:** Metadata
**Purpose:** Reads and analyzes metadata from many different file formats.

**Supported examples:**

* JPEG
* PNG
* PDF
* RAW images
* Audio/video files

**Example:**

```bash
exiftool image.jpg
```

ExifTool can display technical information contained in files and their metadata.

**Project:**
https://exiftool.org/

**License:** Perl Artistic License / GPL

---

# Accounts

## GHunt

**Category:** Account OSINT
**Purpose:** Researches information that may be publicly visible in connection with Google accounts.

**Example:**

```bash
ghunt --help
```

**Project:**
https://github.com/mxrch/GHunt

**License:** MIT

---

# Network

## Nmap

**Category:** Network Discovery
**Purpose:** Discovers network services and reachable ports.

**Example:**

```bash
nmap -sV example.com
```

Nmap can provide information about reachable services and their versions.

**Project:**
https://nmap.org/

**License:** Nmap Public Source License

> ⚠️ **Important:** Only scan systems that you own or have explicit permission to test.

---

# Additional Tools

The toolkit can be expanded with additional tools in the future.

Possible integrations include:

* **Maigret** – Username OSINT
* **Maltego** – Visual relationship mapping
* **Metagoofil** – Metadata research
* **Photon** – Web crawling
* **Subfinder** – Passive subdomain discovery
* **dnsx** – DNS reconnaissance
* **httpx** – HTTP service analysis
* **Sherlock** – Username research
* **SpiderFoot** – Automated OSINT research

New integrations should always respect the respective project's license and terms of use.

---

# License Information

The **OSINT Toolkit** itself is distributed under the license specified in this repository.

The tools listed in this document are **separate third-party projects**.

The OSINT Toolkit's license does not automatically apply to these third-party tools.

Each external tool is subject to:

1. Its own open-source license
2. Its project's terms of use
3. The terms of any external data sources it accesses

If third-party source code is copied or directly integrated into this project, its license requirements must be reviewed and followed.

---

# Security and Responsible Use

The OSINT Toolkit is intended for:

* Education and learning
* OSINT research
* CTFs and security labs
* Researching your own digital footprint
* Authorized security assessments
* Analysis of publicly available information

### Not intended for

The toolkit should not be used to:

* Bypass access controls
* Steal passwords or credentials
* Compromise private accounts
* Obtain information that is not publicly available
* Harass, stalk, or target individuals
* Scan or attack systems without authorization

For network and security-related tools:

> **Only investigate systems for which you have explicit authorization.**

Users are responsible for complying with all applicable laws, regulations, terms of service, and license requirements.

---



