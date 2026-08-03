import json
import os

from quiz import DEFAULT_QUIZZES, Quiz

STATE_FILE = "state.json"


class QuizGame:
    """콘솔 퀴즈 게임의 기본 화면을 관리한다."""

    def __init__(self) -> None:
        self.is_running = True
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.load_state()

    def display_menu(self) -> None:
        print("=" * 40)
        print("        나만의 퀴즈 게임")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def play_quiz(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print("퀴즈 풀기를 시작합니다.")
        correct_count = 0

        for index, quiz in enumerate(self.quizzes, start=1):
            quiz.display(index)
            user_answer = self.get_int_input("정답 입력 (1-4): ", 1, 4)
            if quiz.is_correct(user_answer):
                correct_count += 1
                print("정답입니다!")
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n총 {len(self.quizzes)}문제 중 {correct_count}문제를 맞혔습니다.")
        print(f"최종 점수: {correct_count}점")

    def add_quiz(self) -> None:
        print("퀴즈 추가 기능을 실행합니다.")

    def show_quizzes(self) -> None:
        print("퀴즈 목록 기능을 실행합니다.")

    def show_score(self) -> None:
        print("점수 확인 기능을 실행합니다.")

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
        except json.JSONDecodeError:
            print("ERROR: state.json 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None
        except OSError as e:
            print(f"ERROR: 파일을 읽는 중 오류가 발생했습니다: {e}")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None

    def safe_exit(self, message: str) -> None:
        print(f"\n{message}")
        print("프로그램을 안전하게 종료합니다.")

    def get_int_input(self, prompt: str, min_value: int, max_value: int) -> int:
        while True:
            raw_value = input(prompt).strip()
            if raw_value == "":
                print(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            try:
                value = int(raw_value)
            except ValueError:
                print(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if value < min_value or value > max_value:
                print(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return value

    def get_menu_choice(self) -> str:
        return str(self.get_int_input("선택: ", 1, 5))

    def run(self) -> None:
        actions = {
            "1": self.play_quiz,
            "2": self.add_quiz,
            "3": self.show_quizzes,
            "4": self.show_score,
            "5": self.exit_game,
        }

        try:
            while self.is_running:
                self.display_menu()
                choice = self.get_menu_choice()

                action = actions.get(choice)
                if action:
                    action()
        except KeyboardInterrupt:
            self.safe_exit("사용자에 의해 프로그램이 중단되었습니다.")
        except EOFError:
            self.safe_exit("입력 스트림이 종료되었습니다.")


def main() -> None:
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()