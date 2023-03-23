from sujeito.classifica_sem_sujeito import get_sem_sujeito
from sujeito.classifica_sujeito import get_sujeito
from sujeito.classifica_se import get_se


def num_sujeito(doc,nlp):
    # Checando como o Spacy está classificando as palavras no doc (= resultado da divisão.)
    for t in doc:
        print(t.text, t.dep_)
    sujeito = [t for t in doc if t.dep_ in ("nsubj", "nsubj:pass")]
    # Checando se tem sujeito. O código final vai ter várias subdivisões dos casos com sujeito e dos casos sem sujeito
    return len(sujeito)


def check_se(texto_doc):

    # Casos de "se" conjunção (t.dep_ = "mark") não vão para classifica_se.py
    # "se ele se machucou" --> está em classifica_sujeito
    # problema: "se havia problemas" --> como PRON expl e sendo classificado errado, ver "se escrevia um livro" ok
    print('texto_doc: ',texto_doc)
    #print([type(t) for t in texto_doc])
    se = [
        t
        for t in texto_doc
        if t.text == "se"
        if t.dep_ in ("nsubj", "obj", "expl", "xcomp")
        ]
    return se

def analisa_sujeito(doc,nlp):
    doc=[d for d in doc if type(d)!=str]
    se=check_se(doc)
    n_sujeito=num_sujeito(doc,nlp)
    if se:
        print("Sujeito com 'se' válido")
        return get_se(doc)
    elif n_sujeito>0:
        print('classificar sujeito padrão')
        return get_sujeito(doc,n_sujeito)
    else:
        print('classificar sem sujeito')
        return get_sem_sujeito(doc)
