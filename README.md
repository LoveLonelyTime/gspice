# GSpice
Python SPICE netlist generator.

When I was studying analog circuits, I found that the netlist syntax of LTSpice was not very useful, so I implemented the gspice project.

Compared to spice, you can use Python features to represent circuits.

Like this:

```python
@subckt(params=["r", "c", "len"])
def rc_chain(vin, vout, r, c, len=1):
    wires = [vin] + [wire(f"rc{i}") for i in range(len-1)] + [vout]
    # Generate the corresponding length based on len
    for i in range(len):
        res(wires[i], wires[i+1], r, name=f"r{i}")
        cap(wires[i+1], gnd, c, name=f"c{i}")
```

Call is generate!

```python
voltage(vin, gnd, "AC=1", name="vin")
ssnmos_ro_cap(g=vin, s=gnd, d=vout, gm="1E-2", ro="1k",
              cgs="10p", cgd="10p", cdb="10p", csb="10p", name="nmos")
res(gnd, vout, "1k", name="RD")
```

These are what I hope for.
