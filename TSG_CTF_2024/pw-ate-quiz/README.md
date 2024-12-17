# pw-ate-quiz

## 脆弱性
`idx >= 0`なのでhints[2]を超えて文字を表示してしまう。

```c
int idx;
printf("Enter a hint number (0~2) > ");
if (scanf("%d", &idx) == 1 && idx >= 0) {
    for (int i = 0; i < 8; i++) {
        putchar(hints[idx][i]);
    }
    puts("");
} else {
    break;
}
```

## 方針
passwordを漏洩させる。  
ただしkeyを用いて暗号化した状態で格納されているのでkeyも必要。  
keyは漏洩できないため、暗号化されたinputからkeyを推定する。

| 内容 | 値 |
| -- | -- |
| key |  |
| 省略 |  |
| hints |  |
| password | 暗号化されたパスワード |
| input | ヒント表示前に入力し、暗号化されたもの |

1. 最初のパスワード入力はわかりやすいテキトウな文字列A
2. ヒント番号は不正な値を入力して、password(文字列B)とinput(文字列C)を漏洩する
3. key = C ^ A
4. 暗号化前password = B ^ key

## 攻撃コード
[exploit.py](exploit.py)