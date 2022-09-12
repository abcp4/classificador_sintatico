"""
Esse arquivo recebe o resultado da divisão de orações e faz verificações sobre divisão.
Cada verificação vai levar a uma situação: "se", sujeito, ou sem sujeito.
"""
import spacy
from texto_usuario import texto_doc
from classifica_sujeito import get_sujeito
from classifica_sem_sujeito import get_sem_sujeito
from classifica_se import get_se

# Os comentários abaixo são para Marianna.
# Caso o programa apresente uma classificação inesperada, retirar as ''' acima e abaixo das duas linhas a seguir:
# Rodar a frase de novo
# Selecione e copie o resultado do detalhamento para análise posterior
# Depois, colocar de volta as ''' acima e abaixo das duas linhas
"""
for t in texto_doc:
    print(t.text, t.lemma_, t.pos_, t.dep_, str(t.morph), t.head.text)
"""


def check_sujeito():

    # Casos de "se" conjunção (t.dep_ = "mark") não vão para classifica_se.py
    # "se ele se machucou" --> está em classifica_sujeito
    # problema: "se havia problemas" --> como PRON expl e sendo classificado errado, ver "se escrevia um livro" ok
    se = [
        t
        for t in texto_doc
        if t.text == "se"
        if t.dep_ in ("nsubj", "obj", "expl", "xcomp")
    ]

    if se:
        print(get_se())
    else:
        sujeito = [t for t in texto_doc if t.dep_ == "nsubj"]
        if sujeito:
            print(get_sujeito())
        else:
            print(get_sem_sujeito())


check_sujeito()
