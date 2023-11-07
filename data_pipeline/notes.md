# Steps:

## Convert pcap files into nfpcap

```shell
nfpcapd -r igb0_0000 -l output/
```

### Issues

This doesn't work on enc0_0000:
```shell
Unsupported data link type 109
```

This doesn't work on ovpns1_0000:
```shell
Couldn't attach FILE handle truncated dump file; tried to read 4 file header bytes, only got 0
```

Some packets in the igb files can't be parsed:
```shell
Startup.
[140244681156544] WaitDone() waiting
Unsupported ether type: 0x7373, packet: 7
Unsupported ether type: 0x7373, packet: 8
Unsupported ether type: 0x7373, packet: 20
Unsupported ether type: 0x7373, packet: 21
Unsupported ether type: 0x7373, packet: 43
Unsupported ether type: 0x7373, packet: 44
<...>
Unsupported ether type: 0x7373, packet: 2426
Unsupported ether type: 0x7373, packet: 2428
Unsupported ether type: 0x7373, packet: 2949
Unsupported ether type: 0x7373, packet: 2951
Expired Nodes: 3, in use: 137, total flows: 120
pcap_next_ex() end of file
Packet processing stats: Total: 3904, Skipped: 106, Unknown: 204, Short snaplen: 262
Packet processing stats: Total: 3904, Skipped: 106, Unknown: 204, Short snaplen: 262
```


Is it expected that sa and da contain a lot of `10.200.2.9`? Could it be the NAT issue that Erick mentioned?

- flows are likely getting split; we should try to increase timeout in the pcap->netflow script


## Convert pcapd to netflow
```shell
nfdump -R  netflow -o csv  > netflow.csv
```


