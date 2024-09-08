let body = $response.body
body = JSON.parse(body)
if (body['data']['list'] != undefined) {
    body['data']['list'].forEach((element, index) => {
        if (element['had_freelyread'] !== undefined ){
          element['had_freelyread']= false;
          element['had_viewed']= false;
          element['is_required']= false;
          element['article_could_preview']= true;
        } 
      });
}
body = JSON.stringify(body)
$done({body})
