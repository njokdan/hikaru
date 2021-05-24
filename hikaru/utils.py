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
from typing import Any, Optional
from multiprocessing.pool import ApplyResult
from hikaru.generate import from_dict


class Response(object):
    """
    Response bundles up the possible responses that can be generated by K8s calls

    All Hikaru methods and functions return Response objects, which Hikaru fills out
    upon receiving a response from the underlying K8s method calls. K8s may return
    one of two kinds of values: for blocking calls, K8s returns the response code,
    data object, and headers. For async calls, K8s returns the thread that is
    processing the call. Hikaru's Response objects cover both of these possibilities.

    Public attributes can be interpreted as follows:

    If the call is blocking:

    - code: integer response code from K8s
    - obj: the data returned for the call. May be plain data, or may be an
      instance of a HikaruDocumentBase subclass, depending on the call.
    - headers: a dict-like object of the response headers

    If the call is non-blocking:

    - code, obj, headers: all None UNTIL .get() is called on the Response
        instance, at which point all three are populated as above as well
        as .get() returning a 3-tuple of (object, code, headers)

    Response objects also act as a proxy for the underlying multiprocessing
    thread object (multiprocessing.pool.ApplyResult) and will forward on
    the other public methods of that class.

    If .get() or any of the other async supporting calls are made on a Response
    object that was called blocking then they will all return None.
    """
    # this flag sets the 'translate' argument to from_dict()
    # when retrieving results from K8s. In normal integration cases
    # it should be True, but for certain tests it needs to be False.
    # Testing code that doesn't integrate into Kubernetes can set this
    # to False to avoid improperly named attributes.
    set_false_for_internal_tests = True

    def __init__(self, k8s_response, codes_with_objects):
        """
        Creates a new response:
        :param k8s_response: a 3-tuple consisting of:
            - return value dict
            - return code
            - headers
        :param codes_with_objects: an iterable of ints that are codes for which
            the self.obj field is a K8s object
        """
        self.code: Optional[int] = None
        self.obj: Optional[Any] = None
        self.headers: Optional[dict] = None
        self._thread: Optional[ApplyResult] = None
        self.codes_with_objects = set(codes_with_objects)
        if type(k8s_response) is tuple:
            self._process_result(k8s_response)
        else:
            # assume an ApplyResult
            self._thread = k8s_response

    def _process_result(self, result: tuple):
        self.obj = result[0]
        self.code = result[1]
        self.headers = result[2]
        if self.code in self.codes_with_objects:
            self.obj = (from_dict(self.obj.to_dict(),
                                  translate=self.set_false_for_internal_tests)
                        if self.obj is not None
                        else self.obj)

    def ready(self):
        return self._thread.ready()

    def successful(self):
        return self._thread.successful()

    def wait(self, timeout=None):
        self._thread.wait(timeout=timeout)

    def get(self, timeout=None) -> tuple:
        """
        Fetch the results of an async call into K8s.

        This method waits for a response to a previously submitted request, either
        for a specified amount of time or indefinitely, and either raises an exception
        or returns the delivered response.

        :param timeout: optional float; if supplied, only waits 'timeout' seconds
            for a response until it raises a TimeoutError exception if the response
            hasn't arrived. If not supplied, blocks indefinitely.

        :return: a 3-tuple of (Hikaru object, result code (int), headers). These
            values are also stored in the public attributes of the instance, so
            you don't actually have to capture them upon return if you don't wish to.

        :raises TimeoutError: if a response has not arrived before the specified timeout
            has elapsed.
        :raises RuntimeError: if the reply is the wrong type altogether (should be
            reported).

        May also pass through any other exception.
        """
        result = self._thread.get(timeout=timeout)
        if type(result) is tuple:
            self._process_result(result)
        else:
            raise RuntimeError(f"Received an unknown type of response from K8s: "
                               f"type={type(result)}, value={result}")  # pragma: no cover
        return self.obj, self.code, self.headers
