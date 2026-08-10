class ConsoleIO:
    """콘솔 입출력과 입력 검증을 담당한다."""

    def display_menu(self) -> None:
        print("=" * 40)
        print("        나만의 퀴즈 게임")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 기록 보기")
        print("7. 종료")
        print("=" * 40)

    def print_message(self, message: str) -> None:
        print(message)

    def get_non_empty_text_input(self, prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value == "":
                print("잘못된 입력입니다. 빈 입력은 허용되지 않습니다.")
                continue
            return value

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
        return str(self.get_int_input("선택: ", 1, 7))

    def safe_exit(self, message: str) -> None:
        print(f"\n{message}")
        print("프로그램을 안전하게 종료합니다.")