
TOTAL_MARKS = 720
BIO_QUESTIONS = 90
PHYSICS_QUESTIONS = 45
CHEMISTRY_QUESTIONS = 45

def calculate_score(correct, wrong):
    return (correct * 4) - wrong

def report(correct, wrong):
    score = calculate_score(correct, wrong)
    accuracy = (correct / max(1, correct + wrong)) * 100
    return {
        "score": score,
        "out_of": TOTAL_MARKS,
        "accuracy": round(accuracy, 2),
    }
