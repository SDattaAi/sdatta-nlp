


def clip_results(texts, image, clip_model, clip_processor):
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1)
    # pritn the max probability and the text that gave that probability
    print("clip max prob text:", texts[probs.argmax()], end=" ")
    print("clip max prob:", probs.max().tolist())
    return probs