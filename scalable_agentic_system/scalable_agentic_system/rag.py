class RAGTool:
    # Small local RAG-style documentation search.
    # Production can use a vector database or hybrid search engine.

    def __init__(self):
        self.documents = [
            {
                "title": "Create Invoice API",
                "text": "Creates an invoice. Required parameter: amount. Currency defaults to USD."
            },
            {
                "title": "Sales Reporting API",
                "text": "Returns sales volume for a start_date and end_date."
            },
            {
                "title": "Dispute API",
                "text": "Checks dispute information using user_id."
            },
        ]

    def search(self, query: str, limit: int = 3):
        words = set(query.lower().split())
        results = []
        for doc in self.documents:
            text = f"{doc['title']} {doc['text']}".lower()
            score = sum(1 for word in words if word in text)
            if score:
                results.append((score, doc))
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in results[:limit]]
