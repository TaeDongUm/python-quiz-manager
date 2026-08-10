import random
from typing import Optional

from quiz import Quiz


class QuizRepository:
    """퀴즈 목록을 관리하고 조작한다."""

    def __init__(self, quizzes: list[Quiz] | None = None) -> None:
        self.quizzes = quizzes if quizzes is not None else []

    def add(self, quiz: Quiz) -> None:
        self.quizzes.append(quiz)

    def delete(self, quiz_index: int) -> Optional[Quiz]:
        if quiz_index < 1 or quiz_index > len(self.quizzes):
            return None
        return self.quizzes.pop(quiz_index - 1)

    def get_all(self) -> list[Quiz]:
        return self.quizzes

    def get_count(self) -> int:
        return len(self.quizzes)

    def get_sequence(self, question_count: Optional[int] = None) -> list[Quiz]:
        quiz_sequence = list(self.quizzes)
        random.shuffle(quiz_sequence)
        if question_count is not None:
            return quiz_sequence[:question_count]
        return quiz_sequence

    def is_empty(self) -> bool:
        return len(self.quizzes) == 0
