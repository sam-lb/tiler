import numpy as np
import cv2
from PIL import Image
from scipy.spatial import Delaunay
from scipy.ndimage import uniform_filter, gaussian_filter

def _compute_variance_map(img_np, ksize=9):
    img_f = img_np.astype(np.float32)
    mean = uniform_filter(img_f, size=(ksize, ksize, 1))
    sq_mean = uniform_filter(img_f ** 2, size=(ksize, ksize, 1))
    var = sq_mean - mean ** 2
    var_map = np.sum(var, axis=2)
    return var_map

def compute_adaptive_triangulation(img, num_adaptive_points=5000, save_target=None):
    img_np = np.array(img)
    h, w = img_np.shape[:2]

    var_map = _compute_variance_map(img_np, ksize=9)
    var_map = gaussian_filter(var_map, sigma=3)
    prob_map = var_map / np.sum(var_map)

    indices = np.random.choice(h * w, size=num_adaptive_points, p=prob_map.ravel())
    ys, xs = np.unravel_index(indices, (h, w))
    adaptive_points = np.column_stack((xs, ys)).astype(np.float32)

    corner_pts = np.array([[0, 0], [0, h - 1],
                        [w - 1, 0], [w - 1, h - 1]])
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

    output = Image.fromarray(output)
    if not (save_target is None): output.save(save_target)
    return output