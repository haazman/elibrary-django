import fitz  # PyMuPDF
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re
import string

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def analyze_book_keywords(book, max_keywords=10):
    """
    Analyze book content and extract relevant keywords
    """
    try:
        pdf_path = book.pdf_file.path
        doc = fitz.open(pdf_path)
        
        text_content = ""
        max_pages = min(10, len(doc))
        for page_num in range(max_pages):
            page = doc[page_num]
            page_text = page.get_text()
            if page_text.strip():
                text_content += page_text + " "
        
        doc.close()
        
        if not text_content.strip():
            return ["Tidak ada teks ditemukan dalam PDF"]
        

        text_content = preprocess_text(text_content)
        
        if len(text_content.split()) < 10: 
            return ["Teks terlalu pendek untuk dianalisis"]
        

        keywords = extract_keywords_tfidf(text_content, max_keywords)
        
        return keywords if keywords else ["Tidak ditemukan kata kunci yang signifikan"]
    
    except Exception as e:
        return [f"Error analisis: {str(e)}"]

def preprocess_text(text):
    """
    Clean and preprocess text for keyword extraction
    """

    text = text.lower()
    
    text = re.sub(r'[^\w\s]', ' ', text)
    
    text = ' '.join(text.split())
    
    return text

def extract_keywords_tfidf(text, max_keywords=10):
    """
    Extract keywords using TF-IDF vectorization with fallback methods
    """
    try:
        try:
            stop_words = set(stopwords.words('english'))
        except:
            stop_words = set()  
        
   
        indonesian_stopwords = {
            'dan', 'di', 'ke', 'dari', 'untuk', 'dengan', 'pada', 'dalam', 'yang', 'adalah',
            'ini', 'itu', 'atau', 'juga', 'akan', 'telah', 'sudah', 'dapat', 'bisa', 'tidak',
            'ada', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan',
            'sepuluh', 'bab', 'halaman', 'bagian', 'seperti', 'karena', 'sehingga', 'namun',
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'chapter', 'page', 'book', 'text', 'content', 'section', 'part'
        }
        stop_words.update(indonesian_stopwords)
        
        try:
            words = word_tokenize(text.lower())
        except Exception:
            words = text.lower().split()
        
        filtered_words = [
            word for word in words 
            if word not in stop_words 
            and len(word) > 3 
            and not word.isdigit()
            and word.isalpha()
            and len(word) < 20
        ]
        
        if len(filtered_words) < 5:
            return ["Teks terlalu pendek untuk analisis"]
        
        if len(filtered_words) < 20:
            from collections import Counter
            word_freq = Counter(filtered_words)
            most_common = word_freq.most_common(max_keywords)
            return [word for word, freq in most_common]
        
        processed_text = ' '.join(filtered_words)
        
        try:
            vectorizer = TfidfVectorizer(
                max_features=min(200, len(filtered_words)),
                ngram_range=(1, 1),
                min_df=1,
                max_df=1.0,
                stop_words=None
            )
            
            tfidf_matrix = vectorizer.fit_transform([processed_text])
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
        except ValueError as e:
            from collections import Counter
            word_freq = Counter(filtered_words)
            most_common = word_freq.most_common(max_keywords)
            return [word for word, freq in most_common if freq > 1]
        
        keyword_scores = list(zip(feature_names, tfidf_scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        
        significant_keywords = [
            keyword for keyword, score in keyword_scores[:max_keywords * 2] 
            if score > 0.01
        ]
        
        final_keywords = significant_keywords[:max_keywords]
        return final_keywords if final_keywords else ["Tidak ditemukan kata kunci yang signifikan"]
    
    except Exception as e:
        try:
            words = text.lower().split()
            filtered_words = [word for word in words if len(word) > 3 and word.isalpha()]
            if filtered_words:
                from collections import Counter
                word_freq = Counter(filtered_words)
                most_common = word_freq.most_common(min(max_keywords, 5))
                return [word for word, freq in most_common]
            else:
                return ["Tidak dapat menganalisis teks"]
        except:
            return [f"Error: Tidak dapat memproses teks"]
