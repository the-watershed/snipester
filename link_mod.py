import re

def is_valid_link(link):
    """
    Validate the provided link against a regex pattern.
    Returns True if the link is valid, otherwise False.
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, link) is not None

def strip_html_link(link):
    """
    Extract the base eBay item link from a full HTML link or other formats.
    Returns the cleaned link or None if no valid link is found.
    """
    # Handle standard eBay item links
    match = re.search(r'(https://www\.ebay\.com/itm/\d+)', link)
    if match:
        return match.group(1)

    # Handle shortened eBay links (e.g., https://ebay.us/xyz123)
    match = re.search(r'(https://ebay\.us/\w+)', link)
    if match:
        return match.group(1)

    # Handle embedded links in HTML (e.g., <a href="https://www.ebay.com/itm/1234567890">)
    match = re.search(r'href="(https://www\.ebay\.com/itm/\d+)"', link)
    if match:
        return match.group(1)

    # If no valid link is found, return None
    return None

def crop_link(link):
    """
    Crop the link to only include the part before the "?" character.
    """
    return link.split('?')[0]  # Get the part before the "?"
