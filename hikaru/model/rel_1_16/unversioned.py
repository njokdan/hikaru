#
# Copyright (c) 2021 Incisive Technology Ltd
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
"""
DO NOT EDIT THIS FILE!

This module is automatically generated using the Hikaru build program that turns
a Kubernetes swagger spec into the code for the hikaru.model package.
"""


from hikaru.meta import HikaruBase, HikaruDocumentBase, KubernetesException
from hikaru.generate import get_clean_dict
from hikaru.utils import Response
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, InitVar
from kubernetes.client import CoreV1Api

from kubernetes.client import ApiClient


@dataclass
class Info(HikaruBase):
    r"""
    Info contains versioning information. how we'll want to distribute that information.

    Full name: version.Info

    Attributes:
    buildDate:
    compiler:
    gitCommit:
    gitTreeState:
    gitVersion:
    goVersion:
    major:
    minor:
    platform:
    """

    buildDate: str
    compiler: str
    gitCommit: str
    gitTreeState: str
    gitVersion: str
    goVersion: str
    major: str
    minor: str
    platform: str


globs = dict(globals())
__all__ = [c.__name__ for c in globs.values()
           if type(c) == type]
del globs
