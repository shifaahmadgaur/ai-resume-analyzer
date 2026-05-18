from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume(resume_text, job_description):
    try:
        docs = [resume_text, job_description]

        tfidf = TfidfVectorizer(stop_words='english')
        matrix = tfidf.fit_transform(docs)

        score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]

        return round(score * 100, 2)

    except:
        return 0
