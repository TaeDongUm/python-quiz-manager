from typing import Optional

from console_io import ConsoleIO
from quiz import Quiz
from quiz_repository import QuizRepository
from score_manager import ScoreManager
from storage import JsonStateStore


class QuizGame:
    """콘솔 퀴즈 게임의 기본 화면을 관리한다."""

    def __init__(self) -> None:
        self.io = ConsoleIO()
        self.storage = JsonStateStore()
        self.score_manager = ScoreManager()
        self.repository = QuizRepository()
        self.is_running = True
        self.load_state()

    def display_menu(self) -> None:
        self.io.display_menu()

    def get_question_count(self) -> int:
        return self.io.get_int_input(
            f"몇 문제를 풀지 선택하세요 (1-{self.repository.get_count()}): ",
            1,
            self.repository.get_count(),
        )

    def play_quiz(self) -> None:
        if self.repository.is_empty():
            print("등록된 퀴즈가 없습니다.")
            return

        print("퀴즈 풀기를 시작합니다.")
        correct_count = 0
        hint_count = 0
        question_count = self.get_question_count()
        quiz_sequence = self.repository.get_sequence(question_count)

        for index, quiz in enumerate(quiz_sequence, start=1):
            quiz.display(index)
            if quiz.hint:
                while True:
                    use_hint = input("힌트를 보시겠습니까? (y/n): ").strip().lower()
                    if use_hint == "y":
                        print(f"힌트: {quiz.hint}")
                        hint_count += 1
                        break
                    elif use_hint == "n":
                        print(f"힌트를 사용하지 않음을 선택하셨습니다.")
                        break
                    else:
                        print(f"y 이나 n을 넣어주세요.")
            else:
                print("이 문제에는 힌트가 없습니다.")
            user_answer = self.io.get_int_input("정답 입력 (1-4): ", 1, 4)
            if self.show_answer_result(quiz, user_answer):
                correct_count += 1

        score = self.score_manager.calculate_score(correct_count, len(quiz_sequence), hint_count)
        self.score_manager.update_best_score(score)
        self.score_manager.record_history(score, len(quiz_sequence))
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

        new_quiz = Quiz(
            question=question,
            choices=choices,
            answer=answer,
            hint=hint,
        )
        self.repository.add(new_quiz)
        self.save_state()
        print(f"문제, 선택지, 정답 번호 입력이 완료되었습니다. (총 {self.repository.get_count()}개)")

    def show_quizzes(self) -> None:
        if self.repository.is_empty():
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"등록된 퀴즈는 총 {self.repository.get_count()}개입니다.")
        for index, quiz in enumerate(self.repository.get_all(), start=1):
            print(f"{index}. {quiz.question}")

    def delete_quiz(self, quiz_index: int) -> None:
        if self.repository.is_empty():
            print("등록된 퀴즈가 없습니다.")
            return

        deleted_quiz = self.repository.delete(quiz_index)
        if deleted_quiz is None:
            print("잘못된 번호입니다.")
            return

        self.save_state()
        print(f"'{deleted_quiz.question}' 문제가 삭제되었습니다.")

    def show_score(self) -> None:
        if self.score_manager.get_best_score() is None:
            print("아직 퀴즈를 풀지 않았습니다.")
            return

        print(f"현재 최고 점수는 {self.score_manager.get_best_score()}점입니다.")

    def delete_quiz_menu(self) -> None:
        if self.repository.is_empty():
            print("등록된 퀴즈가 없습니다.")
            return

        self.show_quizzes()
        quiz_index = self.io.get_int_input("삭제할 퀴즈 번호를 입력하세요: ", 1, self.repository.get_count())
        self.delete_quiz(quiz_index)

    def show_score_history(self) -> None:
        if not self.score_manager.get_score_history():
            print("아직 게임 기록이 없습니다.")
            return

        print("게임 기록")
        for entry in self.score_manager.get_score_history():
            print(
                f"{entry['timestamp']} | 점수: {entry['score']}점 | 푼 문제 수: {entry['question_count']}"
            )

    def exit_game(self) -> None:
        print("프로그램을 종료합니다.")
        self.is_running = False

    def load_state(self) -> None:
        quizzes, best_score_loaded, score_history_loaded = self.storage.load()
        self.repository = QuizRepository(quizzes)
        self.score_manager = ScoreManager(best_score_loaded, score_history_loaded)

    def save_state(self) -> bool:
        return self.storage.save(
            self.repository.get_all(),
            self.score_manager.get_best_score(),
            self.score_manager.get_score_history(),
        )

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
            state_saved = self.save_state()
            self.io.safe_exit("사용자에 의해 프로그램이 중단되었습니다.", state_saved)
        except EOFError:
            state_saved = self.save_state()
            self.io.safe_exit("입력 스트림이 종료되었습니다.", state_saved)