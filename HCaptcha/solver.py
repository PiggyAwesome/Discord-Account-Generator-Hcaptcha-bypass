"""
HCaptcha bypass made by yours truly dropout.

Credits:
    _get_hsl: https://github.com/h0nde/py-hcaptcha/blob/main/hcaptcha/temp.py#L42
"""

import json
import math
import random
import base64
import urllib
import hashlib
import requests
from .exceptions import *
from datetime import date, datetime

class Solver:

    def __init__(self, host: str, sitekey: str) -> None:
        """
        class for bypassing / solving the captchas.
        """
        self._host = host
        self._sitekey = sitekey

        self.headers = {
            "Authority": "hcaptcha.com",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://assets.hcaptcha.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Language": "en-US,en;q=0.9"
        }

        self._config = self._site_config()

    def _generate_bypass_payload(self, movement: dict) -> str:
        """
        this basicly is the bypass right here,
        all it does is multiply the movement list by 10.000.
        By doing so it forces hcaptcha to respond with a overload hcaptcha UUID,
        I could have made it just multiply inside the json but it is easier to explain if I just have a function
        for it.
        """
        return movement * 5000

    def _mouse_movement(self) -> list:
        """
        generates the mouse movement data.
        You could just replace
        "random.randint(10, 25)" with "random.randint(50000, 100000)"
        and that would cause you to not need self._generate_bypass_payload()
        """
        movement = []

        for x in range(20000):
            x_movement = random.randint(15, 450)
            y_movement = random.randint(15, 450)
            rounded_time = round(datetime.now().timestamp())
            movement.append([x_movement, y_movement, rounded_time])

        return movement

    def _get_hsl(self) -> str:
        """
        this part takes the req value inside the getsiteconfig and converts it into our hash, we need this for the final step.
        (thanks to h0nde for this function btw, you can find the original code for this at the top of the file.)
        """
        x = "0123456789/:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        req = self._config["req"].split(".")

        req = {
            "header": json.loads(
                base64.b64decode(
                    req[0] +
                    "=======").decode("utf-8")),
            "payload": json.loads(
                base64.b64decode(
                    req[1] +
                    "=======").decode("utf-8")),
            "raw": {
                "header": req[0],
                "payload": req[1],
                "signature": req[2]}}

        def a(r):
            for t in range(len(r) - 1, -1, -1):
                if r[t] < len(x) - 1:
                    r[t] += 1
                    return True
                r[t] = 0
            return False

        def i(r):
            t = ""
            for n in range(len(r)):
                t += x[r[n]]
            return t

        def o(r, e):
            n = e
            hashed = hashlib.sha1(e.encode())
            o = hashed.hexdigest()
            t = hashed.digest()
            e = None
            n = -1
            o = []
            for n in range(n + 1, 8 * len(t)):
                e = t[math.floor(n / 8)] >> n % 8 & 1
                o.append(e)
            a = o[:r]

            def index2(x, y):
                if y in x:
                    return x.index(y)
                return -1
            return 0 == a[0] and index2(a, 1) >= r - 1 or -1 == index2(a, 1)

        def get():
            for e in range(25):
                n = [0 for i in range(e)]
                while a(n):
                    u = req["payload"]["d"] + "::" + i(n)
                    if o(req["payload"]["s"], u):
                        return i(n)

        result = get()
        hsl = ":".join([
            "1",
            str(req["payload"]["s"]),
            datetime.now().isoformat()[:19]
            .replace("T", "")
            .replace("-", "")
            .replace(":", ""),
            req["payload"]["d"],
            "",
            result
        ])
        return hsl

    def _site_config(self) -> dict:
        """
        this will get the siteconfig along with the req value which is a very important step,
        it also changes the hash type to hsl.
        """
        try:
            config = requests.get(
                "https://hcaptcha.com/checksiteconfig?host=%s&sitekey=%s&sc=1&swa=1" %
                (self._host, self._sitekey), headers=self.headers, timeout=3).json()
            if config["pass"]:
                config["c"]["type"] = "hsl"
                return config["c"]
            else:
                raise HCaptchaFailure(
                    "failed to fetch the site configuration.")
        except requests.exceptions.Timeout:
            raise APITimeout("unable to connect to hcaptcha.")
        except Exception:
            raise HCaptchaError(
                "somthing went wrong while receiving the site config.")

    def _get_captcha(self) -> str:
        """
        this is the final step in bypassing hcaptcha.
        this part joins all the data so far into a dict (json) and url encodes it.
        """
        try:
            payload = urllib.parse.urlencode({
                "host": self._host,
                "sitekey": self._sitekey,
                "hl": "en",
                "motionData": {
                    "mm": self._mouse_movement(),
                    "st": round(datetime.now().timestamp()),
                    "prev": {
                        "expiredResponse": False
                    }
                },
                "n": self._get_hsl(),
                "c": json.dumps(self._config)
            })
            self.headers["Content-Length"] = str(len(payload))
            getcaptcha = requests.post(
                "https://hcaptcha.com/getcaptcha?s=%s" %
                (self._sitekey),
                data=payload,
                headers=self.headers,
                timeout=3)
            if "generated_pass_UUID" in getcaptcha.text:
                return getcaptcha.json()["generated_pass_UUID"]
            else:
                raise SolveFailure("unable to solve captcha.")
        except requests.exceptions.Timeout:
            raise APITimeout("unable to connect to hcaptcha.")
        except Exception:
            raise HCaptchaError(
                "somthing went wrong while getting the captcha response.")

    def solve(self):
        """
        this is just the main function, example:

        import hcaptcha
        hcaptcha.Solver(host="discord.com", sitekey="f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34").solve()
        """
        return self._get_captcha()
