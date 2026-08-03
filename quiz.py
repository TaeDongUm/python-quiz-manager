from dataclasses import dataclass, field


@dataclass
class Quiz:
    """퀴즈 한 문제를 나타내는 도메인 객체."""

    question: str
    choices: list[str]
    answer: int  # 1~4

    def display(self, index: int) -> None:
        print(f"\n[문제 {index}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def is_correct(self, user_answer: int) -> bool:
        return self.answer == user_answer

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @staticmethod
    def from_dict(data: dict) -> "Quiz":
        return Quiz(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
        )


DEFAULT_QUIZZES: list[Quiz] = [
    Quiz(
        question="Python에서 리스트(list)와 튜플(tuple)의 가장 큰 차이는?",
        choices=["리스트는 숫자만 저장", "튜플은 변경 불가능(immutable)", "리스트는 정렬이 안 됨", "튜플은 중복을 허용하지 않음"],
        answer=2,
    ),
    Quiz(
        question="Python에서 딕셔너리(dict)의 키(key)로 사용할 수 없는 타입은?",
        choices=["str", "int", "tuple", "list"],
        answer=4,
    ),
    Quiz(
        question="다음 중 Python의 논리 연산자가 아닌 것은?",
        choices=["and", "or", "not", "xor"],
        answer=4,
    ),
    Quiz(
        question="Python에서 None과 0을 == 연산자로 비교하면?",
        choices=["True", "False", "오류 발생", "None"],
        answer=2,
    ),
    Quiz(
        question="Python 클래스의 인스턴스 메서드 첫 번째 매개변수 이름으로 관례적으로 사용되는 것은?",
        choices=["this", "me", "self", "cls"],
        answer=3,
    ),
    Quiz(
        question="Python에서 range(5)가 생성하는 숫자 개수는?",
        choices=["4개", "5개", "6개", "0개"],
        answer=2,
    ),
]
