import torch
from sentence_transformers import SentenceTransformer, util

# model = SentenceTransformer("Sakil/sentence_similarity_semantic_search")

def similar_lines(cos_sim, text):
    threshold_truth = 0.6
    _, indices = torch.topk(cos_sim, k=3)
    
    lines = []
    for idx in indices:
        lines.append(text[idx])
    
    val = torch.max(cos_sim[0])
    
    labels = ["Truth", "Not enough info"]

    if (val > threshold_truth):
        return lines, labels[0] 

    else:
        return lines, labels[1]

def calculate_similarity(news, other_news):
    model = SentenceTransformer("Sakil/sentence_similarity_semantic_search")
    news_emb = model.encode(news)
    results = []

    for i in range(len(other_news)):
        sentences = other_news[i].split('. ')
        sentences = [sentence for sentence in sentences if len(sentence) >= 10]
        embeddings = model.encode(sentences)
        cos_sim = util.cos_sim(news_emb, embeddings)
        
        lines, label = similar_lines(cos_sim, sentences)
        results.append([lines,label])
    
    return results