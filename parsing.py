from __future__ import print_function, division
import re
import codecs

removed_chars = "1234567890^`()&%?!+#[]/—–~«»"
removed_chars2=['\n', '\r', '¿', "/", "\\", '', '*', "_", "<", ">", "=","\t",
                '"', "--"]
replaced_chars = [("â","a"),("ô","o"),("ä","a"),("ö","o"),("ü","u"),("ë","e"),
                  ("è","e"),("é","e"),("à","a"),("ç","c"),("ê","e"),("î","i"),
                  ("ù","u"),
                  ("Ã©","e"),("Ãª","e"),("Ã¨","e"),("ã´","o"),("ã©","e"),
                  ("ã¨","e"),("ã","e"),("åu","oe"),("ã","a"),("aª","e"),
                  ("a\x80\x99","'"),("a\xa0","a"),("a®","i"),("œ","oe"),
                  ("a\x80\x93","-"),("å\x93","oe"),("a¹","u"),("a\x80","a")]
purified_punctuation = ".,'-;:"
vowels = "aeiouy"

def remove_chars(s):
    s = s.replace("\n","")
    for c in removed_chars:
        s = s.replace(c,"")
    for c in removed_chars2:
        s = s.replace(c,"")
    return s

def replace_chars(s):
    for c1,c2 in replaced_chars:
        s = s.replace(c1,c2)
    return s

def purify_punctuation(s):
    s = re.sub(' +', ' ', s) #remove multiple spaces
    s = s.strip()
    for c in purified_punctuation:
        s = s.replace(" "+c+" ",c+" ")
    return s

def purify(s):
    # s = bytes(s,"utf-8").decode('utf-8')
    s = s.lower()
    s = purify_punctuation(s)
    s = replace_chars(s)
    s = remove_chars(s)
    #
    s = replace_chars(s)
    s = purify_punctuation(s)
    s = remove_chars(s)
    return s

def remove_punctuation(s):
    for c in purified_punctuation:
        s = s.replace(c," ")
    return s

def syllable_count(word):
    word = word.lower()
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

def get_words_count(all_words):
    words = {}
    for w in all_words:
        if w in words:
            words[w] += 1
        else:
            words[w] = 0
    return words

def get_all_words(text):
    return text.split(" ")

# def get_all_sentences(text): #TODO: tester: virgule aussi!
#     return text.split(".")

# def get_all_words(text):
#     words = text.split(" ")
#     while "" in words:
#         words.remove("")
#     return words

def get_all_sentences(text, length=2): #TODO: tester: virgule aussi!
    sentences = text.split(".")
    sentences = [s for s in sentences if len(s) >= length]
    return sentences

def get_text(fn):
    with open(fn,"r",encoding="latin-1") as f:
        lines1 = f.readlines()
    text= ""
    for line in lines1:
        text += line+" "
    text = purify(text)
    return text

def write_latex(src, target, title=""):
    fs = open(src, "r")
    ft = open(target, "w")
    ft.write("\\title{"+title+"}\n\date{}\n\\begin{document}\n\maketitle")
    for line in fs.readlines():
        line = line.replace("\n", "\emph{}\par\n")
        ft.write(line)
    ft.write("\n\end{document}")
    fs.close()
    ft.close()

def write_txt(src, target):
    import odt2txt
    out_utf8 = odt2txt.get_bytes(src)
    f = open(target,"wb")
    f.write(out_utf8)
    f.close()

def convert_file(sourceFileName, targetFileName):
    BLOCKSIZE = 1048576 # or some other, desired size in bytes
    with codecs.open(sourceFileName, "r", "your-source-encoding") as sourceFile:
        with codecs.open(targetFileName, "w", "utf-8") as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)
