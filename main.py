import csv

def generate_bricks(nx, ny, nz, length, width, height, color, csv_file="bricks.csv"):
    with open(csv_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y", "z", "length", "width", "height", "color"])
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    x = i * length
                    y = j * width
                    z = k * height
                    writer.writerow([x, y, z, length, width, height, color])

if __name__ == "__main__":
    # Example: 100 x 10 x 10 = 10,000 bricks
    generate_bricks(
        nx=100, ny=10, nz=10,
        length=2, width=1, height=1,
        color="red"
    )
    print("✅ bricks.csv generated successfully.")
