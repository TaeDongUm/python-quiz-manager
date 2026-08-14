from datetime import datetime
from typing import Optional


class ScoreManager:
    """점수 정책과 기록을 관리한다."""

    def __init__(self, best_score: Optional[int] = None, score_history: list[dict] = None) -> None:
        self.best_score = best_score
        self.score_history = score_history if score_history is not None else []

    def calculate_score(self, correct_count: int, total_questions: int, hint_count: int) -> int:
        base_score = int((correct_count / total_questions) * 100) if total_questions else 0
        return max(0, base_score - (hint_count * 10))

    def update_best_score(self, new_score: int) -> None:
        if self.best_score is None or new_score > self.best_score:
            self.best_score = new_score

    def record_history(self, score: int, question_count: int) -> None:
        self.score_history.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "score": score,
                "question_count": question_count,
            }
        )

    def get_best_score(self) -> Optional[int]:
        return self.best_score

    def get_score_history(self) -> list[dict]:
        return self.score_history
