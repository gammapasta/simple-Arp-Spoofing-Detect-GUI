import subprocess
import os
from tkinter import *

window = Tk()
window.title("arp 공격 확인 프로그램")
window.geometry("700x400")

# arp -a command start
arp_output = subprocess.check_output(["arp", "-a"], universal_newlines=True)
print(arp_output)

with open("./arp_result.txt", "w", encoding="utf-8") as f:
    f.write(arp_output)

with open('arp_result.txt', 'r', encoding="utf-8") as f:
    lines = f.readlines()

# create an empty list for IP and MAC
ip_address = [[] for _ in range(5)]
mac_address = [[] for _ in range(5)]
name = [0] * 5
nameNum = 0

# get lines from .txt
for line in lines:
    parts = line.strip().split() #split by blanks
    if len(parts) == 4:  # 공백이 4줄로 나누어 지면 네트워크 인터페이스
        name[nameNum] = parts[1]
        # print(name[nameNum])
        nameNum += 1
    if len(parts) == 3:  # 공백이 3줄로 나누어질 때
        if parts[1] != "ff-ff-ff-ff-ff-ff":
            ip_address[nameNum - 1].append(parts[0])
            mac_address[nameNum - 1].append(parts[1])


# 결과 출력
print("IP 주소 목록:")
print(ip_address)
print("\nMAC 주소 목록:")
print(mac_address, "\n\n")

arr = []

# Text 위젯 생성
text = Text(window)
text.pack()

def check():
    rowNum=0
    noduplicated = FALSE
    for row in mac_address:
        arr = row
        # print(row)
        for i in range(len(arr)):
            temp = arr[i]
            for j in range(i + 1, len(arr)):
                sTemp = arr[j]
                if temp == sTemp:
                    text.insert(END, f"인터페이스 {name[rowNum]} 안에서 같은 mac 주소: {temp}\n")
                    noduplicated = TRUE
        if noduplicated == FALSE and (len(arr) > 1):
            text.insert(END, f"인터페이스 {name[rowNum]} 안에서 같은 mac 주소는 없습니다\n")
        rowNum += 1
        



label = Label(window, text="arp 확인 프로그램")
label.pack()

button1 = Button(window, text="확인하기", command=check)
button1.pack()

f.close()
os.remove("arp_result.txt")
window.mainloop()