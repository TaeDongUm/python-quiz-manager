import json
import os
import random
from datetime import datetime
from typing import Optional

from console_io import ConsoleIO
from quiz import DEFAULT_QUIZZES, Quiz

STATE_FILE = "state.json"


class QuizGame:
    """콘솔 퀴즈 게임의 기본 화면을 관리한다."""

    def __init__(self) -> None:
        self.io = ConsoleIO()
        self.is_running = True
        self.quizzes: list[Quiz] = []
        self.best_score: Optional[int] = None
        self.pending_quiz_input: Optional[dict] = None
        self.score_history: list[dict] = []
        self.load_state()

    def display_menu(self) -> None:
        self.io.display_menu()

    def get_quiz_sequence(self, question_count: Optional[int] = None) -> list[Quiz]:
        quiz_sequence = list(self.quizzes)
        random.shuffle(quiz_sequence)
        if question_count is not None:
            return quiz_sequence[:question_count]
        return quiz_sequence

    def get_question_count(self) -> int:
        return self.io.get_int_input(
            f"몇 문제를 풀지 선택하세요 (1-{len(self.quizzes)}): ",
            1,
            len(self.quizzes),
        )

    def calculate_score(self, correct_count: int, total_questions: int, hint_count: int) -> int:
        base_score = int((correct_count / total_questions) * 100) if total_questions else 0
        return max(0, base_score - (hint_count * 10))

    def play_quiz(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print("퀴즈 풀기를 시작합니다.")
        correct_count = 0
        hint_count = 0
        question_count = self.get_question_count()
        quiz_sequence = self.get_quiz_sequence(question_count)

        for index, quiz in enumerate(quiz_sequence, start=1):
            quiz.display(index)
            if quiz.hint:
                use_hint = input("힌트를 보시겠습니까? (y/n): ").strip().lower() == "y"
                if use_hint:
                    print(f"힌트: {quiz.hint}")
                    hint_count += 1
            else:
                print("이 문제에는 힌트가 없습니다.")
            user_answer = self.io.get_int_input("정답 입력 (1-4): ", 1, 4)
            if self.show_answer_result(quiz, user_answer):
                correct_count += 1

        score = self.calculate_score(correct_count, len(quiz_sequence), hint_count)
        if self.best_score is None or score > self.best_score:
            self.best_score = score
        self.record_score_history(score, len(quiz_sequence))
        self.save_state()
        print(f"\n총 {len(quiz_sequence)}문제 중 {correct_count}문제를 맞혔습니다.")
        print(f"최종 점수: {score}점")

    def show_answer_result(self, quiz: Quiz, user_answer: int) -> bool:
        if quiz.is_correct(user_answer):
            print("정답입니다!")
            return True

        print(f"오답입니다. 정답은 {quiz.answer}번입니다.")
        return False

    def add_quiz(self) -> None:
        print("새로운 퀴즈를 입력합니다.")
        question = self.io.get_non_empty_text_input("문제를 입력하세요: ")
        choices: list[str] = []

        for index in range(1, 5):
            choice = self.io.get_non_empty_text_input(f"선택지 {index}: ")
            choices.append(choice)

        answer = self.io.get_int_input("정답 번호 (1-4): ", 1, 4)
        hint = self.io.get_non_empty_text_input("힌트(선택): ")

        self.pending_quiz_input = {
            "question": question,
            "choices": choices,
            "answer": answer,
            "hint": hint,
        }

        new_quiz = Quiz(
            question=question,
            choices=choices,
            answer=answer,
            hint=hint,
        )
        self.quizzes.append(new_quiz)
        self.save_state()
        print(f"문제, 선택지, 정답 번호 입력이 완료되었습니다. (총 {len(self.quizzes)}개)")

    def show_quizzes(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"등록된 퀴즈는 총 {len(self.quizzes)}개입니다.")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

    def delete_quiz(self, quiz_index: int) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        if quiz_index < 1 or quiz_index > len(self.quizzes):
            print("잘못된 번호입니다.")
            return

        deleted_quiz = self.quizzes.pop(quiz_index - 1)
        self.save_state()
        print(f"'{deleted_quiz.question}' 문제가 삭제되었습니다.")

    def show_score(self) -> None:
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
            return

        print(f"현재 최고 점수는 {self.best_score}점입니다.")

    def delete_quiz_menu(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        self.show_quizzes()
        quiz_index = self.io.get_int_input("삭제할 퀴즈 번호를 입력하세요: ", 1, len(self.quizzes))
        self.delete_quiz(quiz_index)

    def record_score_history(self, score: int, question_count: int) -> None:
        self.score_history.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "score": score,
                "question_count": question_count,
            }
        )

    def show_score_history(self) -> None:
        if not self.score_history:
            print("아직 게임 기록이 없습니다.")
            return

        print("게임 기록")
        for entry in self.score_history:
            print(
                f"{entry['timestamp']} | 점수: {entry['score']}점 | 푼 문제 수: {entry['question_count']}"
            )

    def exit_game(self) -> None:
        print("프로그램을 종료합니다.")
        self.is_running = False

    def load_state(self) -> None:
        if not os.path.exists(STATE_FILE):
            self.quizzes = list(DEFAULT_QUIZZES)
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if content == "":
                self.quizzes = list(DEFAULT_QUIZZES)
                self.best_score = None
                return

            data = json.loads(content)
            quizzes_data = data.get("quizzes", [])
            if not quizzes_data:
                self.quizzes = list(DEFAULT_QUIZZES)
                self.best_score = data.get("best_score", None)
                return

            self.quizzes = [Quiz.from_dict(q) for q in quizzes_data]
            self.best_score = data.get("best_score", None)
            self.score_history = data.get("score_history", [])
        except json.JSONDecodeError:
            print("ERROR: state.json 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None
        except OSError as e:
            print(f"ERROR: 파일을 읽는 중 오류가 발생했습니다: {e}")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None

    def save_state(self) -> None:
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "score_history": self.score_history,
        }

        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"ERROR: 파일을 저장하는 중 오류가 발생했습니다: {e}")

    def run(self) -> None:
        actions = {
            "1": self.play_quiz,
            "2": self.add_quiz,
            "3": self.show_quizzes,
            "4": self.show_score,
            "5": self.delete_quiz_menu,
            "6": self.show_score_history,
            "7": self.exit_game,
        }

        try:
            while self.is_running:
                self.display_menu()
                choice = self.io.get_menu_choice()

                action = actions.get(choice)
                if action:
                    action()
        except KeyboardInterrupt:
            self.io.safe_exit("사용자에 의해 프로그램이 중단되었습니다.")
        except EOFError:
            self.io.safe_exit("입력 스트림이 종료되었습니다.")