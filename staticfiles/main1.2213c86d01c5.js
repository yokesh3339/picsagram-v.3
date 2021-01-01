
var prev = [];
var lis = [];
$(document).ready(function () {
    $(".likebutton").on( 'click', function () {
        e.preventDefault();
        var href = this.href;
        console.log(href);
        var catid;
        catid = $(this).attr("data-catid");
        console.log(catid)
        $.ajax({
            url: href,
            success: function (response) {
                console.log(response);
                if (response['likers']) {
                    $('#likes' + catid).html('<svg width="2em" height="2em" viewBox="0 0 16 16" class="bi bi-suit-heart-fill" fill="red" xmlns="http://www.w3.org/2000/svg"><path d="M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0 3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z"/></svg>');
                    $('#counts' + catid).html("LIKES:" + response['likes_count']);
                }

                else {
                    $('#likes' + catid).html('<svg width="2em" height="2em" viewBox="0 0 16 16" class="bi bi-suit-heart" fill="white" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 6.236l.894-1.789c.222-.443.607-1.08 1.152-1.595C10.582 2.345 11.224 2 12 2c1.676 0 3 1.326 3 2.92 0 1.211-.554 2.066-1.868 3.37-.337.334-.721.695-1.146 1.093C10.878 10.423 9.5 11.717 8 13.447c-1.5-1.73-2.878-3.024-3.986-4.064-.425-.398-.81-.76-1.146-1.093C1.554 6.986 1 6.131 1 4.92 1 3.326 2.324 2 4 2c.776 0 1.418.345 1.954.852.545.515.93 1.152 1.152 1.595L8 6.236zm.392 8.292a.513.513 0 0 1-.784 0c-1.601-1.902-3.05-3.262-4.243-4.381C1.3 8.208 0 6.989 0 4.92 0 2.755 1.79 1 4 1c1.6 0 2.719 1.05 3.404 2.008.26.365.458.716.596.992a7.55 7.55 0 0 1 .596-.992C9.281 2.049 10.4 1 12 1c2.21 0 4 1.755 4 3.92 0 2.069-1.3 3.288-3.365 5.227-1.193 1.12-2.642 2.48-4.243 4.38z"/></svg>');
                    $('#counts' + catid).html("LIKES:" + response['likes_count']);
                }
            }
        })
    }),
        $(".follow").click(function (e) {
            e.preventDefault();
            var href = this.href;
            console.log(href);
            var catid;
            catid = $(this).attr("data-catid");
            console.log(catid)
            $.ajax({
                url: href,
                success: function (response1) {
                    console.log(response1);
                    if (response1['followers']) {
                        $('*#follow' + catid).html("Unfollow").removeClass("btn btn-info").addClass("btn btn-danger");
                        var create_a = $("<a></a>").text(response1['active_user']).attr({ "href": "../listing/" + response1['active_user'], "id": 'followers' + response1['active_user'], class: "dropdown-item alert alert-primary" });
                        $('#followedprof').append(create_a);
                        $('.followedprofcount').html("Followers " + response1['followers_counts_active']);

                    }

                    else {
                        $('*#follow' + catid).html("Follow").removeClass("btn btn-danger").addClass("btn btn-info");
                        $('#followers' + response1['active_user']).remove();
                        $('.followedprofcount').html("Followers " + response1['followers_counts_active']);
                    }
                }
            })
        }),
        $("#search").keyup(function () {
            if (!(this.value === '')) {
                $.ajax({
                    url: "autocomplete",
                    type: 'get',
                    data: {
                        "term": this.value
                    },
                    success: function (lis) {
                        clearAll();
                        for (let i = 0; i < lis.length; i++) {
                            createTag(lis[i]);
                        }
                        var prev = lis;
                    }
                });
            }
            else {
                clearAll();
            }
        }),
        $(".addcmt").click(function (e) {
            e.preventDefault();
            var c_id = $(this).attr("data-catid");
            var val = document.querySelector("#message-text" + c_id);
            console.log("cmt");
            console.log(val.value);
            $.ajax({
                url: "comment",
                type: 'get',
                data: {
                    'cmt': val.value,
                    'id': c_id

                },
                success: function (names) {
                    console.log(names[0]);
                    createComment(names[0], "#comment" + c_id);
                    val.value = "";
                    $("#scroll" + c_id).animate({ scrollTop: $(document).height() }, "fast");

                }

            })


        }),
        $(".createcmt").click(function (e) {
            e.preventDefault();
            var c_id = $(this).attr("data-catid");
            console.log("cmt_fetch");
            $.ajax({
                url: "get_comment",
                type: 'get',
                data: {
                    'id': c_id

                },
                success: function (names) {
                    console.log(names);
                    qs = document.querySelector("#comment" + c_id);
                    ls = document.createElement("div");
                    ls.className = "card-header";
                    ls.textContent = "Comments";
                    qs.append(ls);
                    for (let i = 0; i < names.length; i++) {
                        createComment(names[i], "#comment" + c_id);
                    }

                }

            })


        }),
        $(".onclose").click(function (e) {
            e.preventDefault();
            var c_id = $(this).attr("data-catid");
            qs = document.querySelector("#comment" + c_id);
            qs.innerHTML = "";
        });

});
function clearAll() {
    mb = document.querySelector("#user");
    mb.innerHTML = "";
    ls = document.createElement('div');
    ls.className = "card-header";
    ls.textContent = "List";
    mb.append(ls);
}
function createTag(val) {
    mb = document.querySelector("#user");
    var div_cb = document.createElement('div');
    div_cb.className = "card-body";
    div_cb.style = "margin:0%";
    a_p = document.createElement('a');
    a_p.className = "btn btn-link shadow-none";
    a_p.style = "color: white;margin:0%;text-decoration:none;";
    a_p.href = "../profat/" + val['names'];
    img = document.createElement('img');
    img.src = val['img'];
    img.style = "height:35px;width:35px;border-radius: 50%;margin:0%;margin-right:1em;";
    h5 = document.createElement('h5');
    h5.className = "card-title d-inline";
    h5.textContent = val['names'] + "(" + val["fullname"] + ")";
    p = document.createElement('p');
    p.className = "card-texxt d-inline";
    a_p.append(img);
    a_p.append(h5);
    a_p.append(p);
    div_cb.append(a_p);
    mb.append(div_cb);




}
function createComment(val, ids) {
    mb = document.querySelector(ids);
    var div_cb = document.createElement('div');
    div_cb.className = "card-body";
    div_cb.style = "margin:0%";
    a_p = document.createElement('a');
    a_p.className = "btn btn-link shadow-none";
    a_p.style = "color: white;margin:0%;text-decoration:none;";
    a_p.href = "../profat/" + val['names'];
    img = document.createElement('img');
    img.src = val['img'];
    img.style = "height:35px;width:35px;border-radius: 50%;margin:0%;margin-right:1em;";
    h5 = document.createElement('h5');
    h5.className = "card-title d-inline";
    h5.textContent = val['names'] + ": ";
    p = document.createElement('p');
    p.className = "card-texxt d-inline";
    d = new Date(val['time']);
    dt = d.toLocaleString();
    p.innerHTML = hashtag_element(val['comment']) + " (" + dt + ")";
    a_p.append(img);
    a_p.append(h5);
    div_cb.append(a_p);
    div_cb.append(p);
    mb.append(div_cb);
}
function hashtag_element(val) {
    var string = val.toLowerCase();
    string = string.replace(/#(\S*)/g, '<a href="../search/$1" style="margin:0px;text-decoration:none;">#$1</a>');
    string = string.replace(/@(\S*)/g, '<a href="../profat/$1" style="margin:0px;text-decoration:none;">@$1</a>');
    return string;
}
