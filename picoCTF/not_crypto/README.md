# not-crypto

## 調査
`fread(buf, 1, 0x40, stdin)`で入力された文字列と*謎の変数*の値をmemcmpで比較し、一致すれば`Yep, that's it!`と表示する。  
*謎の変数*の中にflagが入っていると考えられる。  

*謎の変数*の値は複雑な処理で計算されており、コードから簡単に解読できない。  
`there's crypto in here but the challenge is not crypto...`と述べられているように、難読化を解読するのではなさそうだ。

angrで条件を満たすような入力を見つけようとしたが、技術不足によりできなかった。

## exploit
ローカル変数である*謎の変数*の中に単純にflagが格納されているだけなので、**実行中にスタックの中身を表示すれば簡単にflagが分かる。**  
```bash
$ gdb-gef not-crypto
gef> b puts
gef> r
gef> c
Continuing.
I heard you wanted to bargain for a flag... whatcha got?
適当な文字列を入力
gef> p **((char[] **)($rsp+0x50))
flagが表示される
```