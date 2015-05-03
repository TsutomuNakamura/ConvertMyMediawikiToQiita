# ConvertMyMediawikiToQiita
This is a program that converts form of my mediawiki to form of Qiita.

# Convert Examples
* Code tag
```bash
./Convert.py << '__EOF__'
<code>hoge</code>
<span>fuga</span>
__EOF__
```

```bash
`hoge`
<span>fuga</span>
```

* br tag
```bash
./Convert.py << '__EOF__'
hoge<br>
fuga<br />
__EOF__
```

result:
```bash
hoge
fuga
```

* Headings
```bash
./Convert.py << '__EOF__'
= hoge =
====== fuga ======
__EOF__
```

result:
```bash
# hoge 
###### fuga
```

* Definishons
```bash
./Convert.py << '__EOF__'
;aaa
:aaaa
:aaaaa

;ccc
:ccc
;ddd
:ddd
__EOF__
```

result:
```bash
<dl>
  <dt>aaa</dt>
  <dd>aaaa</dd>
  <dd>aaaaa</dd>
</dl>

<dl>
  <dt>ccc</dt>
  <dd>ccc</dd>
  <dt>ddd</dt>
  <dd>ddd</dd>
</dl>
```

* Code segment
```bash
./Convert.py << '__EOF__'
<syntaxhighlight lang="ruby">
puts 'Hello, world!'
</syntaxhighlight>

Here is not text code segment.
 Here is text
 code segment.
__EOF__
```

result:
```bash
```ruby
puts 'Hello, world!'
```　

Here is not text code segment.
```text
Here is text
code segment.
```　
```
(In actually, no multibyte blank will be output)


* Code segment title in my own rule
```bash
./Convert.py << '__EOF__'
This is tutorial of Java.
* HelloWorld.java
<syntaxhighlight lang="java">
public class HelloWorld {
    public static void main(String args[]) {
        System.out.println("Hello world.");
    }
}
</syntaxhighlight>
__EOF__
```

result:
```bash
This is tutorial of Java.
```java:HelloWorld.java
public class HelloWorld {
    public static void main(String args[]) {
        System.out.println("Hello world.");
    }
}
```　
```
(In actually, no multibyte blank will be output)

* Table segment
```bash
$ ./Convert.py << '__EOF__'
{| class="wikitable"
|+ align="top" style="text-align: left" |''テーブルのサンプル''
|-
! subject1
! subject2
! subject3
|-
| text1
| text2
| text3
|-
| text1 || text2 || text3
|-
| text1 !! text2 || text3
|-
! text1 !! text2 !! text3
|-
! text1 || text2 !! text3
|}
__EOF__

* テーブルのサンプル
<table><tbody>
  <tr>
    <th> subject1</th>
    <th> subject2</th>
    <th> subject3</th>
  </tr>
  <tr>
    <td> text1</td>
    <td> text2</td>
    <td> text3</td>
  </tr>
  <tr>
    <td> text1 </td><td> text2 </td><td> text3</td>
  </tr>
  <tr>
    <td> text1 </td><th> text2 </th><td> text3</td>
  </tr>
  <tr>
    <th> text1 </th><th> text2 </th><th> text3</th>
  </tr>
  <tr>
    <th> text1 </th><td> text2 </td><th> text3</th>
  </tr>
</tbody></table>
```

# Reference
##Markdowns that be used in Qiita
http://qiita.com/Qiita/items/c686397e4a0f4f11683d

