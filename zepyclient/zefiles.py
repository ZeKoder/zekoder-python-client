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

from uuid import UUID
from typing import Optional

import httpx

from utils import get_config


# ZEFILES_BASE_URL = "http://localhost:8000"

ZEFILES_BASE_URL = get_config('ZECOMMON_BASE_URL')

class ZeFilesClient:
    """ No Need to use Auth token in ZeCommons that's why we didn't add to this class"""

    def __init__(self, route: str) -> None:
        self.route = route
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    async def get_asset(self, id: UUID) -> Optional[bytes]: # More Pythonic usage
        """ Only for getting uploaded files and images use this one, route should be defined as asset """
        async with httpx.AsyncClient() as client:
            url = f"{ZEFILES_BASE_URL}/{self.route}/{id}"
            params = {"id": str(id)}
            response = await client.get(url, params=params, headers=self.headers)

            if response.status_code == 200:
                return response.content
            else:
                # Handle error or return None
                raise Exception(f"Failed GET_ASSET -> with status {response.status_code}: {response.text}")


    async def get_file_info(self, file_id: UUID) -> Optional[dict]:

        async with httpx.AsyncClient() as client:
            url = f"{ZEFILES_BASE_URL}/{self.route}/{str(file_id)}"
            response = await client.get(url, headers=self.headers)

            if response.status_code == 200:
                return response.json()
            else:
                # Handle error or return None
                raise Exception(f"Failed GET -> with status {response.status_code}: {response.text}")


    async def upload(self, file_path: str, payload: dict = None) -> Optional[dict]:
        """ Only for upload a file or image, use this one """
        async with httpx.AsyncClient() as client:
            url = f"{ZEFILES_BASE_URL}/{self.route}/"

            if payload is None:
                payload = {}
            # Prepare the multipart form data payload
            with open(file_path, "rb") as f:
                files = {"file": ("filename", f.read())}

            for key, value in payload.items():
                files[key] = (None, str(value))

            response = await client.post(url, files=files, headers=self.headers)

            if response.status_code == 200:
                return response.json()
            else:
                # Handle error or return None
                raise Exception(f"Failed UPLOAD -> with status {response.status_code}: {response.text}")

    async def delete(self, id: UUID) -> Optional[bool]:
        """ Delete only exist for asset in zecommons, use this to delete a file or image """
        async with httpx.AsyncClient() as client:
            url = f"{ZEFILES_BASE_URL}/{self.route}/{id}"
            params = {"id": str(id)}
            response = await client.delete(url, params=params, headers=self.headers)

            if response.status_code == 204:
                return True
            else:
                # Handle error or return False
                raise Exception(f"Failed DELETE -> with status {response.status_code}: {response.text}")


