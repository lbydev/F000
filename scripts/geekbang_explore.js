let body = $response.body
body = JSON.parse(body)
if (body['data'] != undefined) {
    body['data'].forEach((element, index) => {
        if (element['list'] !== undefined ) element['list']=[]
      });
}
body = JSON.stringify(body)
$done({body})
