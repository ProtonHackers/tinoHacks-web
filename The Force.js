// Written for tampermonkey for chrome

// ==UserScript==
// @name         The Force
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Vineet Mudupalli
// @grant        none
// @include      https://www.youtube.com/watch?*
// @include      *spotify.com*
// @require      http://code.jquery.com/jquery-3.2.1.js
// ==/UserScript==

//var player;
//window.onYouTubeIframeAPIReady = function() {
// console.log("YouTube API Ready");

if(window.location.href.indexOf("youtube") != -1){
    var play = "";
    var downvol = "";
    var upvol = "";



    $.get("https://forcething.firebaseio.com/.json", function(data){
        play = data.play; 
        upvol = data.upvolume;
        downvol = data.downvolume;
        setInterval(pplay, 100);   
    });

    function pplay(){
        $.get("https://forcething.firebaseio.com/.json", function(data){
            var tempplay = data.play;
            var tempupvol = data.upvolume;
            var tempdownvol = data.downvolume;
            if(tempplay != play){

                play = tempplay;

                var video = document.getElementsByTagName("video")[0];
                if (video.paused) {
                    video.play();}
                else {video.pause();}
            }
            if(tempupvol != upvol){

                upvol = tempupvol;

                var volup = document.getElementsByTagName('video')[0].volume;

                if( volup +0.50 > 1.00){
                    document.getElementsByTagName("video")[0].volume = 1.;
                }
                else{ document.getElementsByTagName("video")[0].volume = (volup +0.50);}

            }
            if( tempdownvol != downvol){

                downvol = tempdownvol;

                var vol = document.getElementsByTagName("video")[0].volume;

                if( vol - 0.50 < 0.0){
                    document.getElementsByTagName('video')[0].volume = 0.0;
                }
                else{ document.getElementsByTagName("video")[0].volume = (vol -0.50);} }

        });}}

if(window.location.href.indexOf("spotify") != -1){
    var plays = "";
    var downvols = "";
    var upvols = "";



    $.get("https://forcething.firebaseio.com/.json", function(datas){
        plays = datas.play; 
        upvols = datas.upvolume;
        downvols = datas.downvolume;
        setInterval(pplays, 100);   
    });

    function pplays(){
        $.get("https://forcething.firebaseio.com/.json", function(datas){
            var tempplays = datas.play;
            var tempupvols = datas.upvolume;
            var tempdownvols = datas.downvolume;
            if(tempplays != plays){
                plays = tempplays;
                (document.querySelector(".spoticon-play-16") || document.querySelector(".spoticon-pause-16")).click();
            }
            if(tempupvols != upvols){
                upvols = tempupvols; 
                document.querySelector(".spoticon-skip-forward-16").click();

            }
            if( tempdownvols != downvols){
                downvols = tempdownvols;
                document.querySelector(".spoticon-skip-back-16").click();
            }

        });}}

