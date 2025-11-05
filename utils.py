import re
import random
import string
from urllib.parse import urlparse
from datetime import datetime, timedelta
from ipaddress import ip_address, IPv4Address, IPv6Address

def is_valid_url(url):
    """
    Validate URL format and security constraints.

    Args:
        url (str): URL to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not url or not isinstance(url, str):
        return False, "URL é obrigatória"

    url = url.strip()
    if not url:
        return False, "URL é obrigatória"

    # Check if URL has protocol
    if not url.startswith(('http://', 'https://')):
        return False, "URL deve começar com http:// ou https://"

    try:
        parsed = urlparse(url)

        # Check if hostname exists
        if not parsed.hostname:
            return False, "URL inválida"

        # Security: Reject localhost and private IP ranges
        try:
            ip = ip_address(parsed.hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                return False, "URLs localhost e privadas não são permitidas"
        except ValueError:
            # Not an IP address, continue with hostname validation
            pass

        # Additional security checks
        hostname = parsed.hostname.lower()
        if hostname in ['localhost', '127.0.0.1', '::1']:
            return False, "URLs localhost não são permitidas"

        # Check for valid URL structure
        if not parsed.scheme in ['http', 'https']:
            return False, "Apenas URLs HTTP e HTTPS são permitidas"

        return True, None

    except Exception:
        return False, "URL inválida"

def is_valid_custom_code(code):
    """
    Validate custom short code.

    Args:
        code (str): Custom code to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not code:
        return True, None  # Optional field

    code = code.strip()

    # Length validation
    if len(code) < 3 or len(code) > 50:
        return False, "Código personalizado deve ter entre 3 e 50 caracteres"

    # Character validation - allow alphanumeric, hyphens, underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', code):
        return False, "Código personalizado deve conter apenas letras, números, hífens e sublinhados"

    # Reserved codes
    reserved_codes = ['api', 'static', 'www', 'mail', 'ftp', 'admin', 'root', 'www']
    if code.lower() in reserved_codes:
        return False, f"'{code}' é um código reservado"

    return True, None

def generate_random_code(length=6):
    """
    Generate a random alphanumeric code.

    Args:
        length (int): Length of code to generate

    Returns:
        str: Random code
    """
    charset = string.ascii_letters + string.digits
    return ''.join(random.choices(charset, k=length))

def parse_expiration_time(expires_in):
    """
    Parse expiration time from string format.

    Args:
        expires_in (str): Expiration time in format like "1h", "1d", "1w", "1m"

    Returns:
        datetime: Expiration datetime or None if no expiration
    """
    if not expires_in:
        return None

    expires_in = expires_in.lower().strip()

    # Parse the number and unit
    match = re.match(r'^(\d+)([hdwm])$', expires_in)
    if not match:
        return None

    number, unit = match.groups()
    number = int(number)

    # Calculate timedelta based on unit
    if unit == 'h':  # hours
        delta = timedelta(hours=number)
    elif unit == 'd':  # days
        delta = timedelta(days=number)
    elif unit == 'w':  # weeks
        delta = timedelta(weeks=number)
    elif unit == 'm':  # months (approximate as 30 days)
        delta = timedelta(days=number * 30)
    else:
        return None

    # Calculate expiration date
    expiration = datetime.utcnow() + delta

    # Limit maximum expiration to 5 years
    max_expiration = datetime.utcnow() + timedelta(days=5 * 365)
    if expiration > max_expiration:
        expiration = max_expiration

    return expiration

def format_datetime(dt):
    """
    Format datetime for display in Portuguese.

    Args:
        dt (datetime): DateTime object

    Returns:
        str: Formatted date/time string
    """
    if not dt:
        return "Nunca"

    # Convert to Brazil timezone (UTC-3) for display
    brazil_time = dt - timedelta(hours=3)
    return brazil_time.strftime('%d/%m/%Y %H:%M')

def format_relative_time(dt):
    """
    Format datetime as relative time in Portuguese.

    Args:
        dt (datetime): DateTime object

    Returns:
        str: Relative time string
    """
    if not dt:
        return "Nunca"

    now = datetime.utcnow()
    diff = now - dt

    if diff.days == 0:
        if diff.seconds < 60:
            return "Agora há pouco"
        elif diff.seconds < 3600:
            minutes = diff.seconds // 60
            return f"Há {minutes} minuto{'s' if minutes != 1 else ''}"
        else:
            hours = diff.seconds // 3600
            return f"Há {hours} hora{'s' if hours != 1 else ''}"
    elif diff.days == 1:
        return "Ontem"
    elif diff.days < 30:
        return f"Há {diff.days} dia{'s' if diff.days != 1 else ''}"
    elif diff.days < 365:
        months = diff.days // 30
        return f"Há {months} mês{'es' if months != 1 else ''}"
    else:
        years = diff.days // 365
        return f"Há {years} ano{'s' if years != 1 else ''}"