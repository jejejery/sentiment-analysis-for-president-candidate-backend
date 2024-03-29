import stanza
import json

'''
@ IMPORTANT!
Please limit the counter beause the data is too much >.<
'''

class Parser:
    def __init__(self,arr_of_tweet):
        try:
            self.nlp = stanza.Pipeline('id')
        except Exception as e:
            stanza.download('id')
            self.nlp = stanza.Pipeline('id')
        
        array = []
        skip_first = True
        counter = 0
        for k in arr_of_tweet:
                tupel = self.get_tuple(k[1])
                if(tupel != []): array.append(tupel)
                counter += 1
                if(counter % 50 == 0):
                  print(f"process {counter} from {len(arr_of_tweet)} data")
                if(counter == 100): #limit up to 50 data only
                  break
              

        self.tuples = array

    @staticmethod
    def clear_arr(unclean_arr):
        arr = []
        for k in unclean_arr: 
            arr.append(k[1])
        return arr

    def stanza_word_to_list(self,word):
        my_list = {"lemma":word.lemma,"upos":word.upos,"xpos":word.xpos,"head":word.head,"deprel":word.deprel}
        return my_list

    def get_tuple(self,text):
      doc = self.nlp(text)
      mytuple = []

      try:
          doc.sentences[0]
          for i in doc.sentences[0].words:
            opinion=""
            target=""
            if i.upos =='NOUN':
              target = i.text
              meta_target = self.stanza_word_to_list(i)

              for j in doc.sentences[0].words:
                if j.id == i.head and j.upos =='NOUN':
                  target = j.text+" "+target

              for j in doc.sentences[0].words:
                if j.upos =="ADJ" and int(j.head) == int(i.id):
                  opinion = j.lemma
                  meta_opinion = self.stanza_word_to_list(j)

                  for k in doc.sentences[0].words:
                    if k.head == j.id:
                      if k.id < j.id :
                        opinion = k.lemma+" "+opinion
                      else:
                        opinion = opinion+" "+k.lemma
              if opinion !="":
                mytuple = {"kalimat":text,"aspect":target.strip(),"opinion":opinion.strip(),"true_tuple":'',"sentiment":'',"meta_aspect":meta_target,"meta_opinion":meta_opinion}
          return mytuple
      except Exception as e:
        return []



    
    def debug(self):
        for k in self.tuples:
             print(k)