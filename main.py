from flaresolverr import FlaresolverrClient

_PROXY_URL = "http://192.168.1.128:9988"

if __name__ == "__main__":

    client = FlaresolverrClient("http://localhost:8191")

    session_id = client.create_flaresolverr_session(proxy=_PROXY_URL, name="my_session")
    print(session_id)

    try:
        url = "http://ip-api.com/json"
        res = client.flare_solverr_get(url, {
            "session": session_id,
        })
        print(res["solution"]["status"])
        print(res["solution"])
    finally:
        client.destroy_flaresolverr_session(session_id)