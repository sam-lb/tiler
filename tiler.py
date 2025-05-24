import numpy as np
from PIL import Image
import cv2
import os
from scipy.spatial import Delaunay
from scipy.ndimage import uniform_filter, gaussian_filter

IMAGE_NAME = "blue_bird.jpg"
INPUT_FILE = "./test_images/{}".format(IMAGE_NAME)
OUTPUT_FILE = "./out_images/{}_processed.jpg".format(IMAGE_NAME.split(".")[0])

img = Image.open(INPUT_FILE).convert("RGB")
img_np = np.array(img)
h, w = img_np.shape[:2]

def compute_variance_map(img_np, ksize=9):
    img_f = img_np.astype(np.float32)
    mean = uniform_filter(img_f, size=(ksize, ksize, 1))
    sq_mean = uniform_filter(img_f**2, size=(ksize, ksize, 1))
    var = sq_mean - mean**2
    var_map = np.sum(var, axis=2)
    return var_map

var_map = compute_variance_map(img_np, ksize=9)
var_map = gaussian_filter(var_map, sigma=3)
prob_map = var_map / np.sum(var_map)

# honestly should probably make this a function of the image size
num_adaptive_points = 3000
indices = np.random.choice(h * w, size=num_adaptive_points, p=prob_map.ravel())
ys, xs = np.unravel_index(indices, (h, w))
adaptive_points = np.column_stack((xs, ys)).astype(np.float32)

corner_pts = np.array([[0,0], [0,h-1], [w-1,0], [w-1,h-1]])
points = np.vstack((adaptive_points, corner_pts))

tri = Delaunay(points)
output = np.zeros_like(img_np)

for simplex in tri.simplices:
    pts = points[simplex].astype(np.int32)
    cx, cy = np.mean(pts, axis=0).astype(int)
    cx = np.clip(cx, 0, w - 1)
    cy = np.clip(cy, 0, h - 1)
    color = img_np[cy, cx].tolist()
    cv2.fillPoly(output, [pts], color)

Image.fromarray(output).save(OUTPUT_FILE)
print(f"Saved adaptive triangulated image to {OUTPUT_FILE}")
