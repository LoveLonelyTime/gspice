from gspice.gspice import *
from gspice.cells import *

# This example shows you how to use the template to define subcircuits

# Functions with '@subclkt' are considered as a subcircuit
# The parameters of this function are divided into two categories,
# one is the input network, and the other is the template parameters
# The internal and external components of the subcircuit are connected through an input network
# Template parameters can control the structure of subcircuits, and must be specified in params

# For this, 'vin' and 'vout' are input networks
# But, 'r' 'c' 'len' are template parameters


@subckt(params=["r", "c", "len"])
def my_rc_chain(vin, vout, r, c, len=1):
    wires = [vin] + [wire(f"rc{i}") for i in range(len-1)] + [vout]
    # Very nice, you can use the 'for' to generate
    # The same applies to generation such as 'if else'
    # But please note the 'name',
    # gspice will not automatically generate the 'name' for you based on the loop variable
    for i in range(len):
        # 'name' should not be a constant string, otherwise it will be named repeatedly
        res(wires[i], wires[i+1], r, name=f"r{i}")
        cap(wires[i+1], gnd, c, name=f"c{i}")


vin, vout = wire("vin"), wire("vout")

voltage(vin, gnd, "PULSE(0 3 3n 10p 10p 10n 10n)", name="vin")
# Just call it, call of subckt must use keyword arguments
my_rc_chain(vin=vin, vout=vout, r="1u", c="1u", len=10, name="rcc")

# Or, my_rc_chain(vin=vin, vout=vout, r="1u", c="1u", len=5)
# You will get an RC chain with a length of 5 instead of 10
# This is Template Magic, thank you Python

gSpice.add_annotation(".trans 100 10n")

# Now, you get the SPICE
print(gSpice.gen())
