"""*------------------------------------------------------------*-
  Continuous Stream Reader - Non Blocking Stream Reader - python module file
   (c) Eyal Arubas 2013
   (c) Minh-An Dao 2019
  version 1.10 - 25/10/2019
 --------------------------------------------------------------
 * References:
 * - http://eyalarubas.com/python-subproc-nonblock.html
 * - https://gist.github.com/EyalAr
 --------------------------------------------------------------"""
from threading import Thread
from queue import Queue, Empty

class StreamReader:

    def __init__(self, popen_object):
        """
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        """

        self._s = popen_object
        self._q = Queue()

        def _populateQueue(stream, queues):
            """
            Collect lines from 'stream' and put them in 'queue'.
            """

            while True:
                line = stream.readline()
                if line:
                    queues.put(line)
                else:
                    raise UnexpectedEndOfStream

        self._t = Thread(target = _populateQueue,
                args = (self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None,
                    timeout = timeout)
        except Empty:
            return None, None

class UnexpectedEndOfStream(Exception): pass
