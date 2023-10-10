#%%
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import matplotlib.pyplot as plt
from utils import fix_channels
from torchvision.transforms import ToTensor

#%%
model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")
#%%
IMAGE_PATH = "/Users/guybasson/Desktop/sdatta-nlp/photos/japan-wrap-dress.jpg"
texts = ["a japanese dress with yellow flowers", "a summer dress with pink flowers", "a pink bra"]
image = Image.open(IMAGE_PATH)

#%%
inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)
outputs = model(**inputs)
logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1)
print("probs", probs)
for text in texts:
    print("text:", text, end=", ")
    print("prob:", probs[0][texts.index(text)].item())
#%%
# plot the image
pil_img = Image.open(open(IMAGE_PATH, "rb"))
pil_img = fix_channels(ToTensor()(image))
pil_img = image.resize((600, 800))

plt.figure(figsize=(12,10))
plt.imshow(pil_img)
ax = plt.gca()
plt.axis('off')
plt.show()