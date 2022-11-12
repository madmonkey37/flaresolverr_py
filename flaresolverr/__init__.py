import json
from typing import Any, Dict, Optional
import requests
from urllib.parse import urljoin

# https://github.com/FlareSolverr/FlareSolverr


class FlaresolverrClient:
    def __init__(self, flaresolverr_host: str):
        self.flaresolverr_host = flaresolverr_host

    def _run_flare_solverr_command(self, command, extra=None):
        if not extra:
            extra = {}
        data = {
            "cmd": command,
        }
        data.update(extra)
        raw_data = json.dumps(data)
        res = requests.post(
            urljoin(self.flaresolverr_host, "v1"),
            headers={
                'Content-Type': 'application/json'
            },
            data=raw_data
        )
        return res.json()
        


    def flare_solverr_get(self, url, extra=None):
        if not extra:
            extra={}
        extra["url"]=url
        flare_solverr_res=self._run_flare_solverr_command(
            "request.get", extra=extra)

        if ("solution" not in flare_solverr_res):
            print("No proxy response: " + str(flare_solverr_res))
        return flare_solverr_res


    def create_flaresolverr_session(self, *, proxy: str, name: Optional[str]=None):
        args: Dict[str, Any]={
            "proxy": {
                "url": proxy,
            }
        }

        if name:
            args["session"]=name

        sessions_create_res=self._run_flare_solverr_command(
            "sessions.create", args)

        status=sessions_create_res["status"]
        if status != "ok":
            raise Exception("Failed to create session")

        session_id=sessions_create_res["session"]
        return session_id


    def destroy_flaresolverr_session(self, session_id: str):
        sessions_destroy_res=self._run_flare_solverr_command("sessions.destroy", {
            "session": session_id,
        })

        print(sessions_destroy_res)
        status=sessions_destroy_res["status"]
        if status != "ok":
            raise Exception("Failed to destroy session")
