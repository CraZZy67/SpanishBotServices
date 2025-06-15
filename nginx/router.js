function routeRequest(req) {
    const body = req.requestText;
    const data = JSON.parse(body);

    if ('pre_checkout_query' in data) {
        req.internalRedirect('@payment');
    } else if ('message' in data && 'successful_payment' in data.message) {
        req.internalRedirect('@payment');
    } else {
        req.internalRedirect('@bot');
    }
}

export default { routeRequest };