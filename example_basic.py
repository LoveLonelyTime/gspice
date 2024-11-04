from gspice.gspice import *
from gspice.cells import *

# First, define wires through 'wire()' function
# 'gnd' is ready
vin, vout = wire("vin"), wire("vout")

# Define devices and netlists
# Remember, 'call' is 'generate'
voltage(vin, gnd, "AC=1", name="vin")
ssnmos_ro_cap(g=vin, s=gnd, d=vout, gm="1E-2", ro="1k",
              cgs="10p", cgd="10p", cdb="10p", csb="10p", name="nmos")

# Don't forget the 'name' parameter, otherwise you will get an automatically named device
res(gnd, vout, "1k", name="RD")

# Add simulation
gSpice.add_annotation(".ac dec 100 10 100MEG")

# Now, you get the SPICE
print(gSpice.gen())
