import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def draw_brick(ax, x, y, z, length, width, height, color):
    # Define vertices of cuboid
    vertices = [
        [x, y, z],
        [x + length, y, z],
        [x + length, y + width, z],
        [x, y + width, z],
        [x, y, z + height],
        [x + length, y, z + height],
        [x + length, y + width, z + height],
        [x, y + width, z + height]
    ]
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[4], vertices[7], vertices[3], vertices[0]]
    ]
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, edgecolors="k", linewidths=0.2))

def visualize_bricks(csv_file="bricks.csv", fast=True):
    df = pd.read_csv(csv_file)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    if fast:
        # Approximate by scatter instead of drawing every face (for >10k bricks)
        ax.scatter(df["x"], df["y"], df["z"], c=df["color"], marker="s", s=2)
    else:
        for _, row in df.iterrows():
            draw_brick(ax, row.x, row.y, row.z, row.length, row.width, row.height, row.color)

    # Set limits
    ax.set_xlim(0, df["x"].max() + df["length"].max())
    ax.set_ylim(0, df["y"].max() + df["width"].max())
    ax.set_zlim(0, df["z"].max() + df["height"].max())

    # Add grid lines
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.show()

if __name__ == "__main__":
    visualize_bricks("bricks.csv", fast=True)
