import spacy

def get_num_verbs(frase,nlp):
    doc = nlp(frase)
    verb_count=0
    lemma_list=["canto", "casa", "dúvida", "respeito", "como", "desejo", "morro", "fala", "ajuda"]
    for t in doc:
        if t.pos_=="VERB" or (t.pos_=="AUX" and t.dep_ in ("cop", "cop:pass", "aux:pass")) or (t.pos_ in ("NOUN") and t.dep_ in ("ccomp", "xcomp", "ROOT", "appos","conj", "amod") and t.lemma_ in lemma_list):
        # if t.pos_=="VERB" or (t.pos_=="ADJ" and t.dep_ == "conj") or (t.pos_=="ADJ" and t.dep_ in ("ccomp", "xcomp", "ROOT")) or (t.pos_ in ("NOUN") and t.dep_ in ("ccomp", "xcomp", "ROOT", "appos","conj") and t.lemma_ in lemma_list):
            verb_count+=1
    return verb_count
