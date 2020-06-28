"""Drivers and buses package for liquidctl.

The typical use case of generic scripts and interfaces – including the
liquidctl CLI – is to instantiate drivers for all known devices found on the
system.

    from liquidctl.driver import *
    for dev in find_liquidctl_devices():
        print(dev.description)

Is also possible to find devices compatible with a specific driver.

    from liquidctl.driver.kraken_two import KrakenTwoDriver
    for dev in KrakenTwoDriver.find_supported_devices():
        print(dev.description)

Copyright (C) 2018–2020  Jonas Malaco
Copyright (C) 2018–2020  each contribution's author

SPDX-License-Identifier: GPL-3.0-or-later
"""

import liquidctl.driver.asetek
import liquidctl.driver.coolit
import liquidctl.driver.coolit_platinum
import liquidctl.driver.corsair_hid_psu
import liquidctl.driver.kraken_two
import liquidctl.driver.kraken_gen4
import liquidctl.driver.nzxt_smart_device
import liquidctl.driver.seasonic

from liquidctl.driver.base import BaseBus, find_all_subclasses


def find_liquidctl_devices(pick=None, **kwargs):
    """Find devices and instantiate corresponding liquidctl drivers.

    Probes all buses and drivers that have been loaded at the time of the call
    and yields driver instances.

    Filter conditions can be passed through to the buses and drivers via
    `**kwargs`.  A driver instance will be yielded for each compatible device
    that matches the supplied filter conditions.

    If `pick` is passed, only the driver instance for the `(pick + 1)`-th
    matched device will be yielded.
    """
    buses = sorted(find_all_subclasses(BaseBus), key=lambda x: x.__name__)
    num = 0
    for bus_cls in buses:
        for dev in  bus_cls().find_devices(**kwargs):
            if pick is not None:
                if num == pick:
                    yield dev
                    return
                num += 1
            else:
                yield dev


__all__ = [
    'find_liquidctl_devices',
]
