import nltk
from nltk.corpus import stopwords


from .models import WordCloud


nltk.download('stopwords')
ENG_STOPWORDS = set(stopwords.words("english"))


def create_word_freq(userProfile):
   res = {}
   tracks = userProfile.tracks.all()
   # remove the stopwords and add to the collection
   for t in tracks:
       words = t.lyrics.split()
       for w in words:
           w = w.lower()
           if w not in ENG_STOPWORDS:
               res[w] = res.get(w,0) + 1
  
   wc = WordCloud(user=userProfile, words=res)
   return wc