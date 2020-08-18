var block = document.getElementById("artist_block");
block.innerHTML = ""
for (let artist of artists) {
    let name = artist["name"];
    let imgURL = artist["img_url"];
    let followers = artist["followers"];
    let genre = artist["genres"][0];
    block.innerHTML +=
        '<div class="col-sm-6 artist">' +
        '<img class="artist-img" loading="lazy" src="' + imgURL + '" />' +
        '<div class="col-sm-6 artist-info">' +
        '<h4 class="artist-name">' + name + '</h4>' +
        '<span class="artist-genre">' + genre + '</span></br>' +
        '<span class="artist-followers">' + followers.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' followers</span></br>' +
        '<div class="artist-release">' +
        '<span class="artist-release-album">with <b>' + artist["album_release"] + '</b></span></br>' +
        '<span class="artist-release-date">' + artist["release_date"] + '</span></br>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '</div>';
}