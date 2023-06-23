a = "[INFO]"
print(a[1:-1])

import re
a= "响应时间:85ms"
res = re.match(r".*:(\d+)ms",a).group(1)
print(res)