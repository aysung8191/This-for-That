const arrows = document.querySelectorAll('.gallery-arrows')

document.addEventListener('DOMContentLoaded', function() {
    if (arrows) {
        document.getElementById('arrow-left').addEventListener('click', runCarouseLeft)
        document.getElementById('arrow-right').addEventListener('click', runCarouseRight)
    }
})

function runCarouseLeft(e) {
    const curImg = document.getElementById('cur-img')
    const curImgID = curImg.dataset.imgId
    const gallery = document.getElementById('img-gallery')
    imgList = gallery.querySelectorAll('img')
    for (let i = 0; i < imgList.length; i++) {
        if(imgList[i].dataset.galleryImgId === curImgID) {
            if (i === 0) {
                curImg.src = imgList[imgList.length-1].src
                curImg.dataset.imgId = imgList[imgList.length-1].dataset.galleryImgId
            } else {
                curImg.src = imgList[i-1].src
                curImg.dataset.imgId = imgList[i-1].dataset.galleryImgId
            }
        }
    }
}

function runCarouseRight(e) {
    const curImg = document.getElementById('cur-img')
    console.log(curImg)
    const curImgID = curImg.dataset.imgId
    const gallery = document.getElementById('img-gallery')
    imgList = gallery.querySelectorAll('img')
    for (let i = 0; i < imgList.length; i++) {
        if(imgList[i].dataset.galleryImgId === curImgID) {
            if (i === imgList.length-1) {
                curImg.src = imgList[0].src
                curImg.dataset.imgId = imgList[0].dataset.galleryImgId
            } else {
                curImg.src = imgList[i+1].src
                curImg.dataset.imgId = imgList[i+1].dataset.galleryImgId
            }
        }
    }
}