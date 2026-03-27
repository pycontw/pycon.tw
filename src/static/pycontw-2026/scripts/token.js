// Tom 2020-08-22:
// This is a hack to inject the token to the next parameter
// The current implementation of the language switcher does not
// support query parameters, which means all query paremeters
// will be lost after switching language.

// However, the token parameter is required in this page,
// So we find the "next" field which is used to redirect
// to the destination page after switching language,
// and then inject the token parameter inside
// so the page won't be broken after language switch

if (window.TOKEN) {
    var next = document.querySelector("[name='next']");
    var params = new URLSearchParams();
    params.append('token', window.TOKEN);

    // Cannot use next.value += ...
    // Because when you refresh the page, the input value is preserved
    // So there would be a lot of concated ?token=... in next.value
    next.value = `${next.value.split('?')[0]}?${params.toString()}`;
}
