navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => { handlerFunction(stream) })

function handlerFunction(stream) {
    rec_norm = new MediaRecorder(stream);
    rec_norm.ondataavailable = e => {
        audio_chunks_normal.push(e.data);
    }
    rec_elder = new MediaRecorder(stream);
    rec_elder.ondataavailable = e => {
        audio_chunks_elder.push(e.data);
    }
}


const big_content = document.getElementById('big-content');
const small_content = document.getElementById('small-content');
const el_compare = document.getElementById('compare');
const btn_process = document.getElementById('process');
let el_loading = document.getElementById('loading');

//normaal elements
const btn_record_normal = document.getElementById('btn-record-normal');
const picture_normaal = document.getElementById('picture_normaal');
const tekst_bij_foto_normaal = document.getElementById('tekst_bij_foto_normaal');
const saved_normaal = document.getElementById('saved_normaal');
let mp3_normaal = document.getElementById('mp3_normaal');
let el_pitch_norm = document.getElementById('pitch_norm');
let el_loudness_norm = document.getElementById('loudness_norm');
let el_pitch_norm_filtered = document.getElementById('pitch_norm_filtered');
let el_loudness_norm_filtered = document.getElementById('loudness_norm_filtered');
let el_sil_tot_norm = document.getElementById('sil_tot_norm');
let el_sil_perc_norm = document.getElementById('sil_perc_norm');

//elder elements
const btn_record_elder = document.getElementById('btn-record-elder');
const picture_elder = document.getElementById('picture_elder');
const tekst_bij_foto_elder = document.getElementById('tekst_bij_foto_elder');
const saved_elder = document.getElementById('saved_elder');
let mp3_elder = document.getElementById('mp3_elder');
let el_pitch_elder = document.getElementById('pitch_elder');
let el_loudness_elder = document.getElementById('loudness_elder');
let el_pitch_elder_filtered = document.getElementById('pitch_elder_filtered');
let el_loudness_elder_filtered = document.getElementById('loudness_elder_filtered');
let el_sil_tot_elder = document.getElementById('sil_tot_elder');
let el_sil_perc_elder = document.getElementById('sil_perc_elder');
let extract_text = document.getElementById('extract_text');

//normal parameters
let pitch_normal = 0;
let loudness_normal = 0;
let audio_chunks_normal = [];
let audio_chunks_elder = [];

Number.prototype.round = function (places) {
    return +(Math.round(this + "e+" + places) + "e-" + places);
}

function sendData(blob_normaal, blob_elder) {

    let audioUrlNormaal = URL.createObjectURL(blob_normaal);
    let recordedAudioNormaal = document.getElementById('recordedAudioNormaal')
    recordedAudioNormaal.src = audioUrlNormaal;
    recordedAudioNormaal.controls = true;
    recordedAudioNormaal.autoplay = false;

    let audioUrlElder = URL.createObjectURL(blob_elder);
    let recordedAudioElder = document.getElementById('recordedAudioElder')
    recordedAudioElder.src = audioUrlElder;
    recordedAudioElder.controls = true;
    recordedAudioElder.autoplay = false;


    let data_to_send = new FormData();
    data_to_send.append('audio_normal', blob_normaal);
    data_to_send.append('audio_elder', blob_elder);

    if (extract_text.checked) {
        data_to_send.append('extract_text', true);
    } else {
        data_to_send.append('extract_text', false);
    }

    console.log('Prepared')
    fetch('/receive_audio', {
        method: 'POST',
        body: data_to_send
    }).then(response => {
        el_loading.classList.add('hidden');
        btn_process.classList.remove('hidden');
        return response.json();
    }).then(json => {
        pitch_normal = json['normal']['pitch'];
        loudness_normal = json['normal']['loudness'];
        pitch_normal_filtered = json['normal_filtered']['pitch'];
        loudness_normal_filtered = json['normal_filtered']['loudness'];
        sil_tot_norm = `${json['normal']['silence_length']} / ${json['normal']['original_length']}`;
        sil_perc_norm = json['normal']['silence_percentage'];
        pitch_elder = json['elder']['pitch'];
        loudness_elder = json['elder']['loudness'];
        pitch_elder_filtered = json['elder_filtered']['pitch'];
        loudness_elder_filtered = json['elder_filtered']['loudness'];
        sil_tot_elder = `${json['elder']['silence_length']} / ${json['elder']['original_length']}`;
        sil_perc_elder = json['elder']['silence_percentage'];


        const divPitchComparison = document.createElement('div');
        divPitchComparison.innerHTML = json['pitch_comparison'];
        el_compare.insertAdjacentElement('beforeend', divPitchComparison);

        const divLoudnessComparison = document.createElement('div');
        divLoudnessComparison.innerHTML = json['loudness_comparison'];
        el_compare.insertAdjacentElement('beforeend', divLoudnessComparison);

        if (json['elder']['speech_recognition'] !== "Tekst-extractie is uitgeschakeld") {
            big_content.insertAdjacentHTML("beforeend", `<div><h4>Wat heb je gezegd?</h4><p>${json['elder']['speech_recognition']}</p></div>`);
            big_content.insertAdjacentHTML("beforeend", `<div><h4>Verkleinwoorden:</h4><p>${json['elder']['verkleinwoorden']}</p></div>`);
            big_content.insertAdjacentHTML("beforeend", `<div><h4>Herhalingen:</h4><p>${json['elder']['herhalingen']}</p></div>`);
            big_content.insertAdjacentHTML("beforeend", `<div><h4>Collectieve voornaamwoorden:</h4><p>${json['elder']['collectieve_voornaamwoorden']}</p></div>`);
            big_content.insertAdjacentHTML("beforeend", `<div><h4>Tussenwerpsels:</h4><p>${json['elder']['tussenwerpsels']}</p></div>`);
        }

    }).then(_ => {
        el_pitch_norm.innerText = pitch_normal;
        el_loudness_norm.innerText = parseFloat(loudness_normal).round(2);
        el_pitch_norm_filtered.innerText = pitch_normal_filtered;
        el_loudness_norm_filtered.innerText = parseFloat(loudness_normal_filtered).round(2);
        el_sil_tot_norm.innerText = sil_tot_norm;
        el_sil_perc_norm.innerText = sil_perc_norm;
        el_pitch_elder.innerText = pitch_elder;
        el_loudness_elder.innerText = parseFloat(loudness_elder).round(2);
        el_pitch_elder_filtered.innerText = pitch_elder_filtered;
        el_loudness_elder_filtered.innerText = parseFloat(loudness_elder_filtered).round(2);
        el_sil_tot_elder.innerText = sil_tot_elder;
        el_sil_perc_elder.innerText = sil_perc_elder;
    }).catch((error) => {
        console.log(error)
    });
}

btn_process.addEventListener('click', () => {
    if (audio_chunks_normal.length > 0 && audio_chunks_elder.length > 0) {
        el_loading.classList.remove('hidden');
        btn_process.classList.add('hidden');
        let blob_normaal = new Blob(audio_chunks_normal, { type: 'audio/mp3' });
        let blob_elder = new Blob(audio_chunks_elder, { type: 'audio/mp3' });
        sendData(blob_normaal, blob_elder);
    }
    else if (mp3_normaal.files.length > 0 && mp3_elder.files.length > 0) {
        el_loading.classList.remove('hidden');
        btn_process.classList.add('hidden');
        let blob_normaal = mp3_normaal.files[0];
        let blob_elder = mp3_elder.files[0];
        sendData(blob_normaal, blob_elder);
    }
    else if (mp3_normaal.files.length > 0 && audio_chunks_elder.length > 0) {
        el_loading.classList.remove('hidden');
        btn_process.classList.add('hidden');
        let blob_normaal = mp3_normaal.files[0];
        let blob_elder = new Blob(audio_chunks_elder, { type: 'audio/mp3' });
        sendData(blob_normaal, blob_elder);
    }
    else if (audio_chunks_normal.length > 0 && mp3_elder.files.length > 0) {
        el_loading.classList.remove('hidden');
        btn_process.classList.add('hidden');
        let blob_normaal = new Blob(audio_chunks_normal, { type: 'audio/mp3' });
        let blob_elder = mp3_elder.files[0];
        sendData(blob_normaal, blob_elder);
    }
    else {
        console.log("No audio recorded or uploaded for either normal or elder");
    }
});

console.log("PRESENT!!")


function start_audio_normal(text_after) {
    audio_chunks_normal = [];
    mp3_normaal.value = "";
    rec_norm.start();
    console.log("STARTED RECORDING");
    btn_record_normal.classList.remove("btn-primary");
    btn_record_normal.classList.add("btn-warning");
    btn_record_normal.innerText = "stop standaard opname"
}

function stop_audio_normal(text_after, text_before) {
    console.log("STOPPED RECORDING");
    btn_record_normal.classList.add("btn-primary");
    btn_record_normal.classList.remove("btn-warning");
    btn_record_normal.innerText = "standaard audio opnemen"
    rec_norm.stop();
    saved_normaal.classList.remove('hidden');
}

btn_record_normal.addEventListener('click', () => {
    console.log("CLICKED");
    if (btn_record_normal.innerText.toLowerCase() === "standaard audio opnemen") {
        start_audio_normal()
    } else if (btn_record_normal.innerText.toLowerCase() === "stop standaard opname") {
        stop_audio_normal()
    }
})




//elder
function start_audio_elder() {
    audio_chunks_elder = [];
    mp3_elder.value = "";
    rec_elder.start();
    console.log("STARTED RECORDING");
    btn_record_elder.classList.remove("btn-primary");
    btn_record_elder.classList.add("btn-warning");
    btn_record_elder.innerText = "stop elder opname"
}

function stop_audio_elder() {
    console.log("STOPPED RECORDING Elder");
    btn_record_elder.classList.add("btn-primary");
    btn_record_elder.classList.remove("btn-warning");
    btn_record_elder.innerText = "elder audio opnemen"
    rec_elder.stop();
    saved_elder.classList.remove('hidden');

}

btn_record_elder.addEventListener('click', () => {
    console.log("CLICKED Elder");
    if (btn_record_elder.innerText.toLowerCase() === "elder audio opnemen") {
        start_audio_elder()
    } else if (btn_record_elder.innerText.toLowerCase() === "stop elder opname") {
        stop_audio_elder()
    }
})