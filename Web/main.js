let playing = false;
let player = -1;
let mic_high = false;
const startBtn = document.getElementById("start-btn");
const logSpan = document.getElementById("log")

console.log(startBtn);

let ws = null;

startBtn.addEventListener("click", () => {
  ws = new WebSocket("wss://guindaillesim.tech:8080");

  ws.onopen = () => {
    console.log("Connected to ws!");
    startBtn.style.display = "none"
  };

  ws.onerror = (e) => {
    console.log(e);
    logSpan.innerHTML = "Connection Error";
    logSpan.className = "nes-text is-error";
  };

  ws.onmessage = (msg) => {
    msg = JSON.parse(msg.data);
    console.log(msg);

    switch (msg.type) {
      case "error": {
        if (msg.content === "full") {
          logSpan.innerHTML = "Game is full!";
          logSpan.className = "nes-text is-error";
        } else {
          logSpan.innerHTML = "Service Error";
          logSpan.className = "nes-text is-error";
        }
        break;
      }
      case "player_connected":
        logSpan.innerHTML = `Waiting for players...`;
        logSpan.className = "nes-text is-primary";
        player = msg.player;
        break;
      case "game_start":
        document.getElementById(
          "log"
        ).innerHTML = `Game started!\nYou are player ${player + 1}.`;
        logSpan.className = "nes-text is-success";
        playing = true
        break;
      case "game_end":
        playing = false
        break;
      default:
        logSpan.innerHTML =
          "Unknown message from server!";
        logSpan.className = "nes-text is-error";
        break;
    }
  };
});

navigator.mediaDevices
  .getUserMedia({ video: false, audio: true })
  .then((stream) => {
    // Create and configure the audio pipeline
    const audioContext = new AudioContext();
    const analyzer = audioContext.createAnalyser();
    analyzer.fftSize = 512;
    analyzer.smoothingTimeConstant = 0.1;
    const sourceNode = audioContext.createMediaStreamSource(stream);
    sourceNode.connect(analyzer);

    // Analyze the sound
    setInterval(() => {
      // Compute the max volume level (-Infinity...0)
      const fftBins = new Float32Array(analyzer.frequencyBinCount); // Number of values manipulated for each sample
      analyzer.getFloatFrequencyData(fftBins);
      // audioPeakDB varies from -Infinity up to 0
      const audioPeakDB = Math.max(...fftBins);

      // Compute a wave (0...)
      const frequencyRangeData = new Uint8Array(analyzer.frequencyBinCount);
      analyzer.getByteFrequencyData(frequencyRangeData);
      const sum = frequencyRangeData.reduce((p, c) => p + c, 0);
      // audioMeter varies from 0 to 10
      const audioMeter = Math.sqrt(sum / frequencyRangeData.length);

      console.log(audioMeter)

      if (playing) {
        ws.send(
          JSON.stringify({
            type: audioMeter > 7.2 ? "mic_high": "mic_low"
          })
        );
      }
    }, 300);
  })
  .catch((err) => {
    console.error(`you got an error: ${err}`);
  });
