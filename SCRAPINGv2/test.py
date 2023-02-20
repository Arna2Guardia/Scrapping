import math,socket

server = "irc.root-me.org"
port = 6667
nickname = "Arna"
target = "candy"
channel = "#root-me_challenge"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, 6667))

irc.send("JOIN #root-me_challenge".encode())
print("JOIN #root-me_challenge")
irc.send("PRIVMSG candy !ep1\r\n".encode())

rep = irc.recv(1024).decode()
print("Rep is:" + rep)
nb1, nb2 = rep.split(b"/")
rep2 = int(nb1) / int(nb2)
irc.send(rep2.encode())
print(irc.recv(1024))


