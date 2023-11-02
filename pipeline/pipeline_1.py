# %%
from PIL import Image
from transformers import YolosFeatureExtractor, YolosForObjectDetection
from torchvision.transforms import ToTensor
from vision_and_nlp_models.yolo_utils import *
from vision_and_nlp_models.utils import fix_channels
from transformers import CLIPProcessor, CLIPModel
from vision_and_nlp_models.clip_utils import text_image_clip_results, text_text_clip_similarity
import json
import warnings
warnings.filterwarnings("ignore")
# %%
# inputs :
yolo_threshold = 0.5
item_name = "zara_item_1"
image_path = "/Users/guybasson/Desktop/sdatta-nlp/photos/" + item_name + ".jpg"
description_path = "/Users/guybasson/Desktop/sdatta-nlp/descriptions/" + item_name + ".txt"
clip_text_path = "/Users/guybasson/Desktop/sdatta-nlp/clip_texts/fashion_general.json"
# read the description
with open(description_path, 'r') as f:
    description = f.read()
with open('/Users/guybasson/Desktop/sdatta-nlp/configs/yolo_fashion_cats.json', 'r') as f:
    yolo_cats = json.load(f)
with open(clip_text_path, 'r') as f:
    dict_of_clip_texts = json.load(f)
clip_model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
clip_processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

# Example texts to compare
print("description: ", description)
texts = ["blue t-shirt", "Bra", "Shirt", "Dress", "Skirt", "Pants", "Hat", "sweatshirt"]

print(text_text_clip_similarity(description,texts, clip_model, clip_processor))
MODEL_NAME = "valentinafeve/yolos-fashionpedia"
yolo_feature_extractor = YolosFeatureExtractor.from_pretrained('hustvl/yolos-small')
yolo_model = YolosForObjectDetection.from_pretrained(MODEL_NAME)
image = Image.open(open(image_path, "rb"))
def yolo_clip_pipeline_1(image, description, dict_of_clip_texts, yolo_threshold, yolo_cats, yolo_feature_extractor, yolo_model, clip_model, clip_processor):
    image = fix_channels(ToTensor()(image))
    image = image.resize((600, 800))
    inputs = yolo_feature_extractor(images=image, return_tensors="pt")
    outputs = yolo_model(**inputs)
    probs = outputs.logits.softmax(-1)[0, :, :-1]
    keep = probs.max(-1).values > yolo_threshold
    bboxes_scaled = rescale_bboxes(outputs.pred_boxes[0, keep].cpu(), image.size)
    dict_clip_image_text_probability = {}
    if len(bboxes_scaled) == 0:
        print("No items found, take the whole image")
        dict_of_probs_per_text = {}
        for key in dict_of_clip_texts.keys():
            clip_probs = text_image_clip_results(dict_of_clip_texts[key], image, clip_model, clip_processor)
            dict_probs = {}
            i = 0
            for dict_of_clip_text in dict_of_clip_texts[key]:
                dict_probs[dict_of_clip_text] = clip_probs[0][i].item()
                i += 1
            print("dict_probs: ", dict_probs)
            dict_of_probs_per_text[key] = dict_probs
        dict_clip_image_text_probability['whole_image'] = dict_of_probs_per_text
    else:
        print("Found ", len(bboxes_scaled), " items")
        i = 0
        for p, (xmin, ymin, xmax, ymax) in zip(probs[keep], bboxes_scaled.tolist()):
            cl = p.argmax()
            cl = p.argmax()
            yolo_cat = yolo_cats[cl]
            if yolo_cat not in ['neckline', 'sleeve']:
                print("item:", i, " yolo_cat:", yolo_cat)
                cropped_img = image.crop((xmin, ymin, xmax, ymax))
                cropped_img = cropped_img.resize((224, 224))
                plt.imshow(cropped_img)
                plt.title("i: " + str(i) + " yolo cat: " + yolo_cats[cl])
                plt.show()
                dict_of_probs_per_text = {}
                for key in dict_of_clip_texts.keys():
                    print("key: ", key)
                    clip_probs = text_image_clip_results(dict_of_clip_texts[key], cropped_img, clip_model, clip_processor)
                    dict_probs = {}
                    i = 0
                    for dict_of_clip_text in dict_of_clip_texts[key]:
                        dict_probs[dict_of_clip_text] = clip_probs[0][i].item()
                        i += 1
                    print("dict_probs: ", dict_probs)
                    dict_of_probs_per_text[key] = dict_probs
                dict_clip_image_text_probability[yolo_cat] = dict_of_probs_per_text
        i = i + 1
    dict_clip_text_text_similarity = {}
    for key in dict_of_clip_texts.keys():
        dict_clip_text_text_similarity[key] = text_text_clip_similarity(description, dict_of_clip_texts[key], clip_model, clip_processor)
        dict_sim = {}
        i = 0
        for dict_of_clip_text in dict_of_clip_texts[key]:
            dict_sim[dict_of_clip_text] = dict_clip_text_text_similarity[key][i].item()
            i += 1
        print("dict_sim: ", dict_sim)
        dict_clip_text_text_similarity[key] = dict_sim

    dict_all = {}
    dict_all['dict_clip_image_text_probability'] = dict_clip_image_text_probability
    dict_all['dict_clip_text_text_similarity'] = {"similarity":dict_clip_text_text_similarity,
                                                  "description":description}
    return dict_all
dict_all = yolo_clip_pipeline_1(image, description, dict_of_clip_texts, yolo_threshold, yolo_cats, yolo_feature_extractor, yolo_model, clip_model, clip_processor)
print("dict_all:", dict_all)