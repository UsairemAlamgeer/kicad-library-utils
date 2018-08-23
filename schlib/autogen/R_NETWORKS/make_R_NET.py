#!/usr/bin/env python

import sys
import os
import math

def roundG(x, g):
    if x > 0:
        return math.ceil(x / g) * g
    else:
        return math.floor(x / g) * g

def roundCrt(x):
    return roundG(x, 0.05)

def makeR_Network(lib, dcm, count):
    name = "R_Network{:02d}".format(count)
    refdes = "RN"

    dcm.write("#\n")
    dcm.write("$CMP {0}\n".format(name))
    dcm.write("D {0} Resistor network, star topology, bussed resistors, small symbol\n".format(count))
    dcm.write("K R Network star-topology\n")
    dcm.write("F http://www.vishay.com/docs/31509/csc.pdf\n")
    dcm.write("$ENDCMP\n")

    dp = 100
    dot_diam = 20
    pinlen = 100
    R_len = 160
    R_w = 60
    W_dist = 30
    box_l_offset = 50
    left = -math.floor(count / 2) * dp
    l_box = left - box_l_offset
    t_box = -125
    h_box = 250
    w_box = (count - 1) * dp + 2 * box_l_offset
    top = -200
    bottom = 200

    lib.write("#\n")
    lib.write("# {0}\n".format(name))
    lib.write("#\n")
    lib.write("DEF {0} {1} 0 0 N N 1 F N\n".format(name, refdes))
    lib.write(("F0 \"{0}\" {1} 0 50 V V C CNN\n").format(refdes, int(l_box - 50)))
    lib.write(("F1 \"{0}\" {1} 0 50 V V C CNN\n").format(name, int(l_box + w_box + 50)))
    lib.write("F2 \"Resistors_ThroughHole:Resistor_Array_SIP{0}\" {1} 0 50 V I C CNN\n".format(count + 1, int(l_box + w_box + 50 + 75)))
    lib.write("F3 \"\" 0 0 50 H V C CNN\n")
    lib.write("$FPLIST\n")
    lib.write(" Resistor?Array?SIP*\n")
    lib.write("$ENDFPLIST\n")
    lib.write("DRAW\n")
    lib.write("S {0} {1} {2} {3} 0 1 10 f\n".format(int(l_box), int(t_box), int(l_box + w_box), int(t_box + h_box)))

    pinl = left
    y = top

    lib.write("X COM 1 {0} {1} {2} D 50 50 1 1 P\n".format(int(pinl), -int(top), int(pinlen)))
    lib.write("P 2 0 1 0 {0} {1} {0} {2} N\n".format(int(pinl), -int(top + pinlen), -int(bottom - pinlen - R_len)))

    for s in range(1, count + 1):
        lib.write("X R{0} {1} {2} {3} {4} U 50 50 1 1 P\n".format(int(s), int(s + 1), int(pinl), -int(bottom), int(pinlen)))
        lib.write("S {0} {1} {2} {3} 0 1 10 N\n".format(int(pinl - R_w / 2), -int(bottom - pinlen - R_len), int(pinl + R_w / 2), -int(bottom - pinlen)))

        if s < count:
            lib.write("P 4 0 1 0 {0} {1} {0} {2} {3} {2} {3} {1} N\n".format(int(pinl), -int(bottom - pinlen - R_len), -int(bottom - pinlen - R_len - W_dist), int(pinl + dp)))
            lib.write("C {0} {1} 10 0 1 0 F\n".format(int(pinl), -int(bottom - pinlen - R_len - W_dist), int(dot_diam / 2)))

        pinl = pinl + dp

    lib.write("ENDDRAW\n")
    lib.write("ENDDEF\n")

def makeR_Pack_SIP(lib, dcm, count):
    name = "R_Pack{:02d}_SIP".format(count)
    refdes = "RN"

    dcm.write("#\n")
    dcm.write("$CMP {0}\n".format(name))
    dcm.write("D {0} Resistor network, parallel topology, SIP package\n".format(count))
    dcm.write("K R Network parallel topology\n")
    dcm.write("F http://www.vishay.com/docs/31509/csc.pdf\n")
    dcm.write("$ENDCMP\n")

    dp = 100
    dR = 300
    pinlen = 150
    R_len = 160
    R_w = 60
    W_dist = 30
    box_l_offset = 50
    left = -roundG(((count - 1) * dR) / 2, 100)
    l_box = left - box_l_offset
    t_box = -75
    h_box = 250
    w_box = ((count - 1) * dR + dp) + 2 * box_l_offset
    top = -200
    bottom = 200

    lib.write("#\n")
    lib.write("# {0}\n".format(name))
    lib.write("#\n")
    lib.write("DEF {0} {1} 0 0 Y N 1 F N\n".format(name, refdes))
    lib.write(("F0 \"{0}\" {1} 0 50 V V C CNN\n").format(refdes, int(l_box - 50)))
    lib.write(("F1 \"{0}\" {1} 0 50 V V C CNN\n").format(name, int(l_box + w_box + 50)))
    lib.write("F2 \"Resistors_ThroughHole:Resistor_Array_SIP{0}\" {1} 0 50 V I C CNN\n".format(2 * count, int(l_box + w_box + 50 + 75)))
    lib.write("F3 \"\" 0 0 50 H V C CNN\n")
    lib.write("$FPLIST\n")
    lib.write(" Resistor?Array?SIP*\n")
    lib.write("$ENDFPLIST\n")
    lib.write("DRAW\n")
    lib.write("S {0} {1} {2} {3} 0 1 10 f\n".format(int(l_box), int(t_box), int(l_box + w_box), int(t_box + h_box)))

    pinl = left
    y = top

    for s in range(1, count + 1):
        lib.write("X R{0}.1 {1} {2} {3} {4} U 50 50 1 1 P\n".format(int(s), int(2 * s - 1), int(pinl), -int(bottom), int(pinlen)))
        lib.write("X R{0}.2 {1} {2} {3} {4} U 50 50 1 1 P\n".format(int(s), int(2 * s), int(pinl + dp), -int(bottom), int(pinlen)))
        lib.write("S {0} {1} {2} {3} 0 1 10 N\n".format(int(pinl - R_w / 2), -int(bottom - pinlen - R_len), int(pinl + R_w / 2), -int(bottom - pinlen)))
        lib.write("P 4 0 1 0 {0} {1} {0} {2} {3} {2} {3} {4} N\n".format(int(pinl), -int(bottom - pinlen - R_len), -int(bottom - pinlen - R_len - W_dist), int(pinl + dp), -int(bottom - pinlen)))
        pinl = pinl + dR

    lib.write("ENDDRAW\n")
    lib.write("ENDDEF\n")

def makeR_Pack(lib, dcm, count):
    name = "R_Pack{:02d}_DIP".format(count)
    refdes = "RN"

    dcm.write("#\n")
    dcm.write("$CMP {0}\n".format(name))
    dcm.write("D {0} Resistor network, parallel topology, DIP package\n".format(count))
    dcm.write("K R Network parallel topology\n")
    dcm.write("$ENDCMP\n")

    dp = 100
    pinlen = 100
    R_len = 150
    R_w = 50
    W_dist = 30
    box_l_offset = 50
    box_t_offset = 20
    left = -roundG(((count - 1) * dp) / 2, 100)
    l_box = left - box_l_offset
    h_box = R_len + 2 * box_t_offset
    t_box = -h_box / 2
    w_box = ((count - 1) * dp) + 2 * box_l_offset
    top = -200
    bottom = 200

    lib.write("#\n")
    lib.write("# {0}\n".format(name))
    lib.write("#\n")
    lib.write("DEF {0} {1} 0 0 Y N 1 F N\n".format(name, refdes))
    lib.write(("F0 \"{0}\" {1} 0 50 V V C CNN\n").format(refdes, int(l_box - 50)))
    lib.write(("F1 \"{0}\" {1} 0 50 V V C CNN\n").format(name, int(l_box + w_box + 50)))
    lib.write("F2 \"\" {0} 0 50 V I C CNN\n".format(int(l_box + w_box + 50 + 75)))
    lib.write("F3 \"\" 0 0 50 H V C CNN\n")
    lib.write("$FPLIST\n")
    lib.write(" DIP*\n")
    lib.write(" SOIC*\n")
    lib.write("$ENDFPLIST\n")
    lib.write("DRAW\n")
    lib.write("S {0} {1} {2} {3} 0 1 10 f\n".format(int(l_box), int(t_box), int(l_box + w_box), int(t_box + h_box)))

    pinl = left
    y = top

    for s in range(1, count + 1):
        lib.write("X R{0}.1 {1} {2} {3} {4} U 50 50 1 1 P\n".format(int(s), int(s), int(pinl), -int(bottom), int(pinlen)))
        lib.write("X R{0}.2 {1} {2} {3} {4} D 50 50 1 1 P\n".format(int(s), int(2 * count - s + 1), int(pinl), -int(top), int(pinlen)))
        lib.write("S {0} {1} {2} {3} 0 1 10 N\n".format(int(pinl - R_w / 2), -int(-R_len / 2), int(pinl + R_w / 2), -int(R_len / 2)))
        lib.write("P 2 0 1 0 {0} {1} {0} {2} N\n".format(int(pinl), -int(bottom - pinlen), -int(R_len / 2)))
        lib.write("P 2 0 1 0 {0} {1} {0} {2} N\n".format(int(pinl), -int(-R_len / 2), -int(top + pinlen)))

        pinl = pinl + dp

    lib.write("ENDDRAW\n")
    lib.write("ENDDEF\n")

def makeR_Network_Dividers_SIP(lib, dcm, count):
    name = "R_Network_Dividers_x{:02d}_SIP".format(count)
    refdes = "RN"

    dcm.write("#\n")
    dcm.write("$CMP {0}\n".format(name))
    dcm.write("D {0} Voltage Dividers network, Dual Terminator, SIP package\n".format(count))
    dcm.write("K R Network divider topology\n")
    dcm.write("F http://www.vishay.com/docs/31509/csc.pdf\n")
    dcm.write("$ENDCMP\n")

    dp = 200
    dot_diam = 20
    pinlen = 100
    R_len = 100
    R_w = 40
    W_dist = 30
    box_l_offset = 50
    left = -math.floor(count / 2) * dp
    top = -300
    bottom = 300
    l_box = left - box_l_offset
    t_box = top + pinlen
    h_box = abs(bottom - pinlen - t_box)
    w_box = (count - 1) * dp + dp / 2 + 2 * box_l_offset
    R_dist = (h_box - 2 * R_len) / 3

    lib.write("#\n")
    lib.write("# {0}\n".format(name))
    lib.write("#\n")
    lib.write("DEF {0} {1} 0 0 Y N 1 F N\n".format(name, refdes))
    lib.write(("F0 \"{0}\" {1} 0 50 V V C CNN\n").format(refdes, int(l_box - 50)))
    lib.write(("F1 \"{0}\" {1} 0 50 V V C CNN\n").format(name, int(l_box + w_box + 50)))
    lib.write("F2 \"Resistors_ThroughHole:Resistor_Array_SIP{0}\" {1} 0 50 V I C CNN\n".format(count + 2, int(l_box + w_box + 50 + 75)))
    lib.write("F3 \"\" 0 0 50 H V C CNN\n")
    lib.write("$FPLIST\n")
    lib.write(" Resistor?Array?SIP*\n")
    lib.write("$ENDFPLIST\n")
    lib.write("DRAW\n")
    lib.write("S {0} {1} {2} {3} 0 1 10 f\n".format(int(l_box), int(t_box), int(l_box + w_box), int(t_box + h_box)))

    pinl = left
    y = top

    lib.write("X COM1 1 {0} {1} {2} D 50 50 1 1 P\n".format(int(pinl), -int(top), int(pinlen)))
    lib.write("X COM2 {0} {1} {2} {3} D 50 50 1 1 P\n".format(int(count + 2), int(left + (count - 1) * dp + dp / 2), -int(top), int(pinlen)))
    lib.write("P 2 0 1 0 {0} {1} {0} {2} N\n".format(int(left + (count - 1) * dp + dp / 2), -int(bottom - pinlen - R_dist / 2), -int(top + pinlen)))

    for s in range(1, count + 1):
        lib.write("X R{0} {1} {2} {3} {4} U 50 50 1 1 P\n".format(int(s), int(s + 1), int(pinl), -int(bottom), int(pinlen)))
        lib.write("S {0} {1} {2} {3} 0 1 10 N\n".format(int(pinl - R_w / 2), -int(top + pinlen + R_dist), int(pinl + R_w / 2), -int(top + pinlen + R_dist + R_len)))
        lib.write("S {0} {1} {2} {3} 0 1 10 N\n".format(int(pinl + 3 * R_w / 2 - R_w / 2), -int(bottom - pinlen - R_dist), int(pinl + 3 * R_w / 2 + R_w / 2), -int(bottom - pinlen - R_dist - R_len)))
        lib.write("P 3 0 1 0 {0} {1} {0} {2} {3} {2} N\n".format(int(pinl + 3 * R_w / 2), -int(bottom - pinlen - R_dist), -int(bottom - pinlen - R_dist / 2), int(left + (count - 1) * dp + dp / 2)))

        if s == 1:
            lib.write("P 2 0 1 0 {0} {1} {0} {2} N\n".format(int(pinl), -int(top + pinlen), -int(top + pinlen + R_dist)))

        if s > 1:
            lib.write("P 3 0 1 0 {0} {1} {2} {1} {2} {3} N\n".format(int(pinl - dp), -int(top + pinlen + R_dist / 2), int(pinl), -int(top + pinlen + R_dist)))

        lib.write("P 2 0 1 0 {0} {1} {0} {2} N\n".format(int(pinl), -int(bottom - pinlen), -int(top + pinlen + R_dist + R_len)))
        lib.write("P 3 0 1 0 {0} {1} {2} {1} {2} {3} N\n".format(int(pinl), -int(top + pinlen + R_dist + R_len + R_dist / 2), int(pinl + 3 * R_w / 2), -int(bottom - pinlen - R_dist - R_len)))
        lib.write("C {0} 0 {1} 0 1 0 F\n".format(int(pinl), int(dot_diam / 2)))

        if s > 1:
            lib.write("C {0} {1} {2} 0 1 0 F\n".format(int(pinl + 3 * R_w / 2), -int(bottom - pinlen - R_dist / 2), int(dot_diam / 2)))

        if s < count:
            lib.write("C {0} {1} {2} 0 1 0 F\n".format(int(pinl), -int(top + pinlen + R_dist / 2), int(dot_diam / 2)))

        pinl = pinl + dp

    lib.write("ENDDRAW\n")
    lib.write("ENDDEF\n")

if __name__ == '__main__':
    lib = open("R_Network.lib", 'w')
    lib.write("EESchema-LIBRARY Version 2.4\n")
    lib.write("#encoding utf-8\n")

    dcm = open("R_Network.dcm", 'w')
    dcm.write("EESchema-DOCLIB  Version 2.0\n")

    for i in range(3, 14):
        makeR_Network(lib, dcm, i)

    for i in range(2, 12):
        makeR_Network_Dividers_SIP(lib, dcm, i)

    for i in range(2, 8):
        makeR_Pack_SIP(lib, dcm, i)

    for i in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        makeR_Pack(lib, dcm, i)

    dcm.write("#End Doc Library\n")
    lib.write("#End Library\n")
