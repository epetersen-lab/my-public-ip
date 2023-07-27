import requests

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class HttpBinOrg:

    def __init__(self):
        self.BASE_URL = "https://httpbin.org"

    def ip(self):
        response = requests.get(f"{self.BASE_URL}/ip")
        response.raise_for_status()
        try:
            return response.json()['origin']
        except (KeyError, requests.exceptions.JSONDecodeError):
            return "Invalid response from host"


def main():
    try:
        print(HttpBinOrg().ip())
        exit(EXIT_SUCCESS)
    except Exception as e:
        print(e)
        exit(EXIT_FAILURE)


if __name__ == "__main__":
    main()
