
# visualize.py
import argparse, csv
import matplotlib.pyplot as plt

def load_bricks(csv_path):
    bricks = []
    with open(csv_path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            bricks.append({k:int(row[k]) for k in row})
    return bricks

def plot_top(bricks, save_path):
    xs = [b["x_mm"] for b in bricks]
    ys = [b["y_mm"] for b in bricks]
    lx = [b["lx_mm"] for b in bricks]
    ly = [b["ly_mm"] for b in bricks]
    L = max(x+dx for x,dx in zip(xs,lx))
    W = max(y+dy for y,dy in zip(ys,ly))

    fig, ax = plt.subplots(figsize=(8, 6))
    for x,y,dx,dy in zip(xs,ys,lx,ly):
        ax.add_patch(plt.Rectangle((x/1000, y/1000), dx/1000, dy/1000, fill=False))
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-0.1, L/1000 + 0.1)
    ax.set_ylim(-0.1, W/1000 + 0.1)
    ax.set_xlabel("Length (m)")
    ax.set_ylabel("Width (m)")
    ax.set_title("Top View (brick footprints)")
    fig.savefig(save_path, dpi=200, bbox_inches="tight")

def plot_side(bricks, save_path):
    xs = [b["x_mm"] for b in bricks]
    zs = [b["z_mm"] for b in bricks]
    lx = [b["lx_mm"] for b in bricks]
    lz = [b["lz_mm"] for b in bricks]
    L = max(x+dx for x,dx in zip(xs,lx))
    H = max(z+dz for z,dz in zip(zs,lz))

    fig, ax = plt.subplots(figsize=(10, 4))
    for x,z,dx,dz in zip(xs,zs,lx,lz):
        ax.add_patch(plt.Rectangle((x/1000, z/1000), dx/1000, dz/1000, fill=False))
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-0.1, L/1000 + 0.1)
    ax.set_ylim(-0.1, H/1000 + 0.1)
    ax.set_xlabel("Length (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Side View (elevation)")
    fig.savefig(save_path, dpi=200, bbox_inches="tight")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="out/bricks.csv")
    ap.add_argument("--top", default="top_view.png")
    ap.add_argument("--side", default="side_view.png")
    args = ap.parse_args()
    bricks = load_bricks(args.csv)
    plot_top(bricks, args.top)
    plot_side(bricks, args.side)
    print(f"Saved {args.top} and {args.side}")
