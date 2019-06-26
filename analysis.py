from __future__ import print_function, division
import os
import parsing

class Document(object):
    def __init__(self, filename, stopwords="./stopwords/stopwords_francais.txt"):
            """<filename> : path of the corpus"""
            if filename.endswith(".odt"):
                new_filename = filename.replace(".odt","_.txt")
                parsing.write_txt(filename, new_filename)
                filename = new_filename
            print("Reading into corpus file " + filename)
            self.text = parsing.get_text(filename)
            print("bu1",self.text.count("qu'elle"))
            self.stats = get_statistics(self.text)
            self.syllables = self.stats[2]
            self.sentences = self.stats[0]
            self.fk = fk(self.stats)
            self.ptext = parsing.remove_punctuation(self.text)
            print("bu2",self.ptext.count("qu'elle"))
            print("     Parsing words...")
            self.all_words = parsing.get_all_words(self.ptext)
            self.words = parsing.get_words_count(self.all_words)
            self.chars = len(self.ptext.replace(" ",""))
            text = parsing.get_text(stopwords)
            text = parsing.purify(text)
            stopwords = parsing.get_all_words(text)
            stopwords.append("a")
            self.stopwords = stopwords

    def show_dominant_words(self, n=20, count_treshold=1):
        """Show <n> dominant words."""
        candidates = [w for w in self.words if not w in self.stopwords]
        candidates.sort(key = lambda x:self.words[x], reverse=True)
        i = 0
        for word in candidates:
            if not word:
                continue
            count = self.words[word]
            if count > count_treshold:
                print(str(i) + ") " +word + " : " + str(count))
                i += 1
                if i == n:
                    break

    def show_word(self, word):
        if word in self.words:
            print(word + " : " + str(self.words[word]) + " counts")
        else:
            print("Nothing found for '" + word + "'")


def get_statistics(s):
    sentences = parsing.get_all_sentences(s)
    words = parsing.get_all_words(s)
    syllables = 0
    for w in words:
        syllables += parsing.syllable_count(w)
    return len(sentences), len(words), syllables

def fk(stats):
    sentences, words, syllables = stats
    return 206.835 - 1.015*words/sentences - 84.6*syllables/words

def text_statistics(fn):
    text = parsing.get_text(fn)
    stats = get_statistics(text)
    sentences = stats[0]
    words = stats[1]
    syllables = stats[2]
    return sentences, words, syllables

def summary_text(fn):
    doc = Document(fn)
    doc.show_dominant_words(n=40)
    print("Characters:",doc.chars)
    print("Syllables:",doc.syllables)
    print("Sentences:",doc.sentences)
    print("Words",len(doc.all_words))
    print("Different words",len(doc.words))
    print("Ratio different words/total words:",
                float(len(doc.words))/len(doc.all_words))
    print("F-K score:", doc.fk)
    print()

def summary_folder(folder):
    N = 0
    c = 0
    docs = 0
    for fn in os.listdir(folder):
        if fn.endswith(".odt") or fn.endswith(".txt"):
            fullpath = os.path.join(folder,fn)
            summary_text(fullpath)
            docs += 1





if __name__ == '__main__':
    summary_folder("./")

#TODO: richesse du vocabulaire: parametre d'etalement de la loi de puissance des mots
#TODO: regarder plutot moyenne et variance de word/sentence et syllabe/words collecte sur chaque individu plutot qu'en moyenne
#TODO: autre mesure

"""
The so-called "Menzerath law" is well known by German linguists dealing with quantitative linguistics, while
it is almost ignored by French linguists. It says that in any linguistic construct, the more constituents a given unit is made
of, the smaller they are. Here this "law" is confronted with observations made on a corpus of texts taken from the
newspaper Le Monde. It appears that globally articles (texts) that have long sentences use longer words than articles
having shorter sentences - but inside most of these articles, long sentences use shorter words than short sentences.
Similar measures made with an intermediate level between "sentence" and "word", or made on phonetic transcriptions of
the texts, do not change the conclusions. This shows that a research on the Menzerath law should always provide precise
information on the exact nature of the units that are being counted and the way they have been obtained.
"""
