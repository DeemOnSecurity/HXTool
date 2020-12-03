#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from time import sleep

sys.path.append("../")

from src.hxtool_scheduler import *
from src import hxtool_global


class test_scheduler:
    def __init__(self):
        self.ht_scheduler = hxtool_scheduler()
        self.ht_scheduler.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.ht_scheduler.logger.setLevel(logging.DEBUG)

        hxtool_global.hxtool_scheduler = self.ht_scheduler

    def run_test(self):
        print("Testing hxtool_scheduler...")
        self.ht_scheduler.start()
        for i in range(1, 500):
            ht_task = hxtool_scheduler_task(
                "System",
                "Test Task {}".format(i),
                immutable=True,
                logger=self.ht_scheduler.logger,
            )
            r = random.randint(1, 100)
            if r > 50:
                ht_task.set_schedule(minutes=random.randint(1, 5))
            ht_task.add_step(
                self, "test_scheduler_function", args=(random.randint(1, 60),)
            )
            self.ht_scheduler.add(ht_task, should_store=False)
            ht_task = None

        try:
            while True:
                sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            self.ht_scheduler.stop()

    def test_scheduler_function(self, n):
        print("Random number is: {}".format(n * random.randint(0, 500)))
        return True


t = test_scheduler()
t.run_test()
