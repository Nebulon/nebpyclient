#
# Copyright 2021 Nebulon, Inc.
# All Rights Reserved.
#
# DISCLAIMER: THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO
# EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
__all__ = [
    "API_SERVER_URI",
    "API_TIMEOUT_SECONDS",
]

API_SERVER_URI = "https://ucapi.nebcloud.nebulon.com/query"
API_TIMEOUT_SECONDS = 60

"""Timeout to wait for nPod creation to complete"""
RECIPE_TIMEOUT_SECONDS = 60 * 45

"""Timeout for token delivery"""
TOKEN_TIMEOUT_SECONDS = 60 * 2
