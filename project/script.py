from project.load_model import load_model
from project.tokenize import nlp, tokenize

model = load_model()

print(model.steps[0])