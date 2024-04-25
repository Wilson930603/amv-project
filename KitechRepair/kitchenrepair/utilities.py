def striped(value):
    """
    The function returns the cleaned value by first stripping the leading and trailing white spaces from the value using the "strip()" method. 
    Then, it removes the "$" symbol from the value by calling the "strip('$')" method. This function can be used to clean scraped data such as 
    price information which may have unwanted symbols or white spaces.
    """
    return value.strip().strip("$").replace("\n", " ")


def if_na(value):
    if value == None or value == "":
        return "N/A"
    return striped(value)


def return_headers():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://www.pigeonandpoodle.com/customer/account/",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }
    return headers
