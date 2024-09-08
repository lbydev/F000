let body = $response.body
body = JSON.parse(body)
body['data']['footer_cover_data'] = null
if (body['data']['freelyread_count']) {
    body['data']['freelyread_count']= 0;
    body['data']['had_freelyread']= false;
    body['data']['had_viewed']= false;
    body['data']['is_required']= false;
    body['data']['article_could_preview']= true;
    body['data']['in_pvip']= 0;
    body['data']['is_vip']= true;
}
body = JSON.stringify(body)
$done({body})
