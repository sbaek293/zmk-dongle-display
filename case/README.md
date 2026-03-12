# ZMK Dongle Display Case — 1.69" Flat Display

A printable case for a ZMK dongle with a **1.69-inch flat display**  
(ST7789V driver, 240 × 280 px, AliExpress item 1005007346976745).

Design inspired by [carrefinho/prospector](https://github.com/carrefinho/prospector/tree/main/case).

---

## Files

| File | Description |
|------|-------------|
| `case_body.step` | Main case body — STEP format (editable in Fusion 360, FreeCAD, etc.) |
| `case_body.stl`  | Main case body — STL format (ready to print) |
| `rear_cap.step`  | Rear snap-fit cap — STEP format |
| `rear_cap.stl`   | Rear snap-fit cap — STL format |
| `generate_case.py` | CadQuery parametric source — modify dimensions and re-run to regenerate |

---

## Display Module Dimensions

| Parameter | Value |
|-----------|-------|
| PCB size | 34.0 × 41.8 mm |
| Active display area | 27.8 × 33.4 mm |
| PCB thickness | 1.6 mm |
| Display glass stack | ~2.1 mm |
| Total module thickness | ~3.7 mm |
| Driver IC | ST7789V |
| Resolution | 240 × 280 px |
| Interface | SPI |

---

## Case Dimensions

| Parameter | Value |
|-----------|-------|
| Outer (W × H × D) | 38.1 × 45.9 × 11.0 mm |
| Display window | 27.8 × 33.4 mm |
| Module pocket depth | 4.0 mm |
| Controller cavity | 22.5 × 38.0 × 4.2 mm |
| USB-C slot | 9.2 × 3.5 mm |
| Wall thickness | 1.8 mm |

---

## Assembly

1. **Print** `case_body.stl` and `rear_cap.stl` in PETG or PLA.  
   Recommended settings: 0.2 mm layer height, 4 perimeters, 20% infill.

2. **Insert the display module** into the front pocket (display face toward the window).  
   A drop of cyanoacrylate or double-sided foam tape keeps it in place.

3. **Place the controller** (Nice!nano v2 / Seeed XIAO nRF5340, or similar)  
   into the rear controller cavity. Route the display FPC cable alongside it.

4. **Snap on the rear cap** — the rim slides into the groove around the rear opening.  
   Add M2 screws through the corners for a more secure fit if needed.

---

## Regenerating the Files

Requires [CadQuery](https://cadquery.readthedocs.io) ≥ 2.7:

```bash
pip install cadquery
python3 case/generate_case.py
```

All dimensions are defined as named constants at the top of `generate_case.py`  
and can be adjusted to fit different display modules or controllers.
