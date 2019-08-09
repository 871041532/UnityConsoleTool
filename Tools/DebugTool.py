import sys
import socket
import _thread
from Color import Color

# 获取端口号
try:
	args = sys.argv[1:]
	port = int(args[0])
except Exception as e:
	print("请输入端口号！")


# GM相关指令
class LogType:
    Error = "#0"
    Assert = "#1"
    Warning = "#2"
    Log = "#3"
    Exception = "#4"


# GM处理函数
color_log = Color()

def switch_error():
	color_log.set_red()
	color_log.print("\nTrace or Error:")

def switch_warning():
	color_log.set_yellow()
	color_log.print("\nWarning:")

def switch_normal():
	color_log.print("")
	color_log.set_white()


gm_dict = {
	LogType.Error: switch_error,
	LogType.Assert: switch_error,
	LogType.Warning: switch_warning,
	LogType.Log: switch_normal,
	LogType.Exception: switch_error,
}

# 解析发来的字符串
def prase_str(strs):
	if strs in gm_dict:
		gm_dict[strs]()
	else:
		color_log.print(strs)

# 启动UDP服务端
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', port))
color_log.print_green("UPD Server Open, Port: " + args[0])
is_init = False
addr = 0

def receive_input():
	while True:
		strs = input()
		s.sendto(strs.encode("utf-8"), addr)

while True:
 	data, client_addr = s.recvfrom(2048)
 	addr = client_addr
 	prase_str(data.decode(encoding="utf-8"))
 	if not is_init:
 		is_init = True
 		_thread.start_new_thread(receive_input, ())