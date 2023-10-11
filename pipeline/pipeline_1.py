# %%
from PIL import Image
from transformers import YolosFeatureExtractor, YolosForObjectDetection
from torchvision.transforms import ToTensor
from vision_and_nlp_models.yolo_utils import *
from vision_and_nlp_models.utils import fix_channels
from transformers import CLIPProcessor, CLIPModel
from vision_and_nlp_models.clip_utils import clip_results
import json
import warnings
warnings.filterwarnings("ignore")
# %%
# inputs :
yolo_threshold = 0.9
IMAGE_PATH = "/Users/guybasson/Desktop/sdatta-nlp/photos/japan-wrap-dress.jpg"
with open('/Users/guybasson/Desktop/sdatta-nlp/configs/yolo_fashion_cats.json', 'r') as f:
    yolo_cats = json.load(f)
clip_model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
clip_processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")
MODEL_NAME = "valentinafeve/yolos-fashionpedia"
yolo_feature_extractor = YolosFeatureExtractor.from_pretrained('hustvl/yolos-small')
yolo_model = YolosForObjectDetection.from_pretrained(MODEL_NAME)
image = Image.open(open(IMAGE_PATH, "rb"))
image = fix_channels(ToTensor()(image))
image = image.resize((600, 800))
inputs = yolo_feature_extractor(images=image, return_tensors="pt")
outputs = yolo_model(**inputs)
probs = outputs.logits.softmax(-1)[0, :, :-1]
keep = probs.max(-1).values > yolo_threshold
bboxes_scaled = rescale_bboxes(outputs.pred_boxes[0, keep].cpu(), image.size)
plot_results(image, probs[keep], bboxes_scaled, yolo_cats)
i = 0
item_clip_texts = ["bra",
                   "shirt",
                   "dress",
                   "shoes",
                   "pants", ]
color_clip_texts = ["red",
                    "blue",
                    "green",
                    "black",
                    "white",
                    "brown", ]
season_clip_texts = ["summer",
                     "winter",
                     "spring",
                     "autumn", ]
weather_clip_texts = ["rain",
                      "snow",
                      "sun",
                      "clouds", ]
for p, (xmin, ymin, xmax, ymax) in zip(probs[keep], bboxes_scaled.tolist()):
    i = i + 1
    print()
    cl = p.argmax()
    cl = p.argmax()
    print("item:", i, " cat:", yolo_cats[cl])
    cropped_img = image.crop((xmin, ymin, xmax, ymax))
    cropped_img = cropped_img.resize((224, 224))
    # plot with plt.imshow(cropped_img) with i in title and cat
    plt.imshow(cropped_img)
    plt.title("i: " + str(i) + " yolo cat: " + yolo_cats[cl])
    plt.show()


    clip_results(item_clip_texts, cropped_img, clip_model, clip_processor)
    clip_results(color_clip_texts, cropped_img, clip_model, clip_processor)
    clip_results(season_clip_texts, cropped_img, clip_model, clip_processor)
    clip_results(weather_clip_texts, cropped_img, clip_model, clip_processor)
