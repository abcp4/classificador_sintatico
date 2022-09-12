frase = "vende-se uma casa."

fs = frase.split()
for f in fs:
    if "-se" in f:
        frase = frase.replace("-se", " se")
        print("s")
print(frase)