"""
Esse arquivo é acionado quando o chama_classificacoes.py e encontra algum tipo de "se".
Abarca vários casos: índice de indeterminação do sujeito, partícula apassivadora e reflexivo.
Poderia ser o caso de ter um arquivo (ou função) para cada um desses casos?
"""
import spacy


def get_se(texto_doc):

    # Listas para verificar a presença de uma função sintática específica
    se = [t for t in texto_doc if t.text == "se"]
    suj = [t for t in texto_doc if "nsubj" in t.dep_ if t.text != "se"]
    obj = [t.text for t in texto_doc if "obj" in t.dep_ if t.text != "se"]
    case = [
        t.text for t in texto_doc for o in obj if "case" in t.dep_ if t.head.text == o
    ]
    xcomp = [
        t.text
        for t in texto_doc
        if "xcomp" in t.dep_
        if t.pos_ == "NOUN" or t.pos_ == "ADJ"
    ]
    heads = len(suj) + len(obj) + len(xcomp)

    if se:
        for s in se:
            if obj:
                if case:
                    if not suj:
                        # Exemplo: "Precisa-se de trabalhadores."
                        se_obj_ind = f"se é o índice de indeterminação do sujeito do verbo {s.head.text} ...indet-obj-ind"
                        return se_obj_ind
                else:
                    # Exemplo: "Vende-se uma casa."
                    se_obj = f"se é a partícula apassivadora e {obj} é o sujeito do verbo {s.head.text} ...obj"
                    return se_obj

            if suj:
                if "nsubj" in s.dep_:
                    for t in suj:
                        # Exemplo: "Compra-se uma casa."
                        se_suj = f"se é a partícula apassivadora e {t.text} é o sujeito do verbo {t.head.text} ...suj"
                        return se_suj

                else:
                    if "PRON" in s.pos_:
                        docl = list(texto_doc)
                        for t in docl:
                            if t.text == "se":
                                if t.dep_ != "mark":
                                    for x in docl:
                                        if x.dep_ == "nsubj":
                                            if x.text != "se":
                                                if docl.index(t) < docl.index(x):
                                                    # Exemplo: "Aqui se compra algo."
                                                    se_mark2 = f"se é a partícula apassivadora e {x.text} é o sujeito do verbo {s.head.text} ...suj-2"
                                                    return se_mark2

                                                else:
                                                    # Exemplo: "O menino se viu no espelho."
                                                    se_refl = f"{suj} é o sujeito do verbo {s.head.text} e <se> é o objeto do verbo {s.head.text} ...refl"
                                                    return se_refl

            if xcomp:
                # Exemplo: "Escrevia-se um livro."
                se_xcomp = f"se é a partícula apassivadora e {xcomp} é o sujeito do verbo {s.head.text} ...xcomp"
                return se_xcomp

            if heads == 0:
                # Exemplo: "Vive-se bem no Rio de Janeiro."
                se_indet = f"se é o índice de indeterminação do sujeito do verbo {s.head.text} ...indet"
                return se_indet

