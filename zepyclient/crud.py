# MIT License
#
# Copyright (c) [2023] Cybernetic Labs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



from typing import Optional
from typing import Optional, Dict, Any
from uuid import UUID

import httpx

from utils import get_logger, get_config

log = get_logger()

BASE_URL = get_config('DATABASE_BASE_URL')
ZEAUTH_BASE_URL = get_config('ZEAUTH_BASE_URL')

# TODO: use service accounts instead
AUTH_USERNAME = get_config('AUTH_USERNAME')
AUTH_PASSWORD = get_config('AUTH_PASSWORD')


class DataClient:
    token = None  # let's store token in class variable
    
    # TODO: Require service account credentials on intialization
    def __init__(self, route: str) -> None:
        self.route = route
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    async def _ensure_token(self) -> str:
        if not self.token:
            self.token = await self._auth()
        return self.token

    async def _auth(self) -> str:
        # get the token from zeauth login
        async with httpx.AsyncClient() as client:
            url = f"{ZEAUTH_BASE_URL}/login"
            # Default headers
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json"
            }
            # payload
            payload = {
                "email": AUTH_USERNAME,
                "password": AUTH_PASSWORD
            }

            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                token = response.json().get("accessToken")
                return token
            else:
                raise Exception(f"Failed get TOKEN -> with status {response.status_code}: {response.text}")


    async def get(self, id: UUID) -> Optional[dict]:
        token = await self._ensure_token()
        self.headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient() as client:
            url = f"{BASE_URL}/{self.route}s/{self.route}_id"
            response = await client.get(url, params={f"{self.route}_id": str(id)}, headers=self.headers)

            if response.status_code == 200:
                return response.json()
            else:
                # Handle error or return None
                raise Exception(f"Failed GET -> with status {response.status_code}: {response.text}")

    async def list(self, page: int, page_size: int) -> Optional[dict]:
        token = await self._ensure_token()
        self.headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient() as client:
            url = f"{BASE_URL}/{self.route}s/"
            response = await client.get(url, params={"page": page, "size": page_size}, headers=self.headers)

            if response.status_code == 200:
                return response.json()
            else:
                # Handle error or return empty list
                raise Exception(f"Failed LIST -> with status {response.status_code}: {response.text}")

    async def create(self, payload: dict) -> Optional[dict]:
        token = await self._ensure_token()
        self.headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient() as client:
            url = f"{BASE_URL}/{self.route}s/"
            response = await client.post(url, json=payload, headers=self.headers)

            if response.status_code == 201:
                return response.json()
            else:
                # Handle error or return None
                raise Exception(f"Failed CREATE -> with status {response.status_code}: {response.text}")


    async def post_data(self, str_for_dec: str) -> Optional[dict]:
        """ This is the Default endpoint in ZeAuth"""
        token = await self._ensure_token()
        self.headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient() as client:
            url = f"{ZEAUTH_BASE_URL}/{self.route}"
            params = {"str_for_dec": str_for_dec}

            response = await client.post(url, headers=self.headers, params=params)

            if response.status_code == 200:
                return response.json()
            else:
                # Handle error or return None
                raise Exception(f"Failed POST request -> with status {response.status_code}: {response.text}")


    async def query(self, payload: dict) -> Optional[dict]:
        token = await self._ensure_token()
        self.headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient() as client:
            url = f"{BASE_URL}/{self.route}/q"
            response = await client.post(url, json=payload, headers=self.headers)

            if response.status_code == 200:
                response_data = response.json()
                return response_data.get('data', [])
            else:
                # Handle error or return None
                raise Exception(f"Failed QUERY -> with status {response.status_code}: {response.text}")

    async def update(self, id: UUID, payload: Dict[str, Any]) -> Optional[dict]:
        token = await self._ensure_token()
        self.headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient() as client:
            url = f"{BASE_URL}/{self.route}s/{self.route}_id"
            response = await client.put(url, params={f"{self.route}_id": str(id)}, json=payload, headers=self.headers)

            if response.status_code == 201:
                return response.json()
            else:
                # Handle error or return None
                raise Exception(f"Failed UPDATE -> with status {response.status_code}: {response.text}")

    async def delete(self, id: UUID) -> Optional[bool]:
        token = await self._ensure_token()
        self.headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient() as client:
            url = f"{BASE_URL}/{self.route}s/{self.route}_id"
            response = await client.delete(url, params={f"{self.route}_id": str(id)}, headers=self.headers)

            if response.status_code == 204:
                return True
            else:
                # Handle error or return False
                raise Exception(f"Failed DELETE -> with status {response.status_code}: {response.text}")


