import yaml


def convert_json_to_yaml(data):
    return yaml.dump(data)


def convert_yaml_to_json(data):
    return yaml.load(data, Loader=yaml.FullLoader)


def get_cookies_dict_list_from_string(header_string=None, domain=""):
    """

string_1 = "memclid=9135473f-0ad2-4cebc279; nfvdid=BQFmAAEBEE0nZkKWazFZ2n9T%2Fe27bYLiLIqccQcZmDnx%2Fd9gIH98p4OCZuOCPGk8GkuBWo7ccSgx1cgxv7GOSghBXvDwPOLkFgddDK5AHv; clSharedContext=706154e2-68ed-4caf--6e4b8dc587ef; SecureNetflixId=v%3D2%26mac%-NUpj9uJV-FPE.%26dt%3D1574329073324; NetflixId=ct%-y3HbNpCB8HDy6HDwIwykji_zDG_Ms5wpjQQxHGtRuK-s5ZN0K8KMc-83qkZ2U9lt00-mL1zaOPS934q8oMG1d4e42Pzfojck4-ZhWv5-R--CamPY6EhFeP7KbLtfGlbAqhQmzx9rSK1YTcOmaNd_F5-TP8Rlk5i_MOcaqgbihOSWd_0ULcz87-kNFUuiX2A6P1wfTj4IHchGB0eHMkVwbagPfbvEKkewxidNS4U9eob_4wL9lUOWrPH-zsAeA_R3HQXfbparVz_sDwurx8Acbcz8Yg1rAIah9bdenqdpku0BvdBGLdidv-hTntZI1iWhh24IL7jM8H-Ue7SZXKiSutrT34.%26bt%3Ddbl%26ch%3DAQEAEAABABRIbF3C3aztynV7C_ZraQTokxHsDYQFvto.%26v%3D2%26mac%3DAQEAEAABABSwNARfFNwvQdhYugxtEpHl6cX7yJKUoTY.; lhpuuidh-browse-Z5UIWCZARJGQVCMI5YBWSWTOPU=IN%3AEN-IN%3A0a0efb9a-878f-4748-9665-0200c17f5ab1_ROOT; lhpuuidh-browse-Z5UIWCZARJGQVCMI5YBWSWTOPU-T=1574329080290; lhpuuidh-browse-Z5UIWCZARJGQVCMI5YBWSWTOPU-NB=IN%3AEN-IN%3A665abd55-e241-4aab-b037-3dcae0463d58_ROOT; lhpuuidh-browse-Z5UIWCZARJGQVCMI5YBWSWTOPU-NB-T=1574329240443; profilesNewSession=0; pas=%7B%22supplementals%22%3A%7B%22muted%22%3Atrue%7D%7D; playerPerfMetrics=%7B%22uiValue%22%3A%7B%22throughput%22%3A965%2C%22throughputNiqr%22%3A3.192376810215789%7D%2C%22mostRecentValue%22%3A%7B%22throughput%22%3A965%2C%22throughputNiqr%22%3A3.192376810215789%7D%7D"

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
