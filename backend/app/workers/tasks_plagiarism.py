from ..services.plagiarism.similarity_engine import compute_similarity_report


def run_plagiarism(document: dict):
    return compute_similarity_report(document)
