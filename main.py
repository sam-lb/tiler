from PIL import Image
from tiler import compute_adaptive_triangulation, compute_adaptive_triangulation_gif

# IMAGE_NAME = "gradation.jpg"
# INPUT_FILE = "./test_images/{}".format(IMAGE_NAME)
# OUTPUT_FILE = "./out_images/{}_processed.jpg".format(IMAGE_NAME.split(".")[0])

GIF_NAME = "blob.gif"
INPUT_FILE = "./test_images/{}".format(GIF_NAME)
OUTPUT_FILE = "./out_images/{}_processed.gif".format(GIF_NAME.split(".")[0])

if __name__ == "__main__":
    # img = Image.open(INPUT_FILE).convert("RGB")
    # compute_adaptive_triangulation(img, save_target=OUTPUT_FILE, num_adaptive_points=100)

    gif = Image.open(INPUT_FILE)
    compute_adaptive_triangulation_gif(gif, save_target=OUTPUT_FILE, num_adaptive_points=200)