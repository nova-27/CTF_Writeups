# vuln_img

## Checksec
```
Arch:       amd64-64-little
RELRO:      No RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        No PIE (0xfff000)
Stripped:   No
```

## 脆弱性
`buf`を超えて書き込める。
```c
char buf[0x100];
scanf("%s", buf);
```

画像データの領域が実行可能になっている。
```c
// Make the data read-only.
mprotect(img_data, IMG_DATA_SIZE, VALIDATE_PROT(~PROT_WRITE));   // r-x
```

## 方針
return addrを上書きできるのでROP  
vuln_imgはgadgetが少ないので、実行可能な画像データ領域のgadgetを利用する。

| 内容 | 値 |
| -- | -- |
| buf |
| size |
| fd |
| return address | **上書き** |
| **ROP** |

1. 0xfff000の領域に`/bin/sh`を書き込む（0xb000000は文字が読み取られない？）
2. execveでシェルを呼び出す

## 攻撃コード
[exploit.py](exploit.py)