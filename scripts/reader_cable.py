#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "schemdraw>=0.19",
# ]
# ///

from pathlib import Path
import schemdraw
import schemdraw.elements as elm


def build_drawing() -> schemdraw.Drawing:
    d = schemdraw.Drawing(fontsize=11, font="sans-serif")
    d.config(unit=2.5, lw=1.8, bgcolor="white")

    # Left connector: RJ45 (J1 on PCB)
    rj45_pins = [
        elm.IcPin(name="sen_pin", pin="1", side="right", slot="8/8", anchorname="p1"),
        elm.IcPin(name="sg_pin", pin="2", side="right", slot="7/8", anchorname="p2"),
        elm.IcPin(name="d1_pin", pin="3", side="right", slot="6/8", anchorname="p3"),
        elm.IcPin(name="GND", pin="4", side="right", slot="5/8", anchorname="p4"),
        elm.IcPin(name="bt_pin", pin="5", side="right", slot="4/8", anchorname="p5"),
        elm.IcPin(name="d0_pin", pin="6", side="right", slot="3/8", anchorname="p6"),
        elm.IcPin(name="GND", pin="7", side="right", slot="2/8", anchorname="p7"),
        elm.IcPin(name="+12V", pin="8", side="right", slot="1/8", anchorname="p8"),
    ]
    rj45 = d.add(
        elm.Ic(
            pins=rj45_pins,
            size=(2.8, 8.2),
            pinspacing=0.95,
            edgepadH=0.5,
            leadlen=0.6,
            fill="#f8fafc",
        ).label("PCB (J1)\nRJ45 (8P8C)", loc="top", fontsize=12)
    )

    # Right connector: JST-SM 6-pin (Keypad, latch facing up, counting L->R)
    # Using pinspacing = (6 * 0.95) / 5 = 1.14 aligns j1 with p1 and j6 with p7!
    jst_pins = [
        elm.IcPin(name="Red (12V)", pin="1", side="left", slot="6/6", anchorname="j1"),
        elm.IcPin(name="White (D1)", pin="2", side="left", slot="5/6", anchorname="j2"),
        elm.IcPin(name="Green (D0)", pin="3", side="left", slot="4/6", anchorname="j3"),
        elm.IcPin(name="Blue (LED)", pin="4", side="left", slot="3/6", anchorname="j4"),
        elm.IcPin(
            name="Yellow (Buz)", pin="5", side="left", slot="2/6", anchorname="j5"
        ),
        elm.IcPin(
            name="Black (GND)", pin="6", side="left", slot="1/6", anchorname="j6"
        ),
    ]
    jst = d.add(
        elm.Ic(
            pins=jst_pins,
            size=(3.1, 7.25),
            pinspacing=1.14,
            edgepadH=0.5,
            leadlen=0.6,
            fill="#f8fafc",
        )
        .anchor("j6")
        .at((rj45.p7.x + 10.5, rj45.p7.y))
        .label("Keypad\nJST-SM (6-pin, L→R)", loc="top", fontsize=12)
    )

    # Unused Cat6 wires (NC)
    d.add(
        elm.Line()
        .right(2.3)
        .at(rj45.p1)
        .color("#d97706")
        .linestyle("--")
        .label("White/Orange", loc="top", fontsize=9.5)
    )
    d.add(elm.NoConnect())

    d.add(
        elm.Line()
        .right(2.3)
        .at(rj45.p4)
        .color("#16a34a")
        .linestyle("--")
        .label("White/Green", loc="top", fontsize=9.5)
    )
    d.add(elm.NoConnect())

    d.add(
        elm.Line()
        .right(2.3)
        .at(rj45.p5)
        .color("#2563eb")
        .linestyle("--")
        .label("White/Blue", loc="top", fontsize=9.5)
    )
    d.add(elm.NoConnect())

    # Pin 3 (d1_pin) -> Orange -> reverse-biased Schottky -> JST Pin 2 (White / D1)
    x_turn_d1 = rj45.p3.x + 3.1
    x_diode_start = rj45.p3.x + 5.2
    d.add(
        elm.Line()
        .right(3.1)
        .at(rj45.p3)
        .color("#ea580c")
        .label("Orange", loc="top", fontsize=10)
    )
    d.add(
        elm.Wire("|-")
        .at((x_turn_d1, rj45.p3.y))
        .to((x_diode_start, jst.j2.y))
        .color("#ea580c")
    )
    d1_diode = d.add(
        elm.Schottky()
        .right()
        .at((x_diode_start, jst.j2.y))
        .to((jst.j2.x - 1.0, jst.j2.y))
        .reverse()
        .color("#ea580c")
        .label("1N5819", loc="top", fontsize=9.5)
    )
    d.add(elm.Line().at(d1_diode.end).to(jst.j2).color("#ea580c"))

    # Pin 6 (d0_pin) -> Green -> reverse-biased Schottky -> JST Pin 3 (Green / D0)
    x_turn_d0 = rj45.p6.x + 3.1
    d.add(
        elm.Line()
        .right(3.1)
        .at(rj45.p6)
        .color("#15803d")
        .label("Green", loc="top", fontsize=10)
    )
    d.add(
        elm.Wire("|-")
        .at((x_turn_d0, rj45.p6.y))
        .to((x_diode_start, jst.j3.y))
        .color("#15803d")
    )
    d0_diode = d.add(
        elm.Schottky()
        .right()
        .at((x_diode_start, jst.j3.y))
        .to((jst.j3.x - 1.0, jst.j3.y))
        .reverse()
        .color("#15803d")
        .label("1N5819", loc="top", fontsize=9.5)
    )
    d.add(elm.Line().at(d0_diode.end).to(jst.j3).color("#15803d"))

    # Pin 2 (sg_pin) -> Blue -> JST Pin 4 (Blue / LED) & jumped to JST Pin 5 (Yellow / Buz)
    x_turn_sg = rj45.p2.x + 3.8
    x_jmp = jst.j4.x - 0.7
    d.add(
        elm.Line()
        .right(3.8)
        .at(rj45.p2)
        .color("#1d4ed8")
        .label("Blue", loc="top", fontsize=10)
    )
    d.add(
        elm.Line().at((x_turn_sg, rj45.p2.y)).to((x_turn_sg, jst.j4.y)).color("#1d4ed8")
    )
    d.add(elm.Line().at((x_turn_sg, jst.j4.y)).to(jst.j4).color("#1d4ed8"))
    d.add(elm.Dot().at((x_jmp, jst.j4.y)).color("#1d4ed8"))
    d.add(
        elm.Line()
        .at((x_jmp, jst.j4.y))
        .to((x_jmp, jst.j5.y))
        .color("#1d4ed8")
        .label("Jumper", loc="top", ofst=0.15, fontsize=9.5)
    )
    d.add(elm.Line().at((x_jmp, jst.j5.y)).to(jst.j5).color("#1d4ed8"))

    # Pin 7 (GND) -> White/Brown -> straight horizontal line to JST Pin 6 (Black / GND)
    d.add(
        elm.Line()
        .at(rj45.p7)
        .to((rj45.p7.x + 3.8, rj45.p7.y))
        .color("#92400e")
        .linestyle("--")
        .label("White/Brown", loc="top", fontsize=10)
    )
    d.add(
        elm.Line()
        .at((rj45.p7.x + 3.8, rj45.p7.y))
        .to(jst.j6)
        .color("#92400e")
        .linestyle("--")
    )

    # Pin 8 (+12V) -> Brown -> JST Pin 1 (Red / 12V)
    x_turn_12v = rj45.p8.x + 4.5
    d.add(
        elm.Line()
        .right(4.5)
        .at(rj45.p8)
        .color("#78350f")
        .label("Brown", loc="top", fontsize=10)
    )
    d.add(
        elm.Line()
        .at((x_turn_12v, rj45.p8.y))
        .to((x_turn_12v, jst.j1.y))
        .color("#78350f")
    )
    d.add(elm.Line().at((x_turn_12v, jst.j1.y)).to(jst.j1).color("#78350f"))

    return d


if __name__ == "__main__":
    out_svg = Path(__file__).resolve().parent.parent / "assets" / "reader-cable.svg"
    drawing = build_drawing()
    drawing.save(str(out_svg), transparent=False)
    print(f"Saved {out_svg}")
