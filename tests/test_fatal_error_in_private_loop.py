# Copyright 2016 by MPI-SWS and Data-Ken Research.
# Licensed under the Apache 2.0 License.
"""Run a private event loop and then throw a fatal error in it to verify that
we shut down cleanly and don't lose the error.
"""

import thingflow.filters.output
from thingflow.base import Scheduler, OutputThing, EventLoopOutputThingMixin, FatalError

import unittest
import asyncio
s = Scheduler(asyncio.get_event_loop())

import time

class TestOutputThing(OutputThing, EventLoopOutputThingMixin):
    def __init__(self):
        super().__init__()

    def _observe_event_loop(self):
        print("starting event loop")
        for i in range(4):
            if self.stop_requested:
                break
            self._dispatch_next(i)
            time.sleep(1)
        raise FatalError("testing the fatal error")

class TestFatalErrorInPrivateLoop(unittest.TestCase):
    def test_case(self):
        m = TestOutputThing()
        m.output()
        c = s.schedule_on_private_event_loop(m)
        m.print_downstream()
        try:
            s.run_forever()
        except FatalError:
            print("we got the fatal error as expected")
        else:
            print("The event loop exited without throwing a fatal error!")
            self.assertFalse(1, "The event loop exited without throwing a fatal error!")

if __name__ == '__main__':
    unittest.main()


