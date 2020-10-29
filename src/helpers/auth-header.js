export function authHeader() {
    // return authorization header with jwt token
    let token = JSON.parse(localStorage.getItem('auth_token'));

    if (token) {
        return { 'Authorization': 'JWT ' + token.access_token };
    } else {
        return {};
    }
}

export function parseJwt(token) {
    var base64Url = token.access_token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map((c) => {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
}