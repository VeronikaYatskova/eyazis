import re
import svgling
import pymorphy2
import spacy
from tinydb import TinyDB, Query
from typing import List, Dict
from langdetect import detect_langs
from repository import Neo4JStorage, LetterEntity, WordEntity, LanguageEntity

morph = pymorphy2.MorphAnalyzer()
db = TinyDB('./db.json')
check = Query()

nlp_ru = spacy.load("ru_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")

def get_words(lines, type=True, lang = 'ru'):
    words = []
    if type and lang == 'ru':
        lines : list
        for line in lines:
            line1 = re.findall(r'[А-яЁё][А-яё\-]*', line)
            for word in line1:
                words.append(word.lower())

    elif not type and lang == 'ru':
        lines : str
        line1 = re.findall(r'[А-яЁё][а-яё\-]*', lines)
        for word in line1:
            words.append(word.lower())

    elif not type and lang == 'en':
        lines : str
        words_en = []
        line1 = re.findall(r'(\|\||&&|!|[А-яЁё][а-яё\-]*)', lines)
        line2 = re.findall(r'[A-z0-9][A-z0-9\-]*', lines)
        for word in line1:
            if word == ('больше' or 'меньше' or 'позже' or 'раньше'):
                words_en.append(word)
            elif word == 'поиск':
                words_en.extend(list(line1))
                words_en.remove(word)
                words.append(word.lower())
                return words, words_en
            else:
                words.append(word.lower())
        for word in line2:
            words_en.append(word)
        return words, words_en

    return words

def parse_words(words, type = True): #words: dict or list
    parsed_words = []
    if type:
        words : dict
        for word in words.keys():
            if db.search(check.word == word):
                db.update({'amount': words[word]}, check.word == word)
                parsed_words.append(db.search(check.word == word)[0])
            else: 
                p_word = morph.parse(word)[0].tag
                parsed_words.append({'word': word, 'amount': words[word],'POS': p_word.POS, 'animacy': p_word.animacy, 'case': p_word.case, 'gender': p_word.gender, 'mood': p_word.mood,
                                'number': p_word.number, 'person': p_word.person, 'tense': p_word.tense, 'transitivity': p_word.transitivity, 'voice': p_word.voice})
    
    else:
        words : list
        for word in words:
            if db.search(check.word == word):
                parsed_words.append(db.search(check.word == word)[0])
            else:
                p_word = morph.parse(word)[0].tag
                parsed_words.append({'word': word, 'amount': 1,'POS': p_word.POS, 'animacy': p_word.animacy, 'case': p_word.case, 'gender': p_word.gender, 'mood': p_word.mood,
                                'number': p_word.number, 'person': p_word.person, 'tense': p_word.tense, 'transitivity': p_word.transitivity, 'voice': p_word.voice})
    return parsed_words

def to_normal(words: List):
    normal_words = []
    for word in words:
        n_word = morph.parse(word)[0].normal_form
        normal_words.append(n_word)

    return normal_words
    
def tree2svg(t):
    img = svgling.draw_tree(t)
    svg_data = img.get_svg()
    return svg_data

def detect_language_by_neuro(text: str):
    lang_arr = detect_langs(text)
    lang_arr = [str(it) for it in lang_arr]

    check_arr = [0, 0, 0]
    for it in lang_arr:
        lang, numb = it.split(':')
        if lang == 'ru':
            check_arr[0] += float(numb)
        elif lang == 'en':
            check_arr[1] += float(numb)
        else:
            check_arr[2] += float(numb)

    check_arr = [float('{:.2f}'.format((it*100))) for it in check_arr]
    
    return f"Данный текст является на {check_arr[0]}% является русскоязычным, на {check_arr[1]}% является англоязычным и на {check_arr[2]}% состоит из других языков" 

def detect_language_by_alphabet(text: str):
    neo4j = Neo4JStorage("bolt://localhost:7687", "neo4j", "password")

    english = neo4j.getLanguageByName("english")
    if english is None:
        english = LanguageEntity("english", None, [], [])
    russian = neo4j.getLanguageByName("russian")
    if russian is None:
        russian = LanguageEntity("russian", None, [], [])

    englishAlphabet: Dict[str, int] = dict()
    russianAlphabet: Dict[str, int] = dict()

    normilizedLine = ''.join(list(re.findall(r'[А-яЁёA-z][А-яёA-z\-]*', text.lower())))

    for char in normilizedLine:
      if russian.containsLetter(LetterEntity(char, 0)) is True:
        russianAlphabet.update({char : (russianAlphabet.get(char) or 0) + 1 })
      elif english.containsLetter(LetterEntity(char, 0)) is True:
        englishAlphabet.update({char: (englishAlphabet.get(char) or 0) + 1 })

    amountRussionLettersOccurences = 0
    amountEnglishLettersOccurences = 0

    print(russianAlphabet)
    print(englishAlphabet)

    for letterOccurences in englishAlphabet.values():
        amountEnglishLettersOccurences += letterOccurences    

    for letterOccurences in russianAlphabet.values():
        amountRussionLettersOccurences += letterOccurences

    countLetters = len(''.join(list(re.findall(r'[А-яЁёA-z][А-яёA-z\-]*', text.lower()))))

    percentRussian = ((amountRussionLettersOccurences) / (countLetters or 1)) * 100
    percentEnglish = ((amountEnglishLettersOccurences) / (countLetters or 1)) * 100
    percentOtherLanguages = (((countLetters - amountRussionLettersOccurences - amountEnglishLettersOccurences)) / countLetters) * 100
    return f"Данный текст является на {percentRussian}% является русскоязычным, на {percentEnglish}% является англоязычным и на {percentOtherLanguages}% состоит из других языков" 

def learn_language_by_alphabet(line: str, languageName: str):
  neo4j = Neo4JStorage("bolt://localhost:7687", "neo4j", "password")
  normilizedLine = ''.join(list(re.findall(r'[А-яЁёA-z][А-яёA-z\-]*', line.lower())))
  language = neo4j.getLanguageByName(languageName.lower())
  if language is None:
    language = LanguageEntity(languageName.lower(), None, [], [])
  for char in normilizedLine:
    language.addLetter(LetterEntity(char, 0))
  neo4j.saveLanguageNode(language)

def learn_language_by_words(line: str, languageName: str):
  neo4j = Neo4JStorage("bolt://localhost:7687", "neo4j", "password")
  language = neo4j.getLanguageByName(languageName)
  if language is None:
    language = LanguageEntity(languageName.lower(), None, [], [])
  for word in re.findall(r'(\|\||&&|!|[А-яЁёA-z][а-яёA-z\-]*)', line):
    [normilizedWord] = to_normal([word])
    language.addWord(WordEntity(normilizedWord, 0))
  neo4j.saveLanguageNode(language)

def detect_language_by_words(text: str):
    neo4j = Neo4JStorage("bolt://localhost:7687", "neo4j", "password")

    english = neo4j.getLanguageByName("english")
    if english is None:
        english = LanguageEntity("english", None, [], [])
    russian = neo4j.getLanguageByName("russian")
    if russian is None:
        russian = LanguageEntity("russian", None, [], [])


    englishWords: Dict[str, int] = dict()
    russianWords: Dict[str, int] = dict()

    for char in re.findall(r'[А-яЁёA-z0-9][А-яёA-z0-9\-]*', text.lower()):
      [normilizedWord] = to_normal([char])
      if russian.containsWord(WordEntity(normilizedWord, 0, None)) is True:
        russianWords.update({normilizedWord : (russianWords.get(normilizedWord) or 0) + 1 })
      elif english.containsWord(WordEntity(normilizedWord, 0)) is True:
        englishWords.update({normilizedWord: (englishWords.get(normilizedWord) or 0) + 1 })
        
    amountRussionLettersOccurences = 0
    amountEnglishLettersOccurences = 0


    for letterOccurences in englishWords.values():
        amountEnglishLettersOccurences += letterOccurences    

    for letterOccurences in russianWords.values():
        amountRussionLettersOccurences += letterOccurences

    countWords = len(re.findall(r'[А-яЁёA-z0-9][А-яёA-z0-9\-]*', text.lower()))
    percentRussian = ((amountRussionLettersOccurences) / (countWords or 1)) * 100
    percentEnglish = ((amountEnglishLettersOccurences) / (countWords or 1)) * 100
    percentOtherLanguages = (((countWords - amountRussionLettersOccurences - amountEnglishLettersOccurences)) / (countWords or 1)) * 100
    return f"Данный текст является на {percentRussian}% является русскоязычным, на {percentEnglish}% является англоязычным и на {percentOtherLanguages}% состоит из других языков" 

def find_key_words(text: str):
    rake_nltk_var = Rake()
    rake_nltk_var.extract_keywords_from_text(text)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    return ', '.join(keyword_extracted[0:6])
