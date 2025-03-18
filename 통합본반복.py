import serial
import time

def send_enq_and_wait_for_ack(ser):
    """ENQ 전송 및 ACK 수신 확인"""
    ENQ = chr(0x05)  # ENQ 코드
    ACK = chr(0x06)  # ACK 코드
    #CAN= chr(0x18)   #CAN 코드
    #EOT= chr(0x04)   #EOT 코드
    # ENQ 전송
    ser.write(ENQ.encode('ascii'))
    print("Sent: ENQ")
    response = ser.read(1).decode('ascii')
    if response == ACK:
        print("Received: ACK")
        return True
    else:
        print("Error: ACK not received.")
        return False
    # ACK 수신 대기
    #start_time = time.time()
    #timeout = 2  # 2초 대기
    #while True:
    #   if ser.in_waiting > 0:  # 데이터 수신 확인
    #       response = ser.read(1).decode('ascii')
    #       if response == ACK:
    #           print("Received: ACK")
    #           return
    #   if time.time() - start_time > timeout:  # 타임아웃 처리
    #       print("Error: ACK not received.")
    #       return False

def send_rs232_command(ser,dispense_time):
    """
    RS-232 통신으로 송신 코드를 전송하고 응답을 읽는 함수.
    :param ser: 시리얼 포트 객체
    :param command: 명령어 (2-4 bytes)
    :param data: 데이터 (2-15 bytes)
    :return: 장비로부터의 응답
    """
    # STX와 ETX 제어 문자 정의
    STX = chr(0x02)  # ASCII 코드 0x02
    ETX = chr(0x03)  # ASCII 코드 0x03
    CAN= chr(0x18)   #CAN 코드
    EOT= chr(0x04)   #EOT 코드

    # 송수신 코드 생성
    transmit_code = f"{STX}04DI  CF{ETX}"
    good=f"{STX}02A02D{ETX}"
    error=f"{STX}02A22B{ETX}"
    
    ser.write(transmit_code.encode('ascii'))
    print(f"Sent: {transmit_code}")
    time.sleep(float(dispense_time+0.03))#토출시간에따라 0.03이상 조절가능 짧을수록0.03 반복수많을수록 증가가능성있음
    # 응답 읽기
    response = ser.read(ser.inWaiting()).decode('ascii')
    
    print(f"Received: {response}")
    if response==good:
        ser.write(EOT.encode('ascii'))
        print(f"Sent: EOT")
    else:
        ser.write(CAN.encode('ascii'))
        print(f"Sent: CAN")
        ser.write(EOT.encode('ascii'))
        print(f"Sent: EOT")




# 장비와 연결
try:
    ser = serial.Serial(port='COM5', baudrate=38400, timeout=1)
    print("Serial connection established.")
    # 반복값 입력
    repeat_count = int(input("Enter repeat count: "))
    #분사시간
    dispense_time=float(input("dispens time(s):"))
    # 반복 ENQ 전송 및 처리
    for i in range(repeat_count):
        print(f"Iteration {i + 1} of {repeat_count}")
    # ENQ/ACK 확인
        if send_enq_and_wait_for_ack(ser):
            print("Device is ready.")
           
            
            #추가명령어처
            send_rs232_command(ser,dispense_time)

        else:
            print("Device is not responding.")

finally:
    ser.close()
    print("Serial connection closed.")
