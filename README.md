
# Brick Cuboid Generator (100 mm wall)

Generates the **location + orientation** of every brick (200×100×100 mm) to build a **maximum internal-volume** hollow cuboid shell with **wall thickness = 100 mm** using exactly **10,000 bricks**.

## Quick start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install matplotlib
python main.py --out out                 # writes out/bricks.csv and out/bricks.json
python visualize.py --csv out/bricks.csv --top top.png --side side.png
```

## Output format
- **CSV**: `x_mm,y_mm,z_mm,lx_mm,ly_mm,lz_mm` (origin and orientation per brick)
- **JSON**: metadata + same list

## Publish to GitHub (public)
Replace `<USER>` with your GitHub username and run:
```bash
git init
git add .
git commit -m "brick cuboid (100mm wall)"
git branch -M main
gh repo create <USER>/brick-cuboid-100mm --public --source=. --remote=origin --push
# or manually:
# git remote add origin https://github.com/<USER>/brick-cuboid-100mm.git
# git push -u origin main
```

After pushing, submit:
- **Repo link**: `https://github.com/<USER>/brick-cuboid-100mm`
