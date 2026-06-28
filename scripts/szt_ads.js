let body = JSON.parse($response.body);
if (body.advlist && body.advlist.length > 0) {
 body.advlist = [];
 body.totalnum = "0";
 }
$done({ body: JSON.stringify(body) });
