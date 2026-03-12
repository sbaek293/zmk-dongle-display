"""
ZMK Dongle Display Case Generator
1.69-inch flat display (ST7789V, 240x280) case design

Display module specifications (typical 1.69" from AliExpress,
item 1005007346976745):
  PCB overall:   34.0 x 41.8 mm
  Active area:   27.8 x 33.4 mm (240 x 280 px)
  PCB thickness: 1.6 mm
  Module height: 3.7 mm (PCB + display glass stack)

Case design inspired by carrefinho/prospector
Intended controller: Nice!nano v2 / Seeed XIAO nRF5340 (or similar)
"""

import cadquery as cq
import os

# ---------------------------------------------------------------------------
# Display module dimensions (1.69" ST7789V, 240x280)
# ---------------------------------------------------------------------------
DISP_PCB_W   = 34.0   # PCB width  (X)
DISP_PCB_H   = 41.8   # PCB height (Y)
DISP_PCB_T   = 1.6    # PCB thickness
DISP_GLASS_T = 2.1    # display glass + bezel thickness above PCB
DISP_TOTAL_T = DISP_PCB_T + DISP_GLASS_T  # ≈ 3.7 mm

DISP_WIN_W   = 27.8   # active display window width  (X)
DISP_WIN_H   = 33.4   # active display window height (Y)

# Active area offset from PCB centre (display centred horizontally,
# shifted 0.5 mm upward relative to PCB centre on this module)
DISP_WIN_OFFSET_X = 0.0
DISP_WIN_OFFSET_Y = 0.5

# ---------------------------------------------------------------------------
# Case geometry constants
# ---------------------------------------------------------------------------
WALL       = 1.8    # wall / shell thickness (mm)
CORNER_R   = 2.5    # outer corner fillet radius (mm)

# Pocket for the display module (0.25 mm assembly clearance each side)
CLEARANCE  = 0.25
POCKET_W   = DISP_PCB_W + 2 * CLEARANCE   # 34.5 mm
POCKET_H   = DISP_PCB_H + 2 * CLEARANCE   # 42.3 mm
POCKET_D   = DISP_TOTAL_T + 0.3           # 4.0 mm — slight Z clearance

# Outer body dimensions
BODY_W  = POCKET_W + 2 * WALL   # ≈ 38.1 mm
BODY_H  = POCKET_H + 2 * WALL   # ≈ 45.9 mm
BODY_T  = POCKET_D + WALL + 5.2  # front wall + pocket + rear controller space ≈ 11.0 mm

# Controller cavity (Nice!nano / Seeed XIAO — fits 22 × 37 mm footprint)
CTRL_W  = 22.5
CTRL_H  = 38.0
CTRL_T  = 4.2    # cavity depth

# USB-C port opening on the bottom edge (centred, 9.2 × 3.5 mm)
USB_W   = 9.2
USB_H   = 3.5
# vertical centre of the USB port on the bottom face:
#   front-face is at Z = +BODY_T/2 (CadQuery centres box on origin)
#   USB sits in the controller cavity zone, near front
USB_Z_FROM_FRONT = WALL + POCKET_D + 1.5   # distance from front face to USB centre

# Snap-fit groove around rear opening (for rear cap)
GROOVE_D = 0.8   # groove depth
GROOVE_H = 1.2   # groove height

# Rear cap dimensions
CAP_T    = 2.2   # total cap thickness
RIM_H    = GROOVE_H + 0.1   # rim height that enters the groove
RIM_T    = GROOVE_D - 0.1   # rim thickness (slight clearance)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
FRONT_WALL_T = WALL   # thickness of the front face wall (same as WALL)


def make_main_body() -> cq.Workplane:
    """Create the main case body with display pocket, window, and USB cutout."""

    # ---- outer shell -------------------------------------------------------
    body = (
        cq.Workplane("XY")
        .box(BODY_W, BODY_H, BODY_T)
        .edges("|Z")
        .fillet(CORNER_R)
    )

    # ---- display module pocket (recessed from front face, +Z direction) ----
    body = (
        body
        .faces(">Z")
        .workplane()
        .rect(POCKET_W, POCKET_H)
        .cutBlind(POCKET_D)
    )

    # ---- display active-area window (through the front wall) ---------------
    body = (
        body
        .faces(">Z")
        .workplane()
        .center(DISP_WIN_OFFSET_X, DISP_WIN_OFFSET_Y)
        .rect(DISP_WIN_W, DISP_WIN_H)
        .cutBlind(FRONT_WALL_T + 0.2)
    )

    # ---- controller cavity (recessed from rear face, -Z direction) ---------
    body = (
        body
        .faces("<Z")
        .workplane()
        .rect(CTRL_W, CTRL_H)
        .cutBlind(CTRL_T)
    )

    # ---- USB-C port slot on the bottom edge --------------------------------
    # The bottom face is at Y = -BODY_H/2.  We cut a slot through it.
    # Z centre of the slot relative to body centre:
    z_centre = BODY_T / 2 - USB_Z_FROM_FRONT
    body = (
        body
        .faces("<Y")
        .workplane()
        .center(0, z_centre)
        .rect(USB_W, USB_H)
        .cutThruAll()
    )

    # ---- snap-fit groove around the rear rim (all 4 walls) -----------------
    # The rear cap's rim slides into this groove.
    # Groove is cut just inside the rear opening edge.
    groove_z = -BODY_T / 2 + GROOVE_H / 2   # Z centre in body coords
    body = (
        body
        .faces("<Z")
        .workplane(offset=-0.001)
        .rect(BODY_W - 2 * (WALL - GROOVE_D), BODY_H - 2 * (WALL - GROOVE_D))
        .rect(BODY_W - 2 * WALL + 0.1, BODY_H - 2 * WALL + 0.1)
        .cutBlind(GROOVE_H)
    )

    return body


def make_rear_cap() -> cq.Workplane:
    """Create the rear snap-fit cap."""

    # outer plate with rounded corners matching body footprint
    cap = (
        cq.Workplane("XY")
        .box(BODY_W, BODY_H, CAP_T)
        .edges("|Z")
        .fillet(CORNER_R)
    )

    # inset rim that slides into the body groove
    # Rim is built as a perimeter frame on the top face (+Z)
    rim_outer_w = BODY_W - 2 * (WALL - GROOVE_D) - 0.2
    rim_outer_h = BODY_H - 2 * (WALL - GROOVE_D) - 0.2
    rim_inner_w = BODY_W - 2 * WALL - 0.4
    rim_inner_h = BODY_H - 2 * WALL - 0.4

    cap = (
        cap
        .faces(">Z")
        .workplane()
        .rect(rim_outer_w, rim_outer_h)
        .rect(rim_inner_w, rim_inner_h)
        .extrude(RIM_H)
    )

    return cap


def export_step(shape, path):
    cq.exporters.export(shape, path, cq.exporters.ExportTypes.STEP)
    print(f"  STEP → {path}")


def export_stl(shape, path):
    cq.exporters.export(shape, path, cq.exporters.ExportTypes.STL,
                        tolerance=0.01, angularTolerance=0.1)
    print(f"  STL  → {path}")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))

    print("Generating main case body …")
    body = make_main_body()
    export_step(body, os.path.join(out_dir, "case_body.step"))
    export_stl(body,  os.path.join(out_dir, "case_body.stl"))

    print("Generating rear cap …")
    cap = make_rear_cap()
    export_step(cap, os.path.join(out_dir, "rear_cap.step"))
    export_stl(cap,  os.path.join(out_dir, "rear_cap.stl"))

    print("\nDone.")
    print(f"Case outer dimensions : {BODY_W:.1f} × {BODY_H:.1f} × {BODY_T:.1f} mm")
    print(f"Display window        : {DISP_WIN_W:.1f} × {DISP_WIN_H:.1f} mm")
    print(f"Module pocket         : {POCKET_W:.1f} × {POCKET_H:.1f} × {POCKET_D:.1f} mm")
    print(f"Controller cavity     : {CTRL_W:.1f} × {CTRL_H:.1f} × {CTRL_T:.1f} mm")
