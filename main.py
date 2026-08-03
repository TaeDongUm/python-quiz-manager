class QuizGame:
    """콘솔 퀴즈 게임의 기본 화면을 관리한다."""

    def __init__(self) -> None:
        self.is_running = True

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
        print("퀴즈 풀기 기능을 실행합니다.")

    def add_quiz(self) -> None:
        print("퀴즈 추가 기능을 실행합니다.")

    def show_quizzes(self) -> None:
        print("퀴즈 목록 기능을 실행합니다.")

    def show_score(self) -> None:
        print("점수 확인 기능을 실행합니다.")

    def exit_game(self) -> None:
        print("프로그램을 종료합니다.")
        self.is_running = False

    def run(self) -> None:
        actions = {
            "1": self.play_quiz,
            "2": self.add_quiz,
            "3": self.show_quizzes,
            "4": self.show_score,
            "5": self.exit_game,
        }

        while self.is_running:
            self.display_menu()
            choice = input("선택: ")

            action = actions.get(choice)
            if action:
                action()


def main() -> None:
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()