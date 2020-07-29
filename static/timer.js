/*
 * Copyright (c) 2020  Ngô Ngọc Đức Huy
 */

const minute = document.querySelector('#minute');
const second = document.querySelector('#second');

function getCookie(name) {
    return document.cookie.split('; ').reduce((r, v) => {
        const parts = v.split('=');
        return parts[0] === name ? decodeURIComponent(parts[1]) : r;
    }, '');
}

function getTimeDifference(difference) {
    if (difference < 0) {
        return [0, 0];
    }
    let minutes = Math.floor(difference / 1000 / 60);
    let seconds = Math.floor((difference / 1000) - minutes * 60);
    return [minutes, seconds];
}

function prettyTime(time) {
    if (time < 10) {
        return '0' + time;
    } else {
        return time.toString()
    }
}

let expiration = new Date(getCookie('exp') * 1000);
let reminded = false

function countDown() {
    let current = new Date();
    let difference = getTimeDifference(expiration - current);
    minute.innerHTML = prettyTime(difference[0]);
    second.innerHTML = prettyTime(difference[1]);
    if (!reminded && difference[0] === 0) {
        M.toast({html: "You're running out of time"});
        M.toast({html: "You can add more time by clicking on \"Add more time\""});
        reminded = true;
    }
}

setInterval(countDown, 1000)
