import yaml


def convert_json_to_yaml(data):
    return yaml.dump(data)


def convert_yaml_to_json(data):
    return yaml.load(data, Loader=yaml.FullLoader)


def get_cookies_dict_list_from_string(header_string=None, domain=""):
    """

    string_1 = "memclid=9135473f-0ad2-4cebc279; nfvdid=BQFmAAEBEE0nZkm;
    a = get_headers_from_response_data(string_1)
    print(a)


    :param header_string:
    :param domain:
    :return:
    """
    cookies = []
    for cookie in header_string.split(";"):
        _ = cookie.split("=")
        cookies.append({
            "name": _[0].strip(),
            "value": _[1],
            # "domain": domain
        })

    return cookies


def get_elapsed_time(start_time=None, end_time=None):
    dt = end_time - start_time
    dt_ms = dt.total_seconds() * 1000  # milliseconds
    return "%.2f ms" % dt_ms
