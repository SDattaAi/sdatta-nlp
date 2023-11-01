
import torch

def text_image_clip_results(texts, image, clip_model, clip_processor):
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
    print(logits_per_image)




    # show all probabilities
    probs = logits_per_image.softmax(dim=1)
    # pritn the max probability and the text that gave that probability
    print("clip max prob text:", texts[probs.argmax()], end=" ")
    print("clip max prob:", probs.max().tolist())
    return probs

def text_text_clip_similarity(item_description,general_texts, clip_model, clip_processor):
    texts = [item_description] + general_texts
    inputs = clip_processor(text=texts, return_tensors="pt", padding=True)
    text_features = clip_model.get_text_features(**inputs)
    similarity = torch.nn.functional.cosine_similarity(
        text_features.unsqueeze(1), text_features.unsqueeze(0), dim=2
    )[0][1:]
    return similarity