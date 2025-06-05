# -*- coding: utf-8 -*-
import re
import urllib3
import argparse
import requests
from bs4 import BeautifulSoup

from urllib.parse import urljoin, urlparse
from requests.exceptions import SSLError, RequestException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

visited = set()

def crawl(url, base_url, ssl_check, depth, max_depth, output, prefix=''):
    if depth > max_depth or url in visited:
        return

    output.append(f"{prefix}{url}")

    html = fetch_html(url, ssl_check)
    if not html:
        return
    soup = BeautifulSoup(html, 'html.parser')

    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)
        parsed = urlparse(full_url)

        # Nettoyage des ancres et paramètres
        clean_url = parsed.scheme + "://" + parsed.netloc + parsed.path.rstrip('/')
        
        if clean_url.startswith(base_url) and clean_url not in visited:
            links.add(clean_url)

    for link in sorted(links):
        crawl(link, base_url, ssl_check, depth + 1, max_depth, output, prefix + '\t')

    visited.add(url)


def fetch_html(url, ssl_check=True):
    try:
        response = requests.get(url, timeout=5, verify=ssl_check)  # verify=True par défaut
        if 'text/html' in response.headers.get('Content-Type', ''):
            return response.text
    except SSLError:
        print(f"[⚠️ SSL ERROR] Problème de certificat sur : {url}")
        try:
            print(f"[⚠️ RETRYING] without SSL check")
            response = requests.get(url, timeout=5, verify=False)  # Désactiver la vérification SSL
            if 'text/html' in response.headers.get('Content-Type', ''):
                return response.text
        except Exception as e:
            print(f"[⚠️ GENERAL ERROR] {url} : {e}")
    except RequestException as e:
        print(f"[⚠️ REQUEST ERROR] {url} : {e}")
    return None


def url_to_filename(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc
    # Remplacer les caractères non autorisés (ex: ':' ou '/') par un underscore
    safe_filename = re.sub(r'[^\w\-_.]', '_', hostname)
    return f"{safe_filename}.txt"


def main(start_url="https://example.com", max_depth=2, ssl_check=True):
    print(f"input URL: {start_url} with max depth {max_depth} SSL {ssl_check}")
    base_url = f"{urlparse(start_url).scheme}://{urlparse(start_url).netloc}"

    output = []
    crawl(start_url, base_url, ssl_check, 0, max_depth, output)

    filename = url_to_filename(start_url)
    # Écriture dans un fichier texte
    with open(filename, "w", encoding="utf-8") as f:
        for line in output:
            f.write(line + "\n")

    print(f"Results in {filename}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Explore un site web et génère une arborescence tabulée."
    )
    parser.add_argument("start_url", type=str, help="URL de départ du site (ex: https://example.com)")
    parser.add_argument("-d", "--depth", type=int, default=2, help="Profondeur maximale d'exploration (défaut: 2)")
    parser.add_argument("-w", "--ssl", action="store_true", help="Désactiver la vérification SSL (non recommandé, optionnel)")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    start_url = args.start_url
    max_depth = args.depth
    verify_ssl = not args.ssl
    main(start_url, max_depth, verify_ssl)
