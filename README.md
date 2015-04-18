# ConvertMyMediawikiToQiita
This is a program that converts form of my mediawiki to form of Qiita.

# Convert Examples
* Code
```bash
./Convert.py << '__EOF__'
> <code>hoge</code> abcde <code>fuga</code>
>   <span>test</span>
> <code>hoge2</code><span>fuga2</span>
> __EOF__
`hoge` abcde `fuga`
  <span>test</span>
`hoge2`<span>fuga2</span>
```

* Headings
```bash
$ ./Convert.py << '__EOF__'
> = hoge =
> ====== fuga ======
> __EOF__
# hoge 
###### fuga
```

* Definishons
```bash
./Convert.py << '__EOF__'
> ;aaa
> :aaaa
> :aaaaa
> 
> hogefjga
> ;bbb
> :bbbb
> :bbbbb
> 
> ;xxx
> :yyy
> I'm living in Tokyo.
> 
> ;ccc
> :ccc
> ;ddd
> :ddd
> __EOF__
<dl>
  <dt>aaa</dt>
  <dd>aaaa</dd>
  <dd>aaaaa</dd>
</dl>

hogefjga
<dl>
  <dt>bbb</dt>
  <dd>bbbb</dd>
  <dd>bbbbb</dd>
</dl>

<dl>
  <dt>xxx</dt>
  <dd>yyy</dd>
</dl>
I'm living in Tokyo.

<dl>
  <dt>ccc</dt>
  <dd>ccc</dd>
  <dt>ddd</dt>
  <dd>ddd</dd>
</dl>
```

To be continued...

# Reference
##Markdowns that be used in Qiita
http://qiita.com/Qiita/items/c686397e4a0f4f11683d

