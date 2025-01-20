# file_viewer2

## 脆弱性
`items[index].str`が文字列`*content`の参照を持った状態で`*content`が`arena[filename]`にmoveされており、`items[index].str`がダグリング参照となっている。
```c++
void update_items(int index, std::unique_ptr<std::string> content, const std::string& filename)
{
    std::string_view str = *content;
...
    items[index].str = str;
...
    arena[filename] = std::move(*content);
}
```

## 方針
素直にflagファイルを表示しようとするとredacted。
そこで、普通のテキストファイルを読み込んでその`str`がflagファイルの中身を指すようにする。

1. flagと同じぐらいのサイズのテキストファイルを読み込む（FAKEフラグの場合には`/usr/share/debianutils/shells.d/dash`を用いた。本物のフラグのサイズに合わせる。）
2. flagを読み込んで1のテキストファイルの`str`を上書き

## 攻撃コード
[exploit.py](exploit.py)