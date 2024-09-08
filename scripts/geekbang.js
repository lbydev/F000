let body = $response.body
body = JSON.parse(body)
body['data']['is_prompt'] = false
body['data']['is_force'] = false
body = JSON.stringify(body)
$done({body})
