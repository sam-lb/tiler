# tiler

Small python utility to turn trianglate images and do flat per-triangle coloring. The points are placed according to how much color variance is in each part of the image.

### Example

```python3

from PIL import Image
from tiler import compute_adaptive_triangulation

img = Image.open("blue_bird.jpg").convert("RGB")
compute_adaptive_triangulation(img, save_target="blue_bird_processed.jpg", num_adaptive_points=3000)

```

#### Before

![blue bird](https://raw.githubusercontent.com/sam-lb/tiler/refs/heads/master/demo/blue_bird.jpg)

#### After

![blue bird processed](https://raw.githubusercontent.com/sam-lb/tiler/refs/heads/master/demo/blue_bird_processed.jpg)