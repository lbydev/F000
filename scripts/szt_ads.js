// 服务器返回的是 GBK 编码文本, 直接用 $response.body 会导致乱码和解析失败。
// 我们需要先获取原始的二进制数据流 $response.bodyBytes, 然后用 $utils.decode 手动指定 GBK 解码。
const bodyString = $utils.decode($response.bodyBytes, 'gbk');
let body = JSON.parse(bodyString);

if (body.advlist && body.advlist.length > 0) {
  body.advlist = [];
  body.totalnum = "0";
}

// 将修改后的对象转回 JSON 字符串，并作为响应返回。
// Surge 会自动处理后续的编码，我们不需要再转回 GBK。
$done({ body: JSON.stringify(body) });
