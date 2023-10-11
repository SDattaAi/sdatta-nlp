#%%
from PIL import Image
from transformers import YolosFeatureExtractor, YolosForObjectDetection
from torchvision.transforms import ToTensor
from vision_and_nlp_models.yolo_utils import *
from vision_and_nlp_models.utils import  fix_channels
from transformers import CLIPProcessor, CLIPModel
#%%
# inputs :
yolo_threshold = 0.9
IMAGE_PATH = "/Users/guybasson/Desktop/sdatta-nlp/photos/japan-wrap-dress.jpg"
#%%
# This is the order of the categories list. NO NOT CHANGE. Just for visualization purposes
yolo_cats = ['shirt, blouse', 'top, t-shirt, sweatshirt', 'sweater', 'cardigan', 'jacket', 'vest', 'pants', 'shorts', 'skirt', 'coat', 'dress', 'jumpsuit', 'cape', 'glasses', 'hat', 'headband, head covering, hair accessory', 'tie', 'glove', 'watch', 'belt', 'leg warmer', 'tights, stockings', 'sock', 'shoe', 'bag, wallet', 'scarf', 'umbrella', 'hood', 'collar', 'lapel', 'epaulette', 'sleeve', 'pocket', 'neckline', 'buckle', 'zipper', 'applique', 'bead', 'bow', 'flower', 'fringe', 'ribbon', 'rivet', 'ruffle', 'sequin', 'tassel']
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
img = visualize_predictions(image, outputs, yolo_cats, threshold=yolo_threshold)
probs = outputs.logits.softmax(-1)[0, :, :-1]
keep = probs.max(-1).values > yolo_threshold

# convert predicted boxes from [0; 1] to image scales
bboxes_scaled = rescale_bboxes(outputs.pred_boxes[0, keep].cpu(), image.size)
for p, (xmin, ymin, xmax, ymax) in zip(probs, bboxes_scaled.tolist()):
    print("p:", p)
    # print cat
    p_argmax = p.argmax()
    print("p_argmax", p_argmax)
    cat = yolo_cats[p_argmax]
    print("cat:", cat)

    cropped_img = image.crop((xmin, ymin, xmax, ymax))
    texts = ["a japanese dress with yellow flowers",
             "a summer dress with pink flowers",
             "a pink bra",
             "shoes",]
    inputs = clip_processor(text=texts, images=cropped_img, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1)
    print("probs", probs)
    for text in texts:
        print("text:", text, end=", ")
        print("prob:", probs[0][texts.index(text)].item())

