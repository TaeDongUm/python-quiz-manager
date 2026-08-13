import json
import os
from typing import Optional

from quiz import DEFAULT_QUIZZES, Quiz


class JsonStateStore:
    """state.json 기반의 게임 상태 저장소."""

    def __init__(self, state_file: str = "state.json") -> None:
        self.state_file = state_file

    def load(self) -> tuple[list[Quiz], Optional[int], list[dict]]:
        if not os.path.exists(self.state_file):
            return list(DEFAULT_QUIZZES), None, []

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if content == "":
                return list(DEFAULT_QUIZZES), None, []

            data = json.loads(content)
            quizzes_data = data.get("quizzes", [])
            best_score = data.get("best_score", None)
            score_history = data.get("score_history", [])

            if not quizzes_data:
                return list(DEFAULT_QUIZZES), best_score, score_history

            quizzes = [Quiz.from_dict(q) for q in quizzes_data]
            return quizzes, best_score, score_history
        except json.JSONDecodeError:
            print("ERROR: state.json 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            return list(DEFAULT_QUIZZES), None, []
        except OSError as e:
            print(f"ERROR: 파일을 읽는 중 오류가 발생했습니다: {e}")
            return list(DEFAULT_QUIZZES), None, []

    def save(self, quizzes: list[Quiz], best_score: Optional[int], score_history: list[dict]) -> bool:
        data = {
            "quizzes": [quiz.to_dict() for quiz in quizzes],
            "best_score": best_score,
            "score_history": score_history,
        }

        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except OSError as e:
            print(f"ERROR: 파일을 저장하는 중 오류가 발생했습니다: {e}")
            return False