## Generate NPCAP

```shell
for file in pcap/attack_2/*; do nfpcapd -r $file -l npcap/; done
```

## Generate Netflow

```shell
nfdump -R  data/input/npcap/attack_1 -o json > netflow.json
```

## Generate Parquet

```shell
python main.py
```