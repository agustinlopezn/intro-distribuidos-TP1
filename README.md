# intro-distribuidos-TP1

iptables:

entrar como root:
sudo -i

crear regla:
iptables -A INPUT -p udp --dport 5000 -m statistic --mode random --probability 0.05 -j DROP
iptables -A OUTPUT -p udp --sport 5000 -m statistic --mode random --probability 0.05 -j DROP

ver reglas:
iptables -L -v -n

borrar reglas:
iptables -F