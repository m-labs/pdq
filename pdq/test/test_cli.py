#!/usr/bin/python3
# Copyright 2013-2017 Robert Jordens <jordens@gmail.com>
#
# This file is part of pdq.
#
# pdq is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pdq is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pdq.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from migen import run_simulation

from pdq.gateware.pdq import PdqSim
from pdq.host import cli


def test():
    buf = BytesIO()
    cli.main(buf, args=[])

    def run(n):
        for i in range(n):
            yield
            print("\r{}".format(i), end="")

    tb = PdqSim()
    run_simulation(tb, [tb.write(buf.getvalue()), tb.record(), run(500)],
                   vcd_name="pdq.vcd")
    try:
        from matplotlib import pyplot as plt
        import numpy as np
    except ImportError:
        pass
    else:
        out = np.array(tb.outputs, np.uint16).view(np.int16)
        plt.step(np.arange(len(out)) - 22, out, "-r")
        plt.show()


if __name__ == "__main__":
    test()
