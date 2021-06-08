text =["london paris london", "paris paris london"]
cv = CountVectorizer()

count_matrix=cv.fit_transform(text)

# //print count matrix.toarray()
similarity_scores = cosine_similarity(count_matrix)

print similarity_scores