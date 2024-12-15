# piercing_misty_mountain

## Checksec
- statically-linked
- no PIE

## 脆弱性
Checksecの結果を見ると、gadgetが使えそう。  
return addrを上書きできるのでROPが考えられる。  
ただし0x08分しか追加で書き込めないのでreturn先の工夫が必要。  

```c
int profile() {
  char job[0x8] = "Job:";
  char age[0x8];
  printf("Job > ");
  read_n(job + 4, 0x18 - 4);  // オーバーフロー
...
}
```

## 方針
mainのbufは自由に書き込み可能なのでこれを利用したい。  
**return先をprofile()にして繰り返し呼ぶことでスタックの位置を調整できる**

| 内容 | 値 |
| -- | -- |
| profile.job |
| profile.age |
| return address | **profile()** | 
| 省略 |
| main.buf | ROP |

1. profileのreturn addressをprofile()に上書きする
2. これを繰り返してrbpをmain.bufに移動させる
3. main.bufに事前にROPのための値を設定する
    1. syscallを利用してシェルを呼び出す
    2. `/bin/sh`が実行ファイル内に見つからないので、事前に`read`を呼び出してメモリに文字列をセット(`0x4c5000`が書き込み可能)

## 攻撃コード
[exploit.py](exploit.py)