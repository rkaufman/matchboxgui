export function authHeader() {
    // return authorization header with jwt token
    let token = JSON.parse(localStorage.getItem('auth_token'));

    if (token) {
        return { 'Authorization': 'JWT ' + token.access_token };
    } else {
        return {};
    }
}