def calculate_checksum(command):
    # 16진수 0x100 (256)로 시작, 8비트 감산
    value = 0x100

    # 각 문자의 아스키 코드로 변환하고 16진수 FF에서 차례대로 감산
    for char in command:
        ascii_value = ord(char)  # 문자를 아스키 코드로 변환
        value = value - ascii_value  # 감산
        if value < 0:  # 8비트 값을 유지하기 위해 음수일 경우 0x100 더하기
            value += 0x100

    # 체크섬 결과
    checksum = value & 0xFF  # 8비트 값으로 유지

    return f"{checksum:02X}"  # 16진수 2자리 문자열로 반환

# 테스트 예시
command = input("Enter command: ")
checksum = calculate_checksum(command)
print(f"Calculated checksum: {checksum}")
