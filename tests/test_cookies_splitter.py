from browser_engine.utils import get_cookies_dict_list_from_string, convert_json_to_yaml

cookie_string = "memclid=9135; nfvdid=BQFmAAEBEE0nZkKWaz0OULAVLBkLg1RgsxYtr0CbTa43Pe9qr%2Fd9gIH98p4OCZuOCPGk8GkuBWo7ccSgx1JS8POHJ%2FMBzANkiRGGcgxv7GOSghBXvDwPOLkFgddDK5AHv; clSharedContext=706154e2--4caf-ab53-6e4b8dc587ef; pas=%7B%22supplementals%22%3A%7B%22muted%22%3Atrue%7D%7D; SecureNetflixId=v%3D2%%.%26dt%; NetflixId=ct%3DBQAOAAEBEKc_vbRrnJoyNv---WcDrFJTeNyPla2sv7ol_JAXMlpitur---Ax12BoW6rcnreRGEGlq-Hc7ZLfrC6sV7tt--a3vjp5doKVmmZ-VYXLjj2ccKFN6GjQIPoaFznO8dK2lVo1CxtyzafL0j5zZunRFZBPDFwwg5KCN8oUKiTXXe3r4bN6wqR3--..%26bt%3Ddbl%26ch%.%26v%3D2%26mac%3DAQEAEAABABR5_eZ31mik5DZ_BWN8skU0ZfjLNrBoljE.; playerPerfMetrics=%7B%22uiValue%22%3A%7B%%22%3A985%2C%22throughputNiqr%22%3A3.192376810215789%7D%2C%22mostRecentValue%22%3A%7B%22throughput%22%3A985%2C%22throughputNiqr%22%3A3.192376810215789%7D%7D; profilesNewSession=0; lhpuuidh-browse-Z5UIWCZ=IN%3AEN-IN%3A2c88dce0-a21d-44fa-a479-87878ac17dca_ROOT; lhpuuidh-browse-Z5UIWCZARJGMWSWTOPU-T=15745883643"
a = get_cookies_dict_list_from_string(cookie_string, domain="netflix.com")
print(a)
yaml_str = convert_json_to_yaml(a)
print(yaml_str)
