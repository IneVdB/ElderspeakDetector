navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => { handlerFunction(stream) })

function handlerFunction(stream) {
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

let audio_chunks_elder = [];

Number.prototype.round = function (places) {
    return +(Math.round(this + "e+" + places) + "e-" + places);
}

function sendData(blob_elder) {

    let audioUrlElder = URL.createObjectURL(blob_elder);
    let recordedAudioElder = document.getElementById('recordedAudioElder')
    recordedAudioElder.src = audioUrlElder;
    recordedAudioElder.controls = true;
    recordedAudioElder.autoplay = false;


    let data_to_send = new FormData();
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
        pitch_elder = json['elder']['pitch'];
        loudness_elder = json['elder']['loudness'];
        pitch_elder_filtered = json['elder_filtered']['pitch'];
        loudness_elder_filtered = json['elder_filtered']['loudness'];
        sil_tot_elder = `${json['elder']['silence_length']} / ${json['elder']['original_length']}`;
        sil_perc_elder = json['elder']['silence_percentage'];

        if (json['elder']['speech_recognition'] !== "Tekst-extractie is uitgeschakeld") {
            big_content.insertAdjacentHTML("beforeend", `<div><h4>Wat heb je gezegd?</h4><p>${json['elder']['speech_recognition']}</p></div>`);
            big_content.insertAdjacentHTML("beforeend", `<div><h4>Verkleinwoorden:</h4><p>${json['elder']['verkleinwoorden']}</p></div>`);
            big_content.insertAdjacentHTML("beforeend", `<div><h4>Herhalingen:</h4><p>${json['elder']['herhalingen']}</p></div>`);
            big_content.insertAdjacentHTML("beforeend", `<div><h4>Collectieve voornaamwoorden:</h4><p>${json['elder']['collectieve_voornaamwoorden']}</p></div>`);
            big_content.insertAdjacentHTML("beforeend", `<div><h4>Tussenwerpsels:</h4><p>${json['elder']['tussenwerpsels']}</p></div>`);
        }

    }).then(_ => {
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
    if (audio_chunks_elder.length > 0) {
        el_loading.classList.remove('hidden');
        btn_process.classList.add('hidden');
        let blob_elder = new Blob(audio_chunks_elder, { type: 'audio/mp3' });
        sendData(blob_elder);
    }
    else if (mp3_elder.files.length > 0) {
        el_loading.classList.remove('hidden');
        btn_process.classList.add('hidden');
        let blob_elder = mp3_elder.files[0];
        sendData(blob_elder);
    }
    else if (audio_chunks_elder.length > 0) {
        el_loading.classList.remove('hidden');
        btn_process.classList.add('hidden');
        let blob_elder = new Blob(audio_chunks_elder, { type: 'audio/mp3' });
        sendData(blob_elder);
    }
    else if (mp3_elder.files.length > 0) {
        el_loading.classList.remove('hidden');
        btn_process.classList.add('hidden');
        let blob_elder = mp3_elder.files[0];
        sendData(blob_elder);
    }
    else {
        console.log("No audio recorded or uploaded");
    }
});

console.log("PRESENT!!")

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