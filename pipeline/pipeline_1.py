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
yolo_threshold = 0.5
item_name = "zara_item_2"
image_path = "/Users/guybasson/Desktop/sdatta-nlp/photos/" + item_name + ".jpg"
description_path = "/Users/guybasson/Desktop/sdatta-nlp/descriptions/" + item_name + ".txt"
clip_text_path = "/Users/guybasson/Desktop/sdatta-nlp/clip_texts/" + item_name + ".json"
# read the description
with open(description_path, 'r') as f:
    description = f.read()
with open('/Users/guybasson/Desktop/sdatta-nlp/configs/yolo_fashion_cats.json', 'r') as f:
    yolo_cats = json.load(f)
with open(clip_text_path, 'r') as f:
    dict_of_clip_texts = json.load(f)
clip_model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
clip_processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")
MODEL_NAME = "valentinafeve/yolos-fashionpedia"
yolo_feature_extractor = YolosFeatureExtractor.from_pretrained('hustvl/yolos-small')
yolo_model = YolosForObjectDetection.from_pretrained(MODEL_NAME)
image = Image.open(open(image_path, "rb"))
image = fix_channels(ToTensor()(image))
image = image.resize((600, 800))
inputs = yolo_feature_extractor(images=image, return_tensors="pt")
outputs = yolo_model(**inputs)
probs = outputs.logits.softmax(-1)[0, :, :-1]
keep = probs.max(-1).values > yolo_threshold
bboxes_scaled = rescale_bboxes(outputs.pred_boxes[0, keep].cpu(), image.size)
plot_results(image, probs[keep], bboxes_scaled, yolo_cats)
if len(bboxes_scaled) == 0:
    print("No items found, take the whole image")
    for key in dict_of_clip_texts.keys():
        clip_results(dict_of_clip_texts[key], image, clip_model, clip_processor)
else:
    print("Found ", len(bboxes_scaled), " items")
    i = 0
    for p, (xmin, ymin, xmax, ymax) in zip(probs[keep], bboxes_scaled.tolist()):
        i = i + 1
        print()
        cl = p.argmax()
        cl = p.argmax()
        cat = yolo_cats[cl]
        print("item:", i, " cat:", cat)
        cropped_img = image.crop((xmin, ymin, xmax, ymax))
        cropped_img = cropped_img.resize((224, 224))
        plt.imshow(cropped_img)
        plt.title("i: " + str(i) + " yolo cat: " + yolo_cats[cl])
        plt.show()
        for key in dict_of_clip_texts.keys():
            clip_results(dict_of_clip_texts[key], cropped_img, clip_model, clip_processor)

print("Real description of product: ", description)