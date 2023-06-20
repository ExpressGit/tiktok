// 发 post 请求
function SendAjax() {
    var data = {};
    data = $('#form1').serialize();
    $.ajax({
        type: 'POST',
        url: "/douyin",
        data: data,
        dataType: 'json',
        beforeSend: function () {
            $("#loading").attr("style", "display:block;");//在请求后台数据之前显示loading图标
            $("#download").attr("style", "display:none;");//隐藏 download
        },
        success: function (result) {
            // console.log(result);//打印服务端返回的数据(调试用)
            if (result.status_code === 200) {
                result = result.data
                if (result.awemeType === 0) {
                    $("#awemeType").html("预览视频");
                    $("#AwemeOrLive").html("下载视频");
                    $("#video").attr("href", removeHttp(result.video.play_addr.url_list[0]));
                    $("#pre_video").attr("src", removeHttp(result.video.play_addr.url_list[0]));
                    $("#video").attr("style", "display:inline;");//显示 video
                }
                if (result.awemeType === 1) {
                    $("#awemeType").html("预览图集");
                    var images = result.images;
                    var licontent = ""; // 拼接输入的 li 标签的字符串
                    for (var i = 0; i < images.length; i++) {
                        licontent += "<li><img src= " + removeHttp(images[i].url_list[0]) + "></li>"
                    }
                    document.getElementById("images").innerHTML = licontent;
                    $("#video").attr("style", "display:none;");//隐藏 video
                }
                if (result.awemeType === 0 || result.awemeType === 1) {
                    $("#cover").attr("href", removeHttp(result.video.cover_original_scale.url_list[0]));
                    $("#pre_video").attr("poster", removeHttp(result.video.dynamic_cover.url_list[0]));
                    $("#music").attr("href", removeHttp(result.music.play_url.url_list[0]));

                    $("#avatar").attr("src", removeHttp(result.author.avatar.url_list[0]));
                    $("#avatar").attr("alt", result.author.nickname);
                    $("#nickname").html(result.author.nickname);
                    $("#desc").html(result.desc);


                    var count = result.statistics.digg_count;
                    var digg_count;
                    if (count < 1000) {
                        digg_count = count
                    } else if (count >= 1000 && count < 10000) {
                        digg_count = (count / 1000).toFixed(1) + "K"
                    } else {
                        digg_count = (count / 10000).toFixed(1) + "W"
                    }
                    $("#aweme_digg_count").html(digg_count);
                    count = result.statistics.comment_count;
                    var comment_count;
                    if (count < 1000) {
                        comment_count = count
                    } else if (count >= 1000 && count < 10000) {
                        comment_count = (count / 1000).toFixed(1) + "K"
                    } else {
                        comment_count = (count / 10000).toFixed(1) + "W"
                    }
                    $("#aweme_comment_count").html(comment_count);
                    count = result.statistics.collect_count;
                    var collect_count;
                    if (count < 1000) {
                        collect_count = count
                    } else if (count >= 1000 && count < 10000) {
                        collect_count = (count / 1000).toFixed(1) + "K"
                    } else {
                        collect_count = (count / 10000).toFixed(1) + "W"
                    }
                    $("#aweme_collect_count").html(collect_count);
                    count = result.statistics.share_count;
                    var share_count;
                    if (count < 1000) {
                        share_count = count
                    } else if (count >= 1000 && count < 10000) {
                        share_count = (count / 1000).toFixed(1) + "K"
                    } else {
                        share_count = (count / 10000).toFixed(1) + "W"
                    }
                    $("#aweme_share_count").html(share_count);

                    $("#icons").attr("style", "display:flex;");//显示 icons
                    $("#icon").attr("style", "display:table-row;");//显示 icon
                    $("#music").attr("style", "display:inline;");//显示 music

                    $("#loading").attr("style", "display:none;");//隐藏 loading
                    $("#download").attr("style", "display:block;");//显示 download
                    // alert("SUCCESS");
                    // 执行弹框
                    narnSuccess();
                }

                if (result.awemeType === 2) {
                    if (result.status === 4) {
                        $("#loading").attr("style", "display:none;");//隐藏 loading
                        $("#download").attr("style", "display:none;");//隐藏 download
                        // 执行弹框
                        narnWarn()
                    } else {
                        $("#AwemeOrLive").html("下载直播");
                        $("#awemeType").html("预览直播");
                        $("#video").attr("href", removeHttp(result.flv_pull_url0));
                        $("#pre_video").attr("src", removeHttp(result.flv_pull_url0));

                        $("#cover").attr("href", removeHttp(result.cover));
                        $("#pre_video").attr("poster", result.cover);
                        $("#avatar").attr("src", removeHttp(result.avatar));
                        $("#avatar").attr("alt", result.nickname);
                        $("#nickname").html(result.nickname);
                        $("#desc").html(result.title);

                        $("#video").attr("style", "display:inline;");//显示 video
                        $("#icons").attr("style", "display:none;");//隐藏 icons
                        $("#icon").attr("style", "display:none;");//隐藏 icon
                        $("#music").attr("style", "display:none;");//隐藏 music

                        $("#loading").attr("style", "display:none;");//隐藏 loading
                        $("#download").attr("style", "display:block;");//显示 download
                        // alert("SUCCESS");
                        // 执行弹框
                        narnSuccess();
                    }
                }
            } else {
                $("#loading").attr("style", "display:none;");//隐藏 loading
                $("#download").attr("style", "display:none;");//隐藏 download

                // 执行弹框
                narnFail();
            }
            ;
        },
        error: function (xhr, type) {
            $("#loading").attr("style", "display:none;");//隐藏 loading
            $("#download").attr("style", "display:none;");//隐藏 download
            // alert("异常！");

            // 执行弹框
            narnFail();
        }
    });
}

// 右上角弹框
function narnSuccess() {
    naranja().success({
        title: '解析成功',
        text: '请及时下载音视频',
        icon: true,
        timeout: 5000,
        buttons: []
    })
}

function narnFail() {
    naranja().error({
        title: '解析失败',
        text: '直播/视频/图集不存在或接口失效',
        icon: true,
        timeout: 5000,
        buttons: []
    })
}

function narnWarn() {
    naranja().warn({
        title: '提示',
        text: '直播未开始',
        icon: true,
        timeout: 5000,
        buttons: []
    })
}


window.addEventListener('DOMContentLoaded', function () {
    document.getElementById('view_aweme').addEventListener('click', function () {
        var awemeType = document.getElementById("awemeType").innerText;

        if (awemeType === "预览视频") {
            // 调小音量
            var videoElement = document.getElementById("pre_video");
            videoElement.volume = 0.6
            /*弹出视频播放层*/
            $("#show-video").show();
        }
        // 图片查看器
        if (awemeType === "预览图集") {

            var viewer = new Viewer(document.getElementById('images'), {
                hidden: function () {
                    viewer.destroy();
                },
            });

            // image.click();
            viewer.show();
        }
        // 预览直播
        if (awemeType === "预览直播") {
            if (flvjs.isSupported()) {//检查flvjs能否正常使用
                var videoElement = document.getElementById('pre_video');//使用id选择器找到第二步设置的dom元素
                var flvPlayer = flvjs.createPlayer({//创建一个新的flv播放器对象
                    type: 'flv',//类型flv
                    url: $("#video").attr("href")//flv文件地址
                });
                flvPlayer.attachMediaElement(videoElement);//将flv视频装载进video元素内
                flvPlayer.load();//载入视频
                flvPlayer.play();//播放视频，如果不想要自动播放，去掉本行

                /*弹出视频播放层*/
                $("#show-video").show();
            }
        }


    });
    /*关闭视频播放层*/
    $(".video-close").click(function () {
        var videoElement = document.getElementById("pre_video");
        videoElement.pause()
        $("#show-video").hide();
    })
});


function removeHttp(url) {
    if (typeof (url) == 'string') {
        url = url.replace(/^https?:/, '');
    }
    return url;
}