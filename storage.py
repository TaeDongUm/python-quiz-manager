import json
import os
import shutil
from typing import Optional

from quiz import DEFAULT_QUIZZES, Quiz


class JsonStateStore:
    """state.json 기반의 게임 상태 저장소."""

    def __init__(self, state_file: str = "state.json") -> None:
        self.state_file = state_file
        self.backup_file = f"{state_file}.bak"

    def load(self) -> tuple[list[Quiz], Optional[int], list[dict]]:
        if not os.path.exists(self.state_file):
            return list(DEFAULT_QUIZZES), None, []

        try:
            data = self._load_file(self.state_file)

        except json.JSONDecodeError:
            print(
                "ERROR: state.json 파일이 손상되었습니다."
            )

            data = self._restore_backup()

            if data is None:
                print(
                    "사용 가능한 백업이 없어 기본 데이터로 초기화합니다."
                )
                return list(DEFAULT_QUIZZES), None, []

            print(
                "state.json.bak 파일에서 데이터를 복구했습니다."
            )

        except OSError as e:
            print(
                f"ERROR: 파일을 읽는 중 오류가 발생했습니다: {e}"
            )

            data = self._restore_backup()

            if data is None:
                return list(DEFAULT_QUIZZES), None, []

            print(
                "state.json.bak 파일에서 데이터를 복구했습니다."
            )

        quizzes_data = data.get("quizzes", [])
        best_score = data.get("best_score", None)
        score_history = data.get("score_history", [])

        if not quizzes_data:
            return (
                list(DEFAULT_QUIZZES),
                best_score,
                score_history,
            )

        quizzes = [
            Quiz.from_dict(q)
            for q in quizzes_data
        ]

        return quizzes, best_score, score_history

    def save(self, quizzes: list[Quiz], best_score: Optional[int], score_history: list[dict]) -> bool:
        data = {
            "quizzes": [quiz.to_dict() for quiz in quizzes],
            "best_score": best_score,
            "score_history": score_history,
        }

        try:
            self._create_backup()

            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except OSError as e:
            print(f"ERROR: 파일을 저장하는 중 오류가 발생했습니다: {e}")
            return False

    def _load_file(self, file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if content == "":
            raise json.JSONDecodeError(
                "파일 내용이 비어 있습니다.",
                content,
                0,
            )

        return json.loads(content)

    def _create_backup(self) -> bool:
        if not os.path.exists(self.state_file):
            return False

        try:
            self._load_file(self.state_file)

            shutil.copy2(
                self.state_file,
                self.backup_file,
            )   

            return True

        except (json.JSONDecodeError, OSError):
            return False
        
    def _restore_backup(self) -> Optional[dict]:
        if not os.path.exists(self.backup_file):
            return None

        try:
            data = self._load_file(self.backup_file)

            shutil.copy2(
                self.backup_file,
                self.state_file,
            )

            return data

        except (json.JSONDecodeError, OSError):
            return None
    