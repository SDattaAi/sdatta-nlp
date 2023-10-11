from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
model_name = "deepset/deberta-v3-base-squad2"
# a) Get predictions
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
QA_input = {
    'question': 'give the words that describe the item in list.'
                'for example: [''comfortable'', ''underwear'', ''made'', ''from'', ''modal'', ''micro'', ''by'', ''tencel'']',
    'context': 'Comfortable underwear made from Modal Micro by TENCEL. TENCEL™ Modal fibers of natural origin are produced in an environmentally conscious manner, while the Micro technology makes the fabric exceptionally soft and fine. The camisole in the fashion color Malachite is particularly comfortable due to the elastic lace band at the neckline and adjustable straps. The model measures 177 cm and wears a DE 36 (German clothing size). Bust: 81 cm. Waist: 60 cm. Hips: 87 cm.'
}
res = nlp(QA_input)
print(res)
# b) Load model & tokenizer
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
