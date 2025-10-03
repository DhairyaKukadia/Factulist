import whois
import requests
import socket
from datetime import datetime

def fetch_domain_metrics(domain: str):
    """
    Fetch basic domain metrics for credibility signals:
    - Age of domain
    - Valid SSL certificate
    - Online status (reachable)
    """

    metrics = {
        "domain": domain,
        "reachable": False,
        "ssl_valid": False,
        "domain_age_years": None
    }

    # Check reachability
    try:
        resp = requests.get(f"http://{domain}", timeout=5)
        metrics["reachable"] = resp.status_code == 200
    except Exception:
        metrics["reachable"] = False

    # Check SSL validity
    try:
        resp = requests.get(f"https://{domain}", timeout=5, verify=True)
        if resp.status_code == 200:
            metrics["ssl_valid"] = True
    except Exception:
        metrics["ssl_valid"] = False

    # Domain age via whois
    try:
        w = whois.whois(domain)
        if isinstance(w.creation_date, list):  # some whois libs return list
            creation_date = w.creation_date[0]
        else:
            creation_date = w.creation_date
        if creation_date:
            metrics["domain_age_years"] = (datetime.now() - creation_date).days // 365
    except Exception:
        metrics["domain_age_years"] = None

    return metrics


if __name__ == "__main__":
    test_domains = ["bbc.com", "foxnews.com", "infowars.com"]
    for d in test_domains:
        print(fetch_domain_metrics(d))
