
# main.py
import argparse, json, csv, os
from brick_core import search_optimal_dims, generate_bricks

def run(outdir:str, top_cover:bool=True):
    os.makedirs(outdir, exist_ok=True)
    best = search_optimal_dims(t=100, top_cover=top_cover,
                               L_max=20000, W_max=20000, H_max=10000)
    if not best:
        raise SystemExit("No feasible dimensions found in search box.")
    L, W, H, IV = best
    print(f"Optimal outer (mm): L={L}, W={W}, H={H}")
    inner_H = H-100 if top_cover else H
    print(f"Internal (mm): {L-200} x {W-200} x {inner_H}")
    print(f"Internal volume (m^3): {IV/1e9:.3f}")
    print("Generating brick placements...")

    placements = list(generate_bricks(L, W, H, t=100, top_cover=top_cover))
    with open(os.path.join(outdir, "bricks.json"), "w") as f:
        json.dump({
            "outer_mm": {"L":L,"W":W,"H":H},
            "wall_mm": 100,
            "top_cover": top_cover,
            "count": len(placements),
            "bricks": placements
        }, f, indent=2)

    with open(os.path.join(outdir, "bricks.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x_mm","y_mm","z_mm","lx_mm","ly_mm","lz_mm"])
        for b in placements:
            x,y,z = b["position"]
            lx,ly,lz = b["orientation"]
            w.writerow([x,y,z,lx,ly,lz])
    print(f"Wrote {len(placements)} bricks to {outdir}/bricks.(json|csv)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out", help="output folder")
    ap.add_argument("--no-top", action="store_true", help="omit top cover")
    args = ap.parse_args()
    run(args.out, top_cover=(not args.no_top))
