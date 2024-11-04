from gspice.gspice import *


class Res:
    def __init__(self, name, p1, p2, value):
        self.name = name
        self.p1 = p1
        self.p2 = p2
        self.value = value

    def gen(self):
        return f"R{self.name} {self.p1} {self.p2} {self.value}"


class Cap:
    def __init__(self, name, p1, p2, value):
        self.name = name
        self.p1 = p1
        self.p2 = p2
        self.value = value

    def gen(self):
        return f"C{self.name} {self.p1} {self.p2} {self.value}"


class Ind:
    def __init__(self, name, p1, p2, value):
        self.name = name
        self.p1 = p1
        self.p2 = p2
        self.value = value

    def gen(self):
        return f"L{self.name} {self.p1} {self.p2} {self.value}"


class Voltage:
    def __init__(self, name, pp, pn, value):
        self.name = name
        self.pp = pp
        self.pn = pn
        self.value = value

    def gen(self):
        return f"V{self.name} {self.pp} {self.pn} {self.value}"


class Current:
    def __init__(self, name, pp, pn, value):
        self.name = name
        self.pp = pp
        self.pn = pn
        self.value = value

    def gen(self):
        return f"I{self.name} {self.pp} {self.pn} {self.value}"


class Gain:
    def __init__(self, name, pvp, pvn, pip, pin, value):
        self.name = name
        self.pvp = pvp
        self.pvn = pvn
        self.pip = pip
        self.pin = pin
        self.value = value

    def gen(self):
        return f"G{self.name} {self.pvp} {self.pvn} {self.pip} {self.pin} {self.value}"


@cell
def res(va, vb, value):
    gSpice.put_cell(Res(gSpice.get_namespace(), va, vb, value))


@cell
def cap(va, vb, value):
    gSpice.put_cell(Cap(gSpice.get_namespace(), va, vb, value))


@cell
def ind(va, vb, value):
    gSpice.put_cell(Ind(gSpice.get_namespace(), va, vb, value))


@cell
def voltage(vp, vn, value):
    gSpice.put_cell(Voltage(gSpice.get_namespace(), vp, vn, value))


@cell
def current(vp, vn, value):
    gSpice.put_cell(Current(gSpice.get_namespace(), vp, vn, value))


@cell
def current(vp, vn, value):
    gSpice.put_cell(Current(gSpice.get_namespace(), vp, vn, value))


@cell
def gain(vp, vn, ip, iin, value):
    gSpice.put_cell(Gain(gSpice.get_namespace(), vp, vn, ip, iin, value))


@subckt(params=["gm"])
def ssnmos(g, d, s, gm):
    gain(s, d, g, s, gm, name="gain")


@subckt(params=["gm"])
def sspmos(g, d, s, gm):
    gain(d, s, s, g, gm, name="gain")


@subckt(params=["gm", "ro"])
def ssnmos_ro(g, d, s, gm, ro):
    gain(s, d, g, s, gm, name="gain")
    res(d, s, ro, name="ro")


@subckt(params=["gm", "ro"])
def sspmos_ro(g, d, s, gm, ro):
    gain(d, s, s, g, gm, name="gain")
    res(d, s, ro, name="ro")


@subckt(params=["gm", "ro", "cgs", "cgd", "cdb", "csb"])
def ssnmos_ro_cap(g, d, s, gm, ro, cgs, cgd, cdb, csb):
    gain(s, d, g, s, gm, name="gain")
    res(d, s, ro, name="ro")
    cap(g, s, cgs, name="cgs")
    cap(g, d, cgd, name="cgd")
    cap(d, gnd, cdb, name="cdb")
    cap(s, gnd, csb, name="csb")


@subckt(params=["gm", "ro", "cgs", "cgd", "cdb", "csb"])
def sspmos_ro_cap(g, d, s, gm, ro, cgs, cgd, cdb, csb):
    gain(d, s, s, g, gm, name="gain")
    res(d, s, ro, name="ro")
    cap(g, s, cgs, name="cgs")
    cap(g, d, cgd, name="cgd")
    cap(d, gnd, cdb, name="cdb")
    cap(s, gnd, csb, name="csb")


@subckt(params=["r", "c", "len"])
def rc_chain(vin, vout, r, c, len=1):
    wires = [vin] + [wire(f"rc{i}") for i in range(len-1)] + [vout]
    for i in range(len):
        res(wires[i], wires[i+1], r, name=f"r{i}")
        cap(wires[i+1], gnd, c, name=f"c{i}")
