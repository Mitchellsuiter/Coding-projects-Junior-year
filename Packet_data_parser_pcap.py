import dpkt
import socket
import collections

filename='capture.pcap'
f = open(filename, 'rb')
pcap = dpkt.pcap.Reader(f)
Ip_synACK_dict={}

for ts, buf in pcap:

    eth=dpkt.ethernet.Ethernet(buf) 
    if eth.type == dpkt.ethernet.ETH_TYPE_IP:
        #print('is ip packet')
        ip=eth.data
        source_ip= socket.inet_ntoa(ip.src)
        
        
        if ip.p == (dpkt.ip.IP_PROTO_TCP):
            tcp=ip.data
            #print('is tcp packet')
            
        try:
            if ( tcp.flags and dpkt.tcp.TH_SYN and dpkt.tcp.TH_ACK ) != 0:
                #print('is tcp syn')
                if source_ip in Ip_synACK_dict.keys():
                    Ip_synACK_dict[source_ip] +=1
                else:
                    Ip_synACK_dict[source_ip]=1
                #print(synflagcounter)
                #print(source_ip)
                #
                continue
        except: AttributeError

print(collections.Counter(Ip_synACK_dict).most_common(10))
    

            
