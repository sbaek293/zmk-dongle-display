/*
 * ZMK Dongle Display Case — OpenSCAD
 * 1.69-inch flat display (ST7789V, 240×280 px)
 *
 * Display module specifications (typical 1.69" from AliExpress,
 * item 1005007346976745):
 *   PCB overall:   34.0 × 41.8 mm
 *   Active area:   27.8 × 33.4 mm (240 × 280 px)
 *   PCB thickness: 1.6 mm
 *   Module height: 3.7 mm (PCB + display glass stack)
 *
 * Case design inspired by carrefinho/prospector and BambuHelper.
 * Intended controller: Nice!nano v2 / Seeed XIAO nRF5340 (or similar).
 *
 * Usage:
 *   Set RENDER to one of:
 *     "body"  — main case body only
 *     "cap"   — rear snap-fit cap only
 *     "both"  — body + cap side-by-side (default, for preview)
 */

// ─── What to render ──────────────────────────────────────────────────────────
RENDER = "both";   // "body" | "cap" | "both"

// ─── Display module dimensions (1.69" ST7789V, 240×280) ──────────────────────
DISP_PCB_W        = 34.0;   // PCB width  (X)
DISP_PCB_H        = 41.8;   // PCB height (Y)
DISP_PCB_T        = 1.6;    // PCB thickness
DISP_GLASS_T      = 2.1;    // display glass + bezel thickness above PCB
DISP_TOTAL_T      = DISP_PCB_T + DISP_GLASS_T;   // ≈ 3.7 mm

DISP_WIN_W        = 27.8;   // active display window width  (X)
DISP_WIN_H        = 33.4;   // active display window height (Y)

// Active-area offset from PCB centre (horizontally centred,
// shifted 0.5 mm upward relative to PCB centre on this module)
DISP_WIN_OFFSET_X = 0.0;
DISP_WIN_OFFSET_Y = 0.5;

// ─── Case geometry constants ──────────────────────────────────────────────────
WALL       = 1.8;   // wall / shell thickness (mm)
CORNER_R   = 2.5;   // outer corner fillet radius (mm)

// Pocket for the display module (0.25 mm assembly clearance each side)
CLEARANCE  = 0.25;
POCKET_W   = DISP_PCB_W + 2 * CLEARANCE;       // 34.5 mm
POCKET_H   = DISP_PCB_H + 2 * CLEARANCE;       // 42.3 mm
POCKET_D   = DISP_TOTAL_T + 0.3;               // 4.0 mm — slight Z clearance

// Outer body dimensions
BODY_W  = POCKET_W + 2 * WALL;   // ≈ 38.1 mm
BODY_H  = POCKET_H + 2 * WALL;   // ≈ 45.9 mm
BODY_T  = POCKET_D + WALL + 5.2; // front wall + pocket + rear controller space ≈ 11.0 mm

// Controller cavity (Nice!nano / Seeed XIAO — 22 × 37 mm footprint)
CTRL_W  = 22.5;
CTRL_H  = 38.0;
CTRL_T  = 4.2;   // cavity depth

// USB-C port opening on the bottom edge (centred, 9.2 × 3.5 mm)
USB_W   = 9.2;
USB_H   = 3.5;
USB_Z_FROM_FRONT = WALL + POCKET_D + 1.5;  // distance from front face to USB centre

// Snap-fit groove around the rear opening (for rear cap)
GROOVE_D = 0.8;   // groove depth (into the wall)
GROOVE_H = 1.2;   // groove height (along Z)

// Rear cap dimensions
CAP_T    = 2.2;                  // total cap thickness
RIM_H    = GROOVE_H + 0.1;      // rim height that enters the groove
RIM_T    = GROOVE_D - 0.1;      // rim thickness (slight clearance)

// ─── $fn — global fragment count for smooth curves ───────────────────────────
$fn = 64;

// ─── Utility: rounded rectangle (2-D), centred at origin ─────────────────────
module rounded_rect(w, h, r) {
    offset(r = r)
        square([w - 2 * r, h - 2 * r], center = true);
}

// ─── Utility: rounded box (3-D), centred at origin ───────────────────────────
// Rounded only on the four vertical (Z) edges, matching the CadQuery design.
module rounded_box(w, h, d, r) {
    linear_extrude(height = d, center = true)
        rounded_rect(w, h, r);
}

// ─── Main case body ───────────────────────────────────────────────────────────
module main_body() {
    difference() {

        // 1. Outer shell — rounded box centred at origin
        rounded_box(BODY_W, BODY_H, BODY_T, CORNER_R);

        // 2. Display module pocket — recessed from the front face (+Z)
        //    The front face is at Z = +BODY_T/2.
        //    Pocket extends POCKET_D into the body.
        translate([0, 0, BODY_T/2 - POCKET_D/2 + 0.001])
            cube([POCKET_W, POCKET_H, POCKET_D + 0.01], center = true);

        // 3. Active-area window — cuts through the remaining front wall
        //    (thickness = WALL = 1.8 mm), centred at DISP_WIN_OFFSET.
        translate([DISP_WIN_OFFSET_X,
                   DISP_WIN_OFFSET_Y,
                   BODY_T/2 - POCKET_D - WALL/2])
            cube([DISP_WIN_W, DISP_WIN_H, WALL + 0.4], center = true);

        // 4. Controller cavity — recessed from the rear face (-Z)
        //    Rear face is at Z = -BODY_T/2.
        translate([0, 0, -BODY_T/2 + CTRL_T/2 - 0.001])
            cube([CTRL_W, CTRL_H, CTRL_T + 0.01], center = true);

        // 5. USB-C port slot on the bottom edge (-Y face)
        //    Z centre of the slot: distance USB_Z_FROM_FRONT from front face.
        usb_z = BODY_T/2 - USB_Z_FROM_FRONT;
        translate([0, 0, usb_z])
            cube([USB_W, BODY_H + 1.0, USB_H], center = true);

        // 6. Snap-fit groove around the rear rim
        //    Cut a frame-shaped channel just inside the rear opening edge.
        //    The groove runs from the rear face inward by GROOVE_H.
        groove_outer_w = BODY_W - 2 * (WALL - GROOVE_D);
        groove_outer_h = BODY_H - 2 * (WALL - GROOVE_D);
        groove_inner_w = BODY_W - 2 * WALL;
        groove_inner_h = BODY_H - 2 * WALL;

        translate([0, 0, -BODY_T/2 + GROOVE_H/2 - 0.001])
            difference() {
                cube([groove_outer_w, groove_outer_h, GROOVE_H + 0.01],
                     center = true);
                cube([groove_inner_w + 0.1, groove_inner_h + 0.1, GROOVE_H + 0.1],
                     center = true);
            }
    }
}

// ─── Rear snap-fit cap ────────────────────────────────────────────────────────
module rear_cap() {
    rim_outer_w = BODY_W - 2 * (WALL - GROOVE_D) - 0.2;
    rim_outer_h = BODY_H - 2 * (WALL - GROOVE_D) - 0.2;
    rim_inner_w = BODY_W - 2 * WALL - 0.4;
    rim_inner_h = BODY_H - 2 * WALL - 0.4;

    union() {
        // Base plate with rounded corners
        rounded_box(BODY_W, BODY_H, CAP_T, CORNER_R);

        // Inset rim on the inner face (+Z)
        translate([0, 0, CAP_T/2 + RIM_H/2])
            difference() {
                cube([rim_outer_w, rim_outer_h, RIM_H], center = true);
                cube([rim_inner_w, rim_inner_h, RIM_H + 0.1], center = true);
            }
    }
}

// ─── Top-level render selection ───────────────────────────────────────────────
if (RENDER == "body") {
    main_body();
} else if (RENDER == "cap") {
    rear_cap();
} else {
    // "both" — place side-by-side with a small gap
    translate([-BODY_W/2 - 2, 0, 0])
        main_body();
    translate([ BODY_W/2 + 2, 0, 0])
        rear_cap();
}
