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

* Code segument
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


To be continued...

# Reference
##Markdowns that be used in Qiita
http://qiita.com/Qiita/items/c686397e4a0f4f11683d

