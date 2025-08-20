
# brick_core.py
from dataclasses import dataclass
from typing import Iterator, List, Tuple, Dict

@dataclass(frozen=True)
class Brick:
    lx: int = 200  # mm along X
    ly: int = 100  # mm along Y
    lz: int = 100  # mm along Z

BRICK = Brick()

def shell_volume_mm3(L:int, W:int, H:int, t:int, top_cover:bool=True) -> int:
    inner_L = max(L - 2*t, 0)
    inner_W = max(W - 2*t, 0)
    inner_H = max(H - (t if top_cover else 0), 0)
    return L*W*H - inner_L*inner_W*inner_H

def internal_volume_mm3(L:int, W:int, H:int, t:int, top_cover:bool=True) -> int:
    inner_L = max(L - 2*t, 0)
    inner_W = max(W - 2*t, 0)
    inner_H = max(H - (t if top_cover else 0), 0)
    return inner_L*inner_W*inner_H

def search_optimal_dims(num_bricks:int=10000, t:int=100, top_cover:bool=True,
                        L_max:int=20000, W_max:int=20000, H_max:int=10000):
    """
    Grid search over multiples of brick dims:
    - L multiple of 200
    - W multiple of 100
    - H multiple of 100
    Subject to shell volume == num_bricks * 200*100*100 mm^3.
    Maximizes internal volume.
    """
    brick_vol = BRICK.lx * BRICK.ly * BRICK.lz  # 2,000,000 mm^3
    target_shell = num_bricks * brick_vol
    best = None
    best_IV = -1

    for L in range(BRICK.lx, L_max+1, BRICK.lx):
        for W in range(BRICK.ly, W_max+1, BRICK.ly):
            for H in range(BRICK.lz, H_max+1, BRICK.lz):
                SV = shell_volume_mm3(L, W, H, t, top_cover)
                if SV == target_shell:
                    IV = internal_volume_mm3(L, W, H, t, top_cover)
                    if IV > best_IV:
                        best_IV = IV
                        best = (L, W, H, IV)
    return best  # (L,W,H,IV) in mm

def generate_bricks(L:int, W:int, H:int, t:int=100, top_cover:bool=True):
    """
    Yield bricks with origin (x,y,z) and orientation (200,100,100).
    Walls: t on four vertical sides; optional top slab t.
    Simple stretcher/half-lap bond by alternating 100 mm shift.
    """
    brick_L, brick_W, brick_H = BRICK.lx, BRICK.ly, BRICK.lz
    nx = L // brick_L
    ny = W // brick_W
    nz = H // brick_H

    for iz in range(nz):
        offset_x = 100 if (iz % 2 == 1) else 0
        for iy in range(ny):
            x_mm = -offset_x if offset_x else 0
            while x_mm < L:
                rot = False
                lx, ly, lz = brick_L, brick_W, brick_H
                px = x_mm if x_mm >= 0 else 0
                # rotate if offset causes overhang at either edge
                if (x_mm < 0) or (px + lx > L):
                    rot = True
                    lx, ly = brick_W, brick_L
                if px + lx > L:
                    break
                in_side = (px < t) or (px + lx > L - t) or (iy*brick_W < t) or ((iy+1)*brick_W > W - t)
                in_top  = top_cover and ((iz+1)*brick_H > H - t)
                if in_side or in_top:
                    yield {
                        "position": (int(px), int(iy*brick_W), int(iz*brick_H)),
                        "orientation": (int(lx), int(ly), int(lz))
                    }
                x_mm += lx

if __name__ == "__main__":
    best = search_optimal_dims()
    print(best)
