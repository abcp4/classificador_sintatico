"""
Esse arquivo é acionado quando o chama_classificacoes.py não encontra nenhum nsubj no doc.
Abarca vários casos: sujeito oculto, oração sem sujeito e outros tipos.
Poderia ser o caso de ter um arquivo (ou função) para cada um desses casos?
"""
from .unidades import clima, meteorologicos, tempo


def get_sem_sujeito(texto_doc):

    for v in texto_doc:
        if "haver" in v.lemma_:
            # Exemplo: "Havia várias pessoas ali."
            verbo_impessoal = "Oração sem sujeito. O verbo é impessoal."
            return verbo_impessoal
        if v.lemma_ in (m for m in meteorologicos):
            # Exemplo: "choveu muito ontem."
            verbo_meteorologico = "Oração sem sujeito. O verbo é meteorológico."
            return verbo_meteorologico
        if v.lemma_ in ("fazer", "Faz", "faz", "ser", "Ser"):
            for o in texto_doc:
                if o.dep_ in ("obj", "obl", "ROOT"): # Ser e ROOT para "Serão dois longos anos".
                    if o.lemma_ in (c for c in clima):
                        # Exemplo: "Faz muito calor no Rio de Janeiro."
                        verbo_clima = "Oração sem sujeito. Expressão climática."
                        return verbo_clima
                    if o.lemma_ in (t for t in tempo):
                        # Exemplo: "Faz dois anos"
                        verbo_tempo = "Oração sem sujeito. Expressão de tempo."
                        return verbo_tempo
        if v.lemma_ in ("estar", "está"):
            for a in texto_doc:
                if a.pos_ == "ADJ":
                    if a.dep_ == "ROOT":
                        if a.lemma_ in (c for c in clima):
                            # Exemplo: "Está muito quente aqui."
                            verbo_clima = "Oração sem sujeito. Expressão climática."
                            return verbo_clima
        if "3" in str(v.morph):
            if "Plur" in str(v.morph):
                # Exemplo: "Roubaram o banco." Também "Chegaram cedo."
                indet_oculto = "Verifique se há um sujeito para esse verbo em outra parte. Se não houver, é sujeito indeterminado."
                return indet_oculto
            if "Sing" in str(v.morph):
                # Exemplo: "Chegou cedo."
                suj_oculto = "Sujeito oculto."
                return suj_oculto
        if "1" in str(v.morph) or "2" in str(v.morph):
            # Exemplo: "Cheguei cedo."
            suj_oculto = "Sujeito oculto."
            return suj_oculto
        if v.pos_ == "VERB":
            if v.dep_ == "ROOT":
                # Exemplo: "escrever." São casos de infinitivo de orações como "Quero escrever."
                suj_oculto = "Sujeito oculto."
                return suj_oculto
