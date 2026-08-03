class QuizGame:
    """콘솔 퀴즈 게임의 기본 화면을 관리한다."""

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

    def run(self) -> None:
        self.display_menu()


def main() -> None:
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()