from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
from urllib.parse import urlparse
import datetime

PORT = 8000

# Expanded Blacklist
BLACKLISTED_DOMAINS = [
    "scam.com", "phishingsite.com", "fraudbank.com", "malware-site.net",
    "getrichquick.com", "login-alert.com", "freeprizes.net", "fakebank.co",
    "unsecure-payments.org", "paypal-alerts.com", "badurl.biz", "verify-update.com",
    "claimprize.xyz", "credit-alert.com", "secure-authenticate.net"
]

PHISHING_KEYWORDS = [
    "login", "verify", "secure", "bank", "paypal", "update", "confirm",
    "account", "password", "billing", "urgent", "click", "restricted",
    "fraud", "unauthorized", "alert", "suspicious", "locked", "reset",
    "credentials", "authentication", "transaction", "payment", "credit",
    "debit", "card", "statement", "invoice", "refund", "charge", "balance",
    "overdue", "limit", "transfer", "security", "protection", "disabled",
    "immediately", "asap", "act now", "attention", "warning", "risk", "threat",
    "compromise", "breach", "validate", "temporary hold", "suspend", "pending",
    "danger", "malware", "infected", "support", "helpdesk", "admin",
    "system error", "critical alert", "firewall", "antivirus", "license expired",
    "security alert", "access denied", "encryption", "irs", "tax", "fine",
    "police", "court", "social security", "gov", "passport", "aadhar", "pan card",
    "email access", "mailbox", "outlook", "gmail", "sign in", "otp", "phishing",
    "spoof", "unsubscribe", "click below", "you have won", "congratulations",
    "prize", "lottery", "bonus", "reward", "gift card", "claim now", "free",
    "voucher", "wire transfer", "bitcoin", "crypto", "wallet", "airdrop",
    "investment", "donation", "inheritance", "beneficiary", "trust fund",
    "ceo", "manager", "hr department", "dear customer", "case number",
    "ticket number", "scam", "hoax", "fake", "compromised", "reactivate",
    "unlock account", "verify identity", "leaked", "dangerous"
]

def extract_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc if parsed.netloc else parsed.path
    domain = domain.lower().replace("www.", "").strip()
    return domain

def is_phishing(url):
    url = url.lower()
    domain = extract_domain(url)

    for blacklisted in BLACKLISTED_DOMAINS:
        if blacklisted in domain:
            return True

    if any(keyword in url for keyword in PHISHING_KEYWORDS):
        return True

    if len(domain.split('.')) > 3:
        return True

    if re.match(r"\d{1,3}(\.\d{1,3}){3}", domain):
        return True

    return False

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == '/check_url':
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len).decode('utf-8')
            data = json.loads(post_body)
            url = data.get("url", "")

            result = is_phishing(url)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"is_phishing": result}).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

def run():
    print(f"Starting server on port {PORT}...")
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
