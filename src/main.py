import pandas as pd
import gui

arp_table = pd.DataFrame({
    'IP_Address': ['192.168.1.1', '192.168.1.10', '192.168.1.11', '192.168.1.1'],
    'MAC_Address': ['AA:BB:CC:11:22:33', 'EE:FF:GG:44:55:66', 'HH:II:JJ:77:88:99', 'ZZ:YY:XX:11:22:33']
})

print("Simulated ARP Table:\n", arp_table, "\n")

suspicious = arp_table.groupby('IP_Address').filter(lambda x: x['MAC_Address'].nunique() > 1)

if not suspicious.empty:
    print("Warning: Possible ARP spoofing detected!")
    print(suspicious)
else:
    print("No duplicate IP-MAC mappings found.")