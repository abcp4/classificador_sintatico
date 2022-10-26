"""
Esse arquivo se aplica somente quando o chama_classificacoes.py detecta um sujeito na oração.
"""


def get_sujeito(texto_doc,n_sujeito):
    sujeito = [t for t in texto_doc if t.dep_ in ("nsubj", "nsubj:pass")]
    sc = []
    if (
        n_sujeito > 1
    ):  # O Spacy está classificando alguns sujeitos compostos marcando 'nsubj' para cada núcleo
        for s in sujeito:
            sct = list(s.subtree)
            sc.append(sct)
        # Exemplo: "O menino e a menina saíram cedo"
        sujeito_composto = f"{sc} formam o sujeito composto de {s.head.text}"  # Precisa formatar melhor a saída
        return sujeito_composto
    else:

        cc = [
            c
            for c in texto_doc
            if c.dep_ == "conj"
            for s in texto_doc
            if s.dep_ == "nsubj"
            for x in texto_doc
            if x.head.text == s.text
            if c.head.text == s.text or (c.head.text == x.text) # Para "O pai do menino(nmod) e a menina(menino) são parentes."
        ]  # esse é o caso tradicional da classificação do Spacy em sujeito composto (um 'nsubj' e um núcleo ligado a ele por 'cc', conjunção)
        if cc:
            ss = []
            # cc = []
            for s in sujeito:
                sst = list(s.subtree)
                ss.append(sst)
            # Exemplo: "O menino e a menina chegaram cedo"
            sujeito_composto = f"{ss} formam o sujeito composto de {s.head.text} #cc"
            return sujeito_composto

        else:
            ss = []
            for s in sujeito:
                if s.text == "que":
                    # Exemplo: "que chegou ontem." Spacy está atribuindo nsubj a "que".
                    sujeito_simples_que = (
                        f"o sujeito de {s.head.text} é o elemento relacionado a <que>"
                    )
                    return sujeito_simples_que
                else:
                    sst = list(s.subtree)
                    ss.append(sst)
                # Exemplo: "O menino chegou cedo."
                sujeito_simples = f"{ss} é o sujeito simples de {s.head} e {s.text} é o núcleo do sujeito."
                return sujeito_simples
